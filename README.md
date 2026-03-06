# LUDARIUM

A Roman-themed entertainment console interface designed for SNES controller input.

## Features

- Full-screen interface optimized for TV displays
- SNES gamepad navigation (no keyboard/mouse required)
- DVD playback via mplayer
- Modular menu system for easy extension

## Requirements

- Python 3.9+
- pygame
- mplayer (for DVD playback)
- SNES USB controller

## Installation

```bash
pip install -r requirements.txt
```

For DVD playback, install mplayer:

```bash
# Debian/Ubuntu
sudo apt install mplayer

# Arch Linux
sudo pacman -S mplayer
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
| A / Start | Pause/Play |
| B | Stop and return to menu |
| D-Pad Left/Right | Seek ±10 seconds |
| D-Pad Up/Down | Seek ±60 seconds |
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
