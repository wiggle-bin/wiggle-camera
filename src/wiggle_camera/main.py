import argparse
import os
import wiggle_camera.camera as camera
from wiggle_camera.light import off, on, default_brightness

def main():
    parser = argparse.ArgumentParser(
        prog="WiggleCamera", description="Control the camera on WiggleBin"
    )

    camera_group = parser.add_argument_group("camera")
    camera_group.add_argument("--picture", action="store_true", help="take one picture")
    camera_group.add_argument(
        "--recording", action="store_true", help="take multiple picture"
    )

    service = parser.add_argument_group("service")
    service.add_argument(
        "--service",
        const="status",
        nargs="?",
        choices=["stop", "start"],
        help="control wiggler recording",
    )

    light = parser.add_argument_group("light")
    light.add_argument(
        "--light", nargs="?", const=default_brightness, help="light intensity from 0.01 to 1", type=float
    )
    light.add_argument("--light-off", action="store_true", help="turn light off")

    args = parser.parse_args()

    if args.picture:
        camera.picture()
    elif args.recording:
        camera.recording()
    elif args.service:
        os.system(f"systemctl --user {args.service} wiggle-camera-record.service")
        print(f"WiggleCamera recording: {args.service}")
    elif args.light:
        on(args.light)
    elif args.light_off:
        off()


if __name__ == "__main__":
    main()
