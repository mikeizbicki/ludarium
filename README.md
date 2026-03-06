# LUDARIUM

A Roman-themed entertainment console interface designed for SNES controller input.

## Features

- Full-screen interface optimized for TV displays
- SNES gamepad navigation (no keyboard/mouse required)
- DVD playback via mpv
- Modular menu system for easy extension

## Requirements

- Python 3.9+
- pygame
- mpv (for DVD playback)
- SNES USB controller

## Installation

```bash
pip install -r requirements.txt
```

For DVD playback, install mpv:

```bash
# Debian/Ubuntu
sudo apt install mpv

# Arch Linux
sudo pacman -S mpv
```

## Usage

```bash
python -m Ludarium
```

Or if installed:

```bash
ludarium
```

## Controls

| Button | Action |
|--------|--------|
| D-Pad Up/Down | Navigate menu |
| A / Start | Select item |
| L + R | Exit to menu / Exit application |

### DVD Controls

| Button | Action |
|--------|--------|
| A / Start | Pause/Play (or select in menu mode) |
| B | Stop and return to menu (or back in menu mode) |
| D-Pad Left/Right | Seek ±10 seconds (or navigate in menu mode) |
| D-Pad Up/Down | Seek ±60 seconds (or navigate in menu mode) |
| Select | Cycle subtitles |
| X | Cycle audio tracks |
| L + R | Exit to menu |

## Adding Menu Items

Create a new Python file in `Ludarium/Menu/` with:

```python
DISPLAY_NAME = "My Item"
DESCRIPTION = "Description shown in menu"

def launch(joystick=None):
    # Your code here
    pass
```

The menu automatically scans for `.py` files in the Menu directory.

## License

MIT
