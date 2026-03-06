"""
DVD Player - English audio with English subtitles.

Launches DVD with English audio and English subtitles.
"""

from Ludarium.DVD import launch_dvd

DISPLAY_NAME = "DVD - Inglés"
DESCRIPTION = "Audio en inglés con subtítulos en inglés"


def launch(joystick=None):
    """Launch DVD with English audio and English subtitles."""
    launch_dvd(joystick=joystick, menu_mode=False, alang="en", slang="en")
