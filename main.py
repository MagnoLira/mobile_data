import time
from datetime import datetime
from adb_utils import get_app_usage, get_battery_status
from data_processing import process_app_usage, parse_battery_status
from save_utils import save_to_csv


def monitor_data(interval_seconds=600):
    global is_monitoring
    app_usage_file = "C:/Users/USER/OneDrive/Documentos/portfolio/mobile_data_project/mobile_data/app_usage.csv"
    battery_file = "C:/Users/USER/OneDrive/Documentos/portfolio/mobile_data_project/mobile_data/battery_status.csv"
    app_usage_fields = ["datetime", "timestamp", "event_type", "package_name"]

    print("Starting monitoring...")
    while is_monitoring:
        try:
            # Collect apps info
            app_output = get_app_usage()
            app_usage = process_app_usage(app_output)
            save_to_csv(app_usage_file, app_usage, app_usage_fields)

            # Collect battery status
            battery_output = get_battery_status()
            battery_status = parse_battery_status(battery_output)
            save_to_csv(battery_file, battery_status)

            print(f"Data saved at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"Error during monitoring: {e}")
        time.sleep(interval_seconds)
    print("Monitoring ended.")
