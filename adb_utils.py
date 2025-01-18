import subprocess

# Exec adb commands 
def run_adb_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        print(f"Error on abd command: {e}")
        return ""

# Collect info on usage apps - daily 
def get_app_usage():
    output = run_adb_command('adb shell dumpsys usagestats --include-history')
    return output

# Collect battery status
def get_battery_status():
    output = run_adb_command('adb shell dumpsys battery')
    return output
