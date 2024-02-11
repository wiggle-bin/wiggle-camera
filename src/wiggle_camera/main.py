import argparse
import os
import wiggle_camera.camera as camera


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

    args = parser.parse_args()

    if args.picture:
        camera.picture()
    elif args.recording:
        camera.recording()
    elif args.service:
        os.system(f"systemctl --user {args.service} wiggle-record.service")
        print(f"WiggleCamera recording: {args.service}")


if __name__ == "__main__":
    main()
