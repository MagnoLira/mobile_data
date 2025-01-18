# mobile_data
Overview

This project provides a comprehensive solution for monitoring mobile application usage and battery statistics using ADB (Android Debug Bridge). It includes a Python-based API built with FastAPI to expose key functionalities, modularized code for clarity and maintainability, and a robust data storage mechanism in CSV format for subsequent analysis.




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

      adb_utils.py: Handles all interactions with ADB.
      
      data_processing.py: Processes raw data from ADB outputs.
      
      save_utils.py: Handles data storage in CSV format.
      
      main.py: Manages the API and orchestrates other modules.

5. CSV Data Storage

      Data is persistently stored in CSV files:
      
      app_usage.csv: Stores application usage data.
      
      battery_status.csv: Stores battery statistics.






API Endpoints

Application Usage

  GET /app-usage/retrieve
  Fetch the latest app usage data.
  
  GET /app-usage/historical
  Retrieve historical app usage data stored in app_usage.csv.

Battery Status

  GET /battery-status/retrieve
  Fetch the current battery status.
  
  GET /battery-status/historical
  Retrieve historical battery status data stored in battery_status.csv.

Monitor Control

  POST /monitor/start
  Start the data monitoring process.
  
  POST /monitor/stop
  Stop the data monitoring process.

System Health

  GET /health
  Check the health status of the API.
