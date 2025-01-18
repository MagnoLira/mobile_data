import subprocess

# Função para executar comandos ADB e capturar a saída
def run_adb_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        print(f"Erro ao executar comando ADB: {e}")
        return ""

# Função para coletar dados de uso de aplicativos
def get_app_usage():
    output = run_adb_command('adb shell dumpsys usagestats --include-history')
    return output

# Função para coletar informações da bateria
def get_battery_status():
    output = run_adb_command('adb shell dumpsys battery')
    return output
