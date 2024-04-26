import os
from pathlib import Path

SERVICE_FILE = 'wiggle-camera-record.service'

def install():
    serviceFile = Path(__file__).parent / "service" / SERVICE_FILE
    os.system(f"sudo cp {serviceFile} /etc/systemd/user/{SERVICE_FILE}")
    os.system(f"systemctl --user enable {SERVICE_FILE}")
    os.system(f"systemctl --user start {SERVICE_FILE}")
