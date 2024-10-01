#!/bin/bash
cd /home/ubuntu/webapp
source . .venv/bin/activate
pip install -r requirements.txt
nohup python weather.py > app.log 2>&1 &
