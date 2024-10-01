FROM python:3.12-slim
LABEL org.opencontainers.image.source = "https://github.com/niv-devops/weather-webapp"
WORKDIR /webapp
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
ENTRYPOINT ["/bin/sh", "-c"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
