#!python
import subprocess
import argparse

parser = argparse.ArgumentParser(
    description='Check platform compatibility with Python.')
parser.add_argument('tag', metavar='TAG', help='Version tag to build.')

args = parser.parse_args()
tag = args.tag
sourcetag = tag
targetimage = f'chenio/autodiscover-email-settings:{tag}'

platforms = [
    'linux/amd64', 'linux/arm64', 'linux/riscv64', 'linux/ppc64le',
    'linux/s390x', 'linux/386', 'linux/mips64le', 'linux/mips64',
    'linux/arm/v7', 'linux/arm/v6'
]

compatible_archs = []

for platform in platforms:
    print(f'Try building image {targetimage} for architecture {platform}.')
    proc = subprocess.run([
        'docker', 'buildx', 'build', '-f', 'Dockerfile', '--platform',
        platform, '-t', targetimage, '.'
    ])
    if proc.returncode == 0:
        compatible_archs.append(platform)

print(f'Successful platforms:')
for platform in compatible_archs:
    print(f'\t- {platform}')