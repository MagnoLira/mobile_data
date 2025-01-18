from fastapi import FastAPI, HTTPException
from threading import Thread
from main import monitor_data
import os

app = FastAPI()

# Control variables 
monitoring_thread = None
is_monitoring = False


# Endpoint to verify monitoring status
@app.get("/status")
def get_status():
    status = "running" if is_monitoring else "stopped"
    return {"status": status}


# Start monitoring 
@app.post("/start")
def start_monitoring():
    global monitoring_thread, is_monitoring
    if is_monitoring:
        raise HTTPException(status_code=400, detail="Monitoring is on.")
    monitoring_thread = Thread(target=monitor_data, daemon=True)
    monitoring_thread.start()
    is_monitoring = True
    return {"message": "Monitoring started."}


# Stop monitoring 
@app.post("/stop")
def stop_monitoring():
    global is_monitoring
    if not is_monitoring:
        raise HTTPException(status_code=400, detail="Monitoring is out.")
    is_monitoring = False
    return {"message": "Monitoring stopped. Refresh the server."}


# Query application usage data
@app.get("/data/apps")
def get_app_data():
    filepath = "C:/Users/USER/OneDrive/Documentos/portfolio/mobile_data_project/mobile_data/app_usage.csv"
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Apps usage not find.")
    with open(filepath, "r", encoding="utf-8") as file:
        data = file.readlines()
    return {"data": data[-10:]}   # last 10 lines 


# Query battery's data 
@app.get("/data/battery")
def get_battery_data():
    filepath = "C:/Users/USER/OneDrive/Documentos/portfolio/mobile_data_project/mobile_data/battery_status.csv"
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Battery's data not find.")
    with open(filepath, "r", encoding="utf-8") as file:
        data = file.readlines()
    return {"data": data[-10:]}  # last 10 lines 


# Download
@app.get("/download/{data_type}")
def download_data(data_type: str):
    valid_types = {
        "apps": "C:/Users/USER/OneDrive/Documentos/portfolio/mobile_data_project/mobile_data/app_usage.csv",
        "battery": "C:/Users/USER/OneDrive/Documentos/portfolio/mobile_data_project/mobile_data/battery_status.csv",
    }
    if data_type not in valid_types:
        raise HTTPException(status_code=400, detail="Invalid data type.")
    filepath = valid_types[data_type]
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not find.")
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
    return {"filename": f"{data_type}.csv", "content": content}
