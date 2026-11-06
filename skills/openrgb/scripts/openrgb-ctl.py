#!/usr/bin/env python3
"""OpenRGB controller helper for system case, motherboard, and RAM lighting."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

PROFILE_DIR = Path.home() / ".config" / "OpenRGB" / "profiles"


def run_openrgb(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["openrgb"] + args, capture_output=True, text=True)


def get_profile_data(name: str) -> dict | None:
    path = PROFILE_DIR / f"{name}.json"
    if not path.is_file():
        return None
    with open(path) as f:
        return json.load(f)


def save_profile_data(name: str, data: dict) -> None:
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    path = PROFILE_DIR / f"{name}.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def hex_to_rgb_int(hex_str: str) -> int:
    hex_str = hex_str.lstrip("#")
    if len(hex_str) != 6:
        raise ValueError(f"Invalid hex color: {hex_str}")
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)
    # OpenRGB internal color packing: (R) | (G << 8) | (B << 16)
    return r | (g << 8) | (b << 16)


def turn_off() -> None:
    # 1. Update/create all-off profile with zeroed LED registers
    data = get_profile_data("all-off")
    if not data:
        # Generate base profile first
        run_openrgb(["-sp", "all-off"])
        data = get_profile_data("all-off")

    if data:
        for ctrl in data.get("controllers", []):
            ctrl["colors"] = [0] * len(ctrl.get("colors", []))
            for m in ctrl.get("modes", []):
                m["brightness"] = 0
                if "colors" in m:
                    m["colors"] = [0] * len(m["colors"])
        save_profile_data("all-off", data)
        run_openrgb(["-p", "all-off"])
    else:
        # Fallback to direct commands
        run_openrgb(["-d", "0", "-m", "Static", "-b", "0", "-c", "000000"])
        run_openrgb(["-d", "1", "-m", "Static", "-b", "0", "-c", "000000"])

    print("All lighting turned OFF (Motherboard, ARGB Case Fans, and RAM).")


def turn_on(color_hex: str = "FFFFFF", brightness: int = 100) -> None:
    color_val = hex_to_rgb_int(color_hex)
    clean_hex = color_hex.lstrip("#").upper()

    # Ensure ARGB zones on MSI board are sized
    run_openrgb(["-d", "1", "-z", "2", "--size", "80", "-z", "3", "--size", "80"])

    # Build profile
    run_openrgb(["-sp", "temp-active"])
    data = get_profile_data("temp-active")
    if data:
        for ctrl in data.get("controllers", []):
            desc = ctrl.get("description", "")
            if "Kingston Fury" in desc:
                ctrl["colors"] = [color_val] * len(ctrl.get("colors", []))
                for m in ctrl.get("modes", []):
                    if m.get("name") == "Static":
                        m["brightness"] = brightness
                        m["colors"] = [color_val]
            elif "MSI" in desc:
                ctrl["active_mode"] = 1  # Static mode
                ctrl["colors"] = [color_val] * len(ctrl.get("colors", []))
                for m in ctrl.get("modes", []):
                    if m.get("name") == "Static":
                        m["brightness"] = brightness
                        m["colors"] = [color_val]
        save_profile_data("temp-active", data)
        run_openrgb(["-p", "temp-active"])
    else:
        run_openrgb(["-m", "Static", "-b", str(brightness), "-c", clean_hex])

    print(f"All lighting turned ON (#{clean_hex} at {brightness}% brightness).")


def set_rainbow() -> None:
    # Ensure ARGB zones sized
    run_openrgb(["-d", "1", "-z", "2", "--size", "80", "-z", "3", "--size", "80"])
    run_openrgb(["-d", "1", "-m", "Rainbow wave"])
    run_openrgb(["-d", "0", "-m", "Rainbow"])
    print("All lighting set to Rainbow effect.")


def show_status() -> None:
    res = run_openrgb(["--list-detailed"])
    print(res.stdout or res.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description="OpenRGB Controller CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("off", help="Turn off all RGB lights")

    on_parser = subparsers.add_parser("on", help="Turn on all lights with a color")
    on_parser.add_argument("color", nargs="?", default="FFFFFF", help="Hex color code (e.g. FFFFFF, 00FFCC)")
    on_parser.add_argument("-b", "--brightness", type=int, default=100, help="Brightness percentage (0-100)")

    subparsers.add_parser("rainbow", help="Set rainbow wave effect on all devices")
    subparsers.add_parser("status", help="Show OpenRGB hardware and mode status")

    args = parser.parse_args()

    if args.command == "off":
        turn_off()
    elif args.command == "on":
        turn_on(args.color, args.brightness)
    elif args.command == "rainbow":
        set_rainbow()
    elif args.command == "status":
        show_status()


if __name__ == "__main__":
    main()
