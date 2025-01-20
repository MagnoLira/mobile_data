from datetime import datetime




def get_keys_of_interest():
    """
    Retorna uma lista de chaves relevantes para o status da bateria.
    """
    return [
        "AC powered", "USB powered", "Wireless powered", "Dock powered",
        "Max charging current", "Max charging voltage", "Charge counter",
        "status", "health", "present", "level", "scale", "voltage",
        "temperature", "technology", "batteryMiscEvent", "batteryCurrentEvent",
        "mSecPlugTypeSummary", "LED Charging", "LED Low Battery", "current now",
        "Adaptive Fast Charging Settings", "Super Fast Charging Settings",
        "FEATURE_WIRELESS_FAST_CHARGER_CONTROL", "mWasUsedWirelessFastChargerPreviously",
        "mWirelessFastChargingSettingsEnable"
    ]
















def parse_battery_status(output):
    """
    Processa a saída do status da bateria do ADB em um dicionário contendo os dados relevantes.
    """
    status = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    keys_of_interest = get_keys_of_interest()

    for line in output.splitlines():
        for key in keys_of_interest:
            if key in line:
                parts = line.split(":")
                if len(parts) == 2:
                    status[key] = parts[1].strip()
    return status

