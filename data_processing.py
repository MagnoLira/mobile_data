from datetime import datetime

# The ADB`s input is a string 

# Processing apps_usage's string 
def process_app_usage(output):
    app_events = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current Timestamp 

    for line in output.splitlines():
        if "time=" in line and "type=" in line and "package=" in line:
            parts = line.split()
            try:
                timestamp = next((p.split('=')[1].replace('"', '') for p in parts if p.startswith("time=")), None)
                event_type = next((p.split('=')[1] for p in parts if p.startswith("type=")), None)
                package_name = next((p.split('=')[1] for p in parts if p.startswith("package=")), None)
                if timestamp and event_type and package_name:
                    app_events.append({
                        "datetime": current_time,   #interest items 
                        "timestamp": timestamp,
                        "event_type": event_type,
                        "package_name": package_name
                    })
            except Exception as e:
                print(f"Erro ao processar linha: {line}\nDetalhes: {e}")
                continue
    return app_events 

# info battery: {String to Dict} 
def parse_battery_status(output):
    status = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    keys_of_interest = [
        "AC powered", "USB powered", "Wireless powered", "Dock powered",
        "Max charging current", "Max charging voltage", "Charge counter",
        "status", "health", "present", "level", "scale", "voltage",
        "temperature", "technology", "batteryMiscEvent", "batteryCurrentEvent",
        "mSecPlugTypeSummary", "LED Charging", "LED Low Battery", "current now",
        "Adaptive Fast Charging Settings", "Super Fast Charging Settings",
        "FEATURE_WIRELESS_FAST_CHARGER_CONTROL", "mWasUsedWirelessFastChargerPreviously",
        "mWirelessFastChargingSettingsEnable"
    ]
    for line in output.splitlines(): 
        for key in keys_of_interest:
            if key in line:
                parts = line.split(":")
                if len(parts) == 2:
                    status[key] = parts[1].strip()
    return status 
