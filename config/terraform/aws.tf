terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.65.0"
    }
  }

  required_version = ">= 1.9.5"
}

provider "aws" {
  region = "eu-central-1"
}

data "http" "my_ip" {
  url = "http://checkip.amazonaws.com/"
}

locals {
  my_ip = "${chomp(data.http.my_ip.response_body)}/32"
}

variable "instance_name" {
  type        = string
  default     = "Infinity Terraform Test Server"
}

resource "aws_instance" "terraform" {
  ami           = "ami-0e04bcbe83a83792e"
  instance_type = "t2.micro"

  tags = {
    Name = var.instance_name
  }

  key_name = "k8s"

  vpc_security_group_ids = [aws_security_group.terraform_sg.id]
}

resource "aws_security_group" "terraform_sg" {
  name        = "terraform_sg"

  dynamic "ingress" {
    for_each = [
      {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = [local.my_ip]
      },
      {
        from_port   = 80
        to_port     = 80
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
      },
      {
        from_port   = 443
        to_port     = 443
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
      }
    ]

    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }

  dynamic "egress" {
    for_each = [
      {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
      }
    ]

    content {
      from_port   = egress.value.from_port
      to_port     = egress.value.to_port
      protocol    = egress.value.protocol
      cidr_blocks = egress.value.cidr_blocks
    }
  }
}
