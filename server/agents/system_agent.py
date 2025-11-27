import platform
import psutil
import datetime

def get_system_status():
    return {
        "status": "online",
        "uptime": str(datetime.datetime.now()), # Simplified uptime
        "platform": platform.system(),
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_percent": psutil.virtual_memory().percent
    }
