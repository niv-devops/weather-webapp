import pytest
from weather import app, get_location_from_args, fetch_weather_data, process_hourly_data

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_location_from_args():
    location = get_location_from_args("Haifa")
    assert location is not None
    assert location.address == "Haifa, Israel"

def test_fetch_weather_data(mocker):
    mock_response = {
        'latitude': 32.8156,
        'longitude': 34.9885,
        'hourly': {
            'temperature_2m': [20, 21, 22],
            'relative_humidity_2m': [50, 55, 60],
            'is_day': [1, 1, 0]
        }
    }

    mocker.patch('openmeteo_requests.Client.weather_api', return_value=[mock_response])
    location = mock_response
    response = fetch_weather_data(location)
    assert response['latitude'] == 32.8156

def test_process_hourly_data():
    mock_response = {
        'Hourly': lambda: {
            'Variables': lambda x: {'ValuesAsNumpy': [20, 21, 22]} if x == 0 else
                                     {'ValuesAsNumpy': [50, 55, 60]} if x == 1 else
                                     {'ValuesAsNumpy': [1, 1, 0]}
        }
    }

    forecasts = process_hourly_data(mock_response)
    assert len(forecasts) == 7

def test_health_check(client):
    response = client.get('/health')
    assert response.data == b'Healthy'
    assert response.status_code == 200

