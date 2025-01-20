import subprocess

# Exec adb commands 
def run_adb_command(command):
    """
    Executes an ADB command and returns the output.
    
    Args:
        command (str): The ADB command to execute.

    Returns:
        str: The output from the ADB command."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        print(f"Error on abd command: {e}")
        return ""