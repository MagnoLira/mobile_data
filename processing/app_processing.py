from datetime import datetime







def extract_value(parts, key):
    """
    Extract a specific key in the format 'key=value'.
    """
    return next((p.split('=')[1].replace('"', '') for p in parts if p.startswith(key)), None)


def process_app_usage(output):
    """
    Process the list of output in dict
    """
    app_events = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current Timestamp 

    for line in output.splitlines():
        if "time=" in line and "type=" in line and "package=" in line:
            parts = line.split()
            try:
                timestamp = extract_value(parts, "time=")
                event_type = extract_value(parts, "type=")
                package_name = extract_value(parts, "package=")

                if timestamp and event_type and package_name:
                    app_events.append({
                        "datetime": current_time,
                        "timestamp": timestamp,
                        "event_type": event_type,
                        "package_name": package_name
                    })
            except Exception as e:
                print(f"Error in process: {line}\nDetails: {e}")
                continue
    return app_events

