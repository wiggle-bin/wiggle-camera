# WiggleCamera

The [WiggleBIn](https://github.com/wiggle-bin/wiggle-bin) recording service for taking pictures.

## Prepare Raspberry PI

Install picamera2 - https://github.com/raspberrypi/picamera2.

Set package venv to have access to system packages

```
python3 -m venv --system-site-packages .venv
```

## Installation

```
pip3 install wiggle-camera
```

## CLI

```
wiggle-camera -h
```

## Prepare Raspberry PI

```
sudo apt-get install libcap-dev
```

## Enable recording service

In the terminal run `wiggle-camera-install`. This will install and start a service which runs `wiggle-camera --record` to take pictures every couple of seconds.

```
wiggle-camera-install
```

## Services

You can check the status with:

```
systemctl --user status wiggle-camera.service
```

To stop the service run:

```
systemctl --user stop wiggle-camera.service
```

To start the service run:

```
systemctl --user start wiggle-camera.service
```

## Installation for development

Updating packages on Raspberry Pi
```
pip install --upgrade pip setuptools wheel
python -m pip install --upgrade pip
```

Installing package
```
pip3 install -e .
```

For installation without dev dependencies
```
pip install --no-dev -r requirements.txt
```