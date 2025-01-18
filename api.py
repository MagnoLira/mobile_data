from fastapi import FastAPI, HTTPException
from threading import Thread
from main import monitor_data
import os

app = FastAPI()

# Variável para controlar o status do monitoramento
monitoring_thread = None
is_monitoring = False


# Endpoint para verificar o status do monitoramento
@app.get("/status")
def get_status():
    status = "running" if is_monitoring else "stopped"
    return {"status": status}


# Endpoint para iniciar o monitoramento
@app.post("/start")
def start_monitoring():
    global monitoring_thread, is_monitoring
    if is_monitoring:
        raise HTTPException(status_code=400, detail="Monitoramento já está em execução.")
    monitoring_thread = Thread(target=monitor_data, daemon=True)
    monitoring_thread.start()
    is_monitoring = True
    return {"message": "Monitoramento iniciado."}


# Endpoint para parar o monitoramento
@app.post("/stop")
def stop_monitoring():
    global is_monitoring
    if not is_monitoring:
        raise HTTPException(status_code=400, detail="Monitoramento não está em execução.")
    is_monitoring = False
    return {"message": "Monitoramento parado. Reinicie o servidor para finalizar completamente."}


# Endpoint para consultar dados de uso de aplicativos
@app.get("/data/apps")
def get_app_data():
    filepath = "C:/Users/USER/OneDrive/Documentos/portfolio/mobile_data_project/mobile_data/app_usage.csv"
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Dados de aplicativos não encontrados.")
    with open(filepath, "r", encoding="utf-8") as file:
        data = file.readlines()
    return {"data": data[-10:]}  # Retorna as últimas 10 linhas


# Endpoint para consultar dados da bateria
@app.get("/data/battery")
def get_battery_data():
    filepath = "C:/Users/USER/OneDrive/Documentos/portfolio/mobile_data_project/mobile_data/battery_status.csv"
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Dados de bateria não encontrados.")
    with open(filepath, "r", encoding="utf-8") as file:
        data = file.readlines()
    return {"data": data[-10:]}  # Retorna as últimas 10 linhas


# Endpoint para baixar os dados em CSV
@app.get("/download/{data_type}")
def download_data(data_type: str):
    valid_types = {
        "apps": "C:/Users/USER/OneDrive/Documentos/portfolio/mobile_data_project/mobile_data/app_usage.csv",
        "battery": "C:/Users/USER/OneDrive/Documentos/portfolio/mobile_data_project/mobile_data/battery_status.csv",
    }
    if data_type not in valid_types:
        raise HTTPException(status_code=400, detail="Tipo de dado inválido.")
    filepath = valid_types[data_type]
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
    return {"filename": f"{data_type}.csv", "content": content}
