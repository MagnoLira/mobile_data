from adb.adb_utils import run_adb_command

def get_app_usage():
    """
    Collects app usage stats using ADB.

    Returns:
        str: The raw usage stats output from the ADB command.
    """
    output = run_adb_command('adb shell dumpsys usagestats --include-history')
    return output
