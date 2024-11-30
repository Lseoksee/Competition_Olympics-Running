from datetime import datetime

def Log(*values):
    now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(now, *values)
