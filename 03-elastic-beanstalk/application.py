
import os
from flask import Flask, jsonify

application = Flask(__name__)

APP_ENV = os.getenv("APP_ENV", "development")
APP_VERSION = os.getenv("APP_VERSION", "1.0")
APP_MESSAGE = os.getenv(
    "APP_MESSAGE",
    "Hello from AWS Elastic Beanstalk!"
)


@application.route("/")
def home():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Elastic Beanstalk CI/CD</title>
        <style>
            body {{
                background: #111827;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 100px 20px;
            }}
            .card {{
                background: #1f2937;
                padding: 40px;
                border-radius: 15px;
                display: inline-block;
            }}
            h1 {{ color: #60a5fa; }}
            .status {{ color: #34d399; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>AWS Elastic Beanstalk Deployment Successful!</h1>
            <h2 class="status">{APP_MESSAGE}</h2>
            <p>Environment: {APP_ENV}</p>
            <p>Application Version: {APP_VERSION}</p>
            <p>Platform: Python + Flask</p>
        </div>
    </body>
    </html>
    """


@application.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "environment": APP_ENV,
        "version": APP_VERSION
    })


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
