from datetime import datetime




def get_keys_of_interest():
    """
    Revelevants columns to get battery data 
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
    str --> dict: get the data based on the keys in the get_keys_of_interest
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

