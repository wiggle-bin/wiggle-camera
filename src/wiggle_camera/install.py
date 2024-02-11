import os
from pathlib import Path


def install():
    scriptFile = Path(__file__).parent / f"service/wiggle-record-boot.sh"
    serviceFile = Path(__file__).parent / f"service/wiggle-record.service"
    os.system(f"sudo cp {scriptFile} /usr/bin/wiggle-record-boot.sh")
    os.system(f"sudo cp {serviceFile} /etc/systemd/user/wiggle-record.service")
    os.system("systemctl --user enable wiggle-record.service")
    os.system("systemctl --user start wiggle-record.service")
