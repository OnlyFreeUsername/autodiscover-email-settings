#!/usr/bin/env python3
from argparse import ArgumentParser
from datetime import datetime, timezone
from pathlib import Path
from subprocess import run

DOCKER_CMD = "docker"

parser = ArgumentParser(description="Create custom images.")
parser.add_argument("tags", metavar="TAG", nargs="+", help="Version tags to build.")

args = parser.parse_args()

platforms = [
    "linux/amd64",
    "linux/arm64/v8",
    "linux/s390x",
    "linux/arm/v7",
    "linux/arm/v6",
]


def build(
    image: str,
    directory: Path,
    platforms: list[str],
    build_args: list[tuple[str, str]] | None = None,
):
    if build_args is None:
        build_args = []
    platformlist = ",".join(platforms)
    CMD = [
        DOCKER_CMD,
        "buildx",
        "build",
        "-f",
        "Dockerfile",
        "--push",
        "--pull",
        "--platform",
        platformlist,
        "-t",
        image,
    ]
    for arg, val in build_args:
        CMD.extend(["--build-arg", f"{arg}={val}"])
    CMD.append(str(directory))
    run(CMD, check=True)


def main():
    for tag in args.tags:
        targetimage = f"chenio/autodiscover-email-settings:{tag}"

        print(f"Building image {targetimage}")
        build(
            targetimage,
            Path.cwd(),
            platforms,
            [
                ("TAG", tag),
                ("BUILD_DATE", datetime.now(timezone.utc).isoformat()),
                ("VCS_REF", tag),
            ],
        )

if __name__ == "__main__":
    main()

