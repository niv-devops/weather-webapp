FROM python:3.12-slim
LABEL org.opencontainers.image.source = "https://github.com/niv-devops/weather-webapp"
WORKDIR /webapp
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends zlib1g=1:1.3.dfsg-3.1ubuntu2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
