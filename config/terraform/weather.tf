terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
}

provider "docker" {}

resource "docker_image" "webapp_tf" {
  name = "devopsgoofy/weather-webapp:latest"
  keep_locally = false
}

resource "docker_container" "webapp_tf" {
  name  = "webappTF"
  image = docker_image.webapp_tf.name
  ports {
    internal = 5000
    external = 5000
  }
}

