"""
Weather Webapp using Flask, Gunicorn and Nginx
API: https://api.open-meteo.com/v1/forecast

Active env:        $ . .venv/bin/activate
Run application:   $ flask --app weather run
Install dependency: pip install --break-system-packages --user <dependency>
"""

import os
import json
import logging
from decimal import Decimal
from datetime import datetime, timedelta
import boto3
from boto3 import client
import ecs_logging
from flask import Flask, render_template, request, abort, Response, jsonify, send_from_directory
from geopy.geocoders import Nominatim
import openmeteo_requests
import requests_cache
from retry_requests import retry
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, generate_latest
from day import forecast

app = Flask(__name__)

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.3')
location_request_counter = Counter('location_counter', 'HTTP Location Requests Total', ['location'])
'''
logging.basicConfig(filename='/var/log/flask/app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('/var/log/flask/logs.json')
handler.setFormatter(ecs_logging.StdlibFormatter())
logger.addHandler(handler)
'''
def get_location_from_args(location_arg):
    """ Get location from user input """
    geolocator = Nominatim(user_agent="weather.py")
    location = geolocator.geocode(location_arg, language="en")
    return location

def fetch_weather_data(location):
    """ Fetch weather data from the API """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "hourly": ["temperature_2m", "relative_humidity_2m", "is_day"],
        "timezone": "GMT"
    }
    responses = openmeteo.weather_api(url, params=params)
    if responses is None or responses[0] is None:
        raise ValueError("Failed to fetch weather data")
    return responses[0]

def process_hourly_data(response):
    """ Process the hourly weather data """
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_is_day = hourly.Variables(2).ValuesAsNumpy()

    forecasts = []

    for day in range(7):
        count_is_day = 0
        day_temp_sum = 0
        night_temp_sum = 0
        day_humidity_sum = 0

        for hour in range(24):
            index = day * 24 + hour
            temperature = hourly_temperature_2m[index]
            humidity = hourly_relative_humidity_2m[index]
            is_day = hourly_is_day[index]

            if is_day:
                day_temp_sum += temperature
                count_is_day += 1
            else:
                night_temp_sum += temperature

            day_humidity_sum += humidity

        avg_day_temp = day_temp_sum / count_is_day if count_is_day > 0 else -99999
        avg_night_temp = night_temp_sum / (24 - count_is_day) if (24 - count_is_day) > 0 else -99999
        avg_daily_humidity = day_humidity_sum / 24

        date_obj = datetime.today().date() + timedelta(days=day)
        forecast_instance = {
            "date": str(date_obj),
            "avg_night_temp": float(avg_night_temp),
            "avg_day_temp": float(avg_day_temp),
            "avg_daily_humidity": float(avg_daily_humidity)
        }
        forecasts.append(forecast_instance)

    return forecasts

def convert_to_decimal(data):
    """ Convert data types to int for AWS DynamoDB """
    if isinstance(data, dict):
        return {k: convert_to_decimal(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_decimal(i) for i in data]
    elif isinstance(data, float):
        return Decimal(str(data))
    return data

def data_history(location, forecasts):
    """ Save history of search data to a JSON file """
    date_str = datetime.today().strftime("%m-%d-%Y")
    filename = f"{location}_{date_str}.json"
    filepath = os.path.join('data_history', filename)
    if not os.path.exists('data_history'):
        os.makedirs('data_history')
    with open(filepath, 'w') as json_file:
        json.dump(forecasts, json_file, indent=4)

@app.context_processor
def env_vars():
    """ Send environment variables to app routes """
    return {
        'BG_COLOR': os.getenv('BG_COLOR', '#121212')
    }

@app.route('/', methods=['GET'])
def get_weather():
    """ Main page to get location from user and get forecast data from API """
    app.logger.debug("Received GET request to root route")
    if request.method == 'GET':
        location_arg = request.args.get('location')

        if location_arg is None or location_arg.strip() == '':
            app.logger.info("No location provided, rendering location.html")
            return render_template('location.html')

        try:
            location = get_location_from_args(location_arg)
            if location is None:
                app.logger.info("No location provided, rendering location.html")
                return render_template('location.html', locationError="Location not found 👍")

            app.logger.info(f"Location geocode obtained: {location_arg}")
            location_request_counter.labels(location=location_arg).inc()
            response = fetch_weather_data(location)
            forecasts = process_hourly_data(response)
            data_history(location_arg, forecasts)

        except ValueError as e:
            logging.error(f"Error during backup: {e}")
            return render_template('location.html', locationError=str(e))

        app.logger.debug(f"Weather data successfully retrieved for location: {location_arg}")
        return render_template('forecast.html',
                               forecasts=forecasts,
                               location=location,
                               locationError=None
                               )

@app.route('/staticWeb')
def static_web():
    """ Present static web for AWS S3 bucket """
    return render_template('staticWeb.html')

@app.route('/health')
def health_check():
    """ Check web connectivity """
    return 'Healthy', 200

@app.route('/download', methods=['GET'])
def get_image():
    """ Download sky's image from AWS S3 bucket """
    s3 = client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                      aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    file = s3.get_object(Bucket='tasty-kfc-bucket', Key='sky.jpg')
    return Response(
        file['Body'].read(),
        headers={"Content-Disposition": "attachment;filename=sky.jpg"}
    )

@app.route('/database', methods=['POST'])
def save_data():
    """ Save weather data to AWS DynamoDB """
    dynamodb = boto3.resource('dynamodb',
                   aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                   aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                   region_name='eu-central-1')
    table = dynamodb.Table('WeatherData')
    location = request.form.get('location')
    date = request.form.get('date')
    forecasts = request.form.get('forecast_data')
    forecasts = convert_to_decimal(forecasts)
    item = {
        'Location': location,
        'Date': date,
        'forecasts': forecasts
    }
    table.put_item(Item=item)
    return jsonify({'message': 'Data saved successfully.'}), 200

@app.route('/api/backuphaifa', methods=['GET'])
def backup_haifa():
    """ Auto backups of Haifa's weather to AWS DynamoDB """
    dynamodb = boto3.resource('dynamodb',
                   aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                   aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                   region_name='eu-central-1')
    table = dynamodb.Table('HaifaWeather')
    location = get_location_from_args("Haifa")
    response = fetch_weather_data(location)
    forecasts = convert_to_decimal(process_hourly_data(response))
    item = {
            'Location': 'Haifa',
            'Date': str(datetime.today().date()),
            'forecasts': forecasts
    }
    table.put_item(Item=item)
    return jsonify({'message': 'Data saved successfully.'}), 200

@app.route('/metrics')
def metrics():
    """ Expose metrics for Prometheus """
    return generate_latest()

@app.route('/logs')
def elkstack_logs():
    """ Expose logs for ELK Stack """
    app.logger.debug("Debug log level")
    app.logger.info("Program running correctly")
    app.logger.warning("Warning; low disk space!")
    app.logger.error("Error!")
    app.logger.critical("Program halt!")
    return "logger levels!"

@app.route('/history', methods=['GET'])
def list_files():
    """ List all saved history JSON files """
    files = os.listdir('data_history')
    location_filter = request.args.get('location')
    date_filter = request.args.get('date')
    if location_filter:
        files = [f for f in files if location_filter in f]
    if date_filter:
        files = [f for f in files if date_filter in f]
    return render_template('history.html', files=files)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """ Download the specified JSON file """
    return send_from_directory('data_history', filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
