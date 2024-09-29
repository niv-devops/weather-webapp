FROM python:3.11-slim
LABEL org.opencontainers.image.source = "https://github.com/niv-devops/weather-webapp"
WORKDIR /webapp
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
