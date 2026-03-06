"""
DVD Player - Spanish audio, no subtitles.

Launches DVD with Spanish audio and subtitles disabled.
"""

from Ludarium.DVD import launch_dvd

DISPLAY_NAME = "DVD - Español"
DESCRIPTION = "Audio en español, sin subtítulos"


def launch(joystick=None):
    """Launch DVD with Spanish audio, no subtitles."""
    launch_dvd(joystick=joystick, menu_mode=False, alang="es", slang="no")
