# WiggleCamera

The [WiggleR](https://github.com/wiggle-bin/wiggle-r) recording service for taking pictures.

## Installation

```
pip3 install wiggle-camera
```

## CLI

```
wiggle-camera -h
```

## Enable recording service

In the terminal run `wiggle-camera-install`. This will install and start a service which runs `wiggle-camera --record` to take pictures every couple of seconds.

```
wiggle-camera-install
```

## Services

You can check the status with:

```
systemctl --user status wiggle-record.service
```

To stop the service run:

```
systemctl --user stop wiggle-record.service
```

To start the service run:

```
systemctl --user start wiggle-record.service
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