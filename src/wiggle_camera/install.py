import os
from pathlib import Path

BOOTH_FILE = 'wiggle-camera-record-boot.sh'
SERVICE_FILE = 'wiggle-camera-record.service'

def install():
    scriptFile = Path(__file__).parent / "service" / BOOTH_FILE
    serviceFile = Path(__file__).parent / "service" / SERVICE_FILE
    os.system(f"sudo cp {scriptFile} /usr/bin/{BOOTH_FILE}")
    os.system(f"sudo cp {serviceFile} /etc/systemd/user/{SERVICE_FILE}")
    os.system(f"systemctl --user enable {SERVICE_FILE}")
    os.system(f"systemctl --user start {SERVICE_FILE}")
