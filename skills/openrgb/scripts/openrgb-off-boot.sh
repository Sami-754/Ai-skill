#!/usr/bin/env bash
# Boot-time wrapper: turn off all RGB lighting.
# Runs as root via systemd, but reuses sami's OpenRGB profile location.
set -euo pipefail

export HOME=/home/sami
exec /usr/bin/python3 /home/sami/.agents/skills/openrgb/scripts/openrgb-ctl.py off
