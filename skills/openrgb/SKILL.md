---
name: "openrgb"
description: "Control PC case lighting, motherboard RGB headers, and RAM lighting using OpenRGB. Use whenever the user asks to turn on/off, inspect, or change RGB lighting, colors, or effects on PC components."
---

# OpenRGB Skill

Manages PC chassis lighting, motherboard ARGB/RGB headers, and RAM illumination via OpenRGB.

## Hardware Reference (Local System)

* **Motherboard:** MSI PRO B650-S WIFI (`MS-7E26`)
  * **Device ID:** `1`
  * **Controller:** MSI Mystic Light (`/dev/hidraw0`, USB `0db0:0076`)
  * **Zones:**
    * `JRAINBOW1` & `JRAINBOW2` (5V 3-pin ARGB headers → Case fans & ARGB strips)
    * `JRGB1` & `JRGB2` (12V 4-pin RGB headers)
* **RAM:** Kingston Fury DDR5 DRAM
  * **Device ID:** `0`
  * **Controller:** SMBus / I2C at `/dev/i2c-8` address `0x61` (12 LEDs)

---

## Critical Gotchas

1. **ARGB Header Sizing:**
   OpenRGB defaults `JRAINBOW1` and `JRAINBOW2` to 0 LEDs. Case fans will not light up until the zones are resized:
   ```bash
   openrgb -d 1 -z 2 --size 80 -z 3 --size 80
   ```
2. **Kingston Fury DDR5 Black/Off Bug:**
   Setting `--color 000000` via generic CLI without updating individual LED registers leaves the DRAM in Direct mode with decimal `255` (`#0000FF` / Red). To turn the RAM fully off, all 12 individual LED channels and brightness register `&20` must be zeroed (handled automatically by `openrgb-ctl.py off` or loading profile `all-off`).

---

## Quick Helper Tool

An automated CLI helper is located at `scripts/openrgb-ctl.py`:

```bash
# Turn OFF all lights (RAM, case fans, motherboard)
~/.agents/skills/openrgb/scripts/openrgb-ctl.py off

# Turn ON all lights (default: White #FFFFFF)
~/.agents/skills/openrgb/scripts/openrgb-ctl.py on

# Turn ON with specific hex color and brightness
~/.agents/skills/openrgb/scripts/openrgb-ctl.py on 00E5FF -b 80   # Ice Blue at 80%

# Set dynamic Rainbow Wave effect
~/.agents/skills/openrgb/scripts/openrgb-ctl.py rainbow

# Check current devices and modes
~/.agents/skills/openrgb/scripts/openrgb-ctl.py status
```

---

## Direct OpenRGB CLI Commands

```bash
# List devices and modes
openrgb --list-detailed

# Load saved profile
openrgb -p all-off
openrgb -p all-white

# Set motherboard static color (Device 1)
openrgb -d 1 -m Static -b 100 -c FF0000

# Open graphical interface (Wayland / KDE)
openrgb &
```
