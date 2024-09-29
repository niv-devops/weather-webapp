"""
WSGI entry point for the weather application.
This module runs the application using the WSGI server.
"""
from weather import app

if __name__ == "__main__":
    app.run()
