"""
DVD Player - Menu mode.

Launches DVD to the main menu for manual language/subtitle selection.
"""

from Ludarium.DVD import launch_dvd

DISPLAY_NAME = "DVD - Menú"
DESCRIPTION = "Ir al menú del DVD"


def launch(joystick=None):
    """Launch DVD to the menu."""
    launch_dvd(joystick=joystick, menu_mode=True)
