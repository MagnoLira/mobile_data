# Mobile Data


Overview

This project provides a comprehensive solution for monitoring mobile application usage and battery statistics using ADB (Android Debug Bridge). It includes a Python-based API built with FastAPI to expose key functionalities, a modularized architecture for clarity and maintainability, and a robust data storage mechanism in a structured database instead of CSV files.

Features

1. Application Usage Monitoring

      Captures detailed app usage data, including:

      Timestamp of the event

      Event type (e.g., app opened, closed, or interacted with)

      Package name of the app

2. Battery Status Monitoring

      Extracts detailed battery information such as:

      Charging type (AC, USB, wireless)

      Battery level, voltage, and temperature

      Charging current and health status

3. RESTful API Endpoints

      Start/Stop Monitoring: Control the monitoring process dynamically.

      Retrieve Data: Fetch real-time or stored application usage and battery data.

      Health Check: Ensure the system is running smoothly.

4. Modular Architecture

The project follows a structured and scalable architecture:

project/
├── adb/
│   ├── __init__.py          # Global imports for the ADB package.
│   ├── battery_utils.py     # Functions for battery monitoring.
│   ├── app_usage_utils.py   # Functions for app usage tracking.
│   ├── adb_utils.py         # General ADB interaction commands.
├── processing/
│   ├── __init__.py          # Global imports for processing.
│   ├── battery_processing.py  # Processing battery data.
│   ├── app_usage_processing.py # Processing app usage data.
├── db/
│   ├── __init__.py          # General database configurations.
│   ├── credentials.py       # Manages database access credentials.
│   ├── landing_layer.py     # Functions for the landing layer (raw data).
│   ├── silver_layer.py      # Functions for the silver layer (processed data).
│   ├── gold_layer.py        # Functions for the gold layer (analytical data).
│   ├── db_utils.py          # Utility functions for database connections and transactions.
├── utils/
│   ├── __init__.py          # Global imports for utilities.
│   ├── logging.py           # Logging configuration and management.
│   ├── validation.py        # Generic validations and checks.
├── api/
│   ├── __init__.py          # API configurations.
│   ├── endpoints.py         # Defines API endpoints (FastAPI).
├── main.py                  # Entry point to start the application and connect modules.
├── requirements.txt         # Project dependencies.
├── .gitignore               # Files and directories ignored by Git.
└── README.md                # Project documentation.

5. Database Storage

It follows a multi-layered data approach:

      Landing Layer: Raw data ingestion.

      Silver Layer: Processed and structured data.

      Gold Layer: Optimized for analytics and reporting.

API Endpoints

Application Usage

      GET /app-usage/retrieveFetch the latest app usage data.

      GET /app-usage/historicalRetrieve historical app usage data from the database.

Battery Status

      GET /battery-status/retrieveFetch the current battery status.

      GET /battery-status/historicalRetrieve historical battery status data from the database.

Monitor Control

      POST /monitor/startStart the data monitoring process.

      POST /monitor/stopStop the data monitoring process.

System Health

      GET /healthCheck the health status of the API.






