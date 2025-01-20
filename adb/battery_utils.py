from adb.adb_utils import run_adb_command

def get_battery_status():
    """
    Collects battery status using ADB.

    Returns:
        str: The raw battery status output from the ADB command.
    """
    output = run_adb_command('adb shell dumpsys battery')
    return output
