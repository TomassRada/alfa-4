import datetime

def log(message, path):
    """Zapíše log msg do souboru"""
    now = datetime.datetime.now()
    with open(path, 'a') as f:
        f.write(f"{now} - {message}\n")
