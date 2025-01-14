import subprocess

def get_battery_history():
    """Colect the historical activity from battery usage via ADB"""
    try:
        result = subprocess.check_output("adb logcat -d | grep 'Battery'", shell=True)
        return result.decode("utf-8")
    except Exception as e:
        return f"Error: {str(e)}"


def get_app_usage_history():
    """Collect the historical activity from general apps usage via ADB"""
    try:
        result = subprocess.check_output("adb shell dumpsys usagestats", shell=True)
        return result.decode("utf-8")
    except Exception as e:
        return f"Error: {str(e)}"
