#!/usr/bin/env python

# Stellar Game Engine - Pygame 1.9
# Copyright (C) 2012, 2013 Julian Marchant <onpon4@lavabit.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Stellar Game Engine - Pygame 1.9

Stellar Game Engine is a library for Stellar.  It is a game engine
loosely based on Game Maker.

Except where otherwise noted, all documented features are required to be
offered by all implementations.  Any implementation failing to do so is
incomplete.

Constants:
    IMPLEMENTATION: A string identifying the how the engine is
        implemented (e.g. the name of the graphics library used).
    ALIGN_LEFT: Flag indicating alignment to the left.
    ALIGN_CENTER: Flag indicating alignment to the horizontal center.
    ALIGN_RIGHT: Flag indicating alignment to the right.
    ALIGN_TOP: Flag indicating alignment to the top.
    ALIGN_MIDDLE: Flag indicating alignment to the vertical middle.
    ALIGN_BOTTOM: Flag indicating alignment to the bottom.
    MOUSE_BUTTON_LEFT: The mouse button number which corresponds with
        the left mouse button.
    MOUSE_BUTTON_RIGHT: The mouse button number which corresponds with
        the right mouse button.
    MOUSE_BUTTON_MIDDLE: The mouse button number which corresponds with
        the middle mouse button.
    MOUSE_BUTTON_WHEEL_UP: The mouse button number which corresponds
        with rolling the mouse wheel up.
    MOUSE_BUTTON_WHEEL_DOWN: The mouse button number which corresponds
        with rolling the mouse wheel down.
    MOUSE_BUTTON_WHEEL_LEFT: The mouse button number which corresponds
        with tilting the mouse wheel to the left.
    MOUSE_BUTTON_WHEEL_RIGHT: The mouse button number which corresponds
        with tilting the mouse wheel to the right.

Global variables:
    game: Stores the current game.  If there is no game currently, this
        variable is set to None.
    image_directories: A list of directories where images can be found.
        Default is ./data/images, ./data/sprites, or ./data/backgrounds.
    font_directories: A list of directories where font files can be
        found.  Default is ./data/fonts.
    sound_directories: A list of directories where sounds can be found.
        Default is ./data/sounds.
    music_directories: A list of directories where music files can be
        found.  Default is ./data/music.

Classes:
    Game: Class which handles the game.
    Sprite: Class used to store images and animations.
    BackgroundLayer: Class used to store a background layer.
    Background: Class used to store parallax-scrolling backgrounds.
    Font: Class used to store and handle fonts.
    Sound: Class used to store and play sound effects.
    Music: Class used to store and play music.
    StellarClass: Class used for game objects.
    Room: Class used for game rooms, e.g. levels.
    View: Class used for views in rooms.

Functions:
    create_object: Create an object in the current room.
    sound_stop_all: Stop playback of all sounds.
    get_key_pressed: Return whether or not a given key is pressed.
    get_mouse_button_pressed: Return whether or not a given mouse
        button is pressed.
    get_joystick_axis: Return the position of the given axis.
    get_joystick_hat: Return the position of the given HAT.
    get_joystick_button_pressed: Return whether or not the given
        joystick button is pressed.
    get_joysticks: Return the number of joysticks available.
    get_joystick_axes: Return the number of axes on the given
        joystick.
    get_joystick_hats: Return the number of HATs on the given
        joystick.
    get_joystick_buttons: Return the number of buttons on the
        given joystick.

Implementation-specific information:
This implementation supports hardware rendering, which can improve
performance in some cases.  It is not enabled by default.  To enable it,
set ``sge.hardware_rendering`` to True.  To get the best performance
with hardware rendering, you should use colorkeys instead of alpha
transparency.

Since Pygame supports trackballs, they are implemented as extra analog
sticks.  Their movement is limited to the range of an analog stick to
ensure full compatibility.  You can disable this limitation by setting
``sge.real_trackballs`` to True.

sge.Sprite supports the following image formats:
    PNG
    JPEG
    Non-animated GIF
    BMP
    PCX
    Uncompressed Truevision TGA
    TIFF
    ILBM
    Netpbm
    X Pixmap

sge.Sound supports the following audio formats:
    Uncompressed WAV
    Ogg Vorbis

sge.Music supports the following audio formats:
    Ogg Vorbis
    MP3 (support limited; use not recommended)
    MOD
    XM
    MIDI

For starting position in MOD files, the pattern order number is used
instead of the number of milliseconds.

If Pygame is built without full image support, sge.Sprite will only
support uncompressed BMP images.  In addition, the pygame.mixer module,
which is used for audio playback, is optional and depends on SDL_mixer;
if pygame.mixer is unavailable, sounds and music will not play.  If you
encounter problems with loading images or playing sounds, check your
build of Pygame.

On some systems, the game will crash if sge.Music attempts to load an
unsupported format.  Since MP3's support is limited, it is best to avoid
using it; consider using Ogg instead.

Balance control is not supported in either sge.Sound or sge.Music.
Sounds and music play through both speakers equally.

sge.Sprite.draw_line supports anti-aliasing for lines with a thickness
of 1 only.  sge.Sprite.draw_text supports anti-aliasing in all cases.
No other drawing functions support anti-aliasing.

"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__version__ = "0.0.49"

import os

import pygame

from .constants import *
from .Game import Game
from .Sprite import Sprite
from .BackgroundLayer import BackgroundLayer
from .Background import Background
from .Font import Font
from .Sound import Sound
from .Music import Music
from .StellarClass import StellarClass, Mouse
from .Room import Room
from .View import View
from .functions import *


__all__ = [
    # Constants
    'IMPLEMENTATION', 'ALIGN_LEFT', 'ALIGN_CENTER', 'ALIGN_RIGHT', 'ALIGN_TOP',
    'ALIGN_MIDDLE', 'ALIGN_BOTTOM', 'MOUSE_BUTTON_LEFT', 'MOUSE_BUTTON_RIGHT',
    'MOUSE_BUTTON_MIDDLE',

    # Classes
    'Game', 'Sprite', 'BackgroundLayer', 'Background', 'Font', 'Sound',
    'Music', 'StellarClass', 'Room', 'View',

    # Functions
    'create_object', 'sound_stop_all', 'music_clear_queue', 'music_stop_all',
    'get_key_pressed', 'get_mouse_button_pressed', 'get_joystick_axis',
    'get_joystick_hat', 'get_joystick_button_pressed', 'get_joysticks',
    'get_joystick_axes', 'get_joystick_hats', 'get_joystick_buttons'
    ]

# Global variables
game = None
image_directories = [os.path.join(PROGRAM_DIR, 'data', 'images'),
                     os.path.join(PROGRAM_DIR, 'data', 'sprites'),
                     os.path.join(PROGRAM_DIR, 'data', 'backgrounds')]
font_directories = [os.path.join(PROGRAM_DIR, 'data', 'fonts')]
sound_directories = [os.path.join(PROGRAM_DIR, 'data', 'sounds')]
music_directories = [os.path.join(PROGRAM_DIR, 'data', 'music')]

hardware_rendering = False
real_trackballs = False
