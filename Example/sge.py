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

sge.Sprite.draw_line supports anti-aliasing for lines with a thickness
of 1 only.  sge.Sprite.draw_text supports anti-aliasing in all cases.
No other drawing functions support anti-aliasing.

"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__version__ = "0.0.46"

import sys
import os
import math
import weakref

import pygame

__all__ = ['Game', 'Sprite', 'BackgroundLayer', 'Background', 'Font', 'Sound',
           'Music', 'StellarClass', 'Room', 'View', 'game',
           'image_directories', 'font_directories', 'sound_directories',
           'music_directories', 'IMPLEMENTATION', 'ALIGN_LEFT', 'ALIGN_CENTER',
           'ALIGN_RIGHT', 'ALIGN_TOP', 'ALIGN_MIDDLE', 'ALIGN_BOTTOM',
           'MOUSE_BUTTON_LEFT', 'MOUSE_BUTTON_RIGHT', 'MOUSE_BUTTON_MIDDLE',
           'create_object', 'sound_stop_all', 'music_clear_queue',
           'music_stop_all', 'get_key_pressed', 'get_mouse_button_pressed',
           'get_joystick_axis', 'get_joystick_hat',
           'get_joystick_button_pressed', 'get_joysticks', 'get_joystick_axes',
           'get_joystick_hats', 'get_joystick_buttons', 'hardware_rendering',
           'real_trackballs']

PROGRAM_DIR = os.path.dirname(sys.argv[0])

COLORS = {'white': '#ffffff', 'silver': '#c0c0c0', 'gray': '#808080',
          'black': '#000000', 'red': '#ff0000', 'maroon': '#800000',
          'yellow': '#ffff00', 'olive': '#808000', 'lime': '#00ff00',
          'green': '#008000', 'aqua': '#00ffff', 'teal': '#008080',
          'blue': '#0000ff', 'navy': '#000080', 'fuchsia': '#ff00ff',
          'purple': '#800080'}
COLORNAMES = {}
for pair in COLORS.items():
    COLORNAMES[pair[1]] = pair[0]

KEYS = {"0": pygame.K_0, "1": pygame.K_1, "2": pygame.K_2, "3": pygame.K_3,
        "4": pygame.K_4, "5": pygame.K_5, "6": pygame.K_6, "7": pygame.K_7,
        "8": pygame.K_8, "9": pygame.K_9, "a": pygame.K_a, "b": pygame.K_b,
        "c": pygame.K_c, "d": pygame.K_d, "e": pygame.K_e, "f": pygame.K_f,
        "g": pygame.K_g, "h": pygame.K_h, "i": pygame.K_i, "j": pygame.K_j,
        "k": pygame.K_k, "l": pygame.K_l, "m": pygame.K_m, "n": pygame.K_n,
        "o": pygame.K_o, "p": pygame.K_p, "q": pygame.K_q, "r": pygame.K_r,
        "s": pygame.K_s, "t": pygame.K_t, "u": pygame.K_u, "v": pygame.K_v,
        "w": pygame.K_w, "x": pygame.K_x, "y": pygame.K_y, "z": pygame.K_z,
        "alt_left": pygame.K_LALT, "alt_right": pygame.K_RALT,
        "ampersand": pygame.K_AMPERSAND, "apostrophe": pygame.K_QUOTE,
        "asterisk": pygame.K_ASTERISK, "at": pygame.K_AT,
        "backslash": pygame.K_BACKSLASH, "backspace": pygame.K_BACKSPACE,
        "backtick": pygame.K_BACKQUOTE, "bracket_left": pygame.K_LEFTBRACKET,
        "bracket_right": pygame.K_RIGHTBRACKET, "break": pygame.K_BREAK,
        "caps_lock": pygame.K_CAPSLOCK, "caret": pygame.K_CARET,
        "clear": pygame.K_CLEAR, "colon": pygame.K_COLON,
        "comma": pygame.K_COMMA, "ctrl_left": pygame.K_LCTRL,
        "ctrl_right": pygame.K_RCTRL, "delete": pygame.K_DELETE,
        "dollar": pygame.K_DOLLAR, "down": pygame.K_DOWN, "end": pygame.K_END,
        "enter": pygame.K_RETURN, "equals": pygame.K_EQUALS,
        "escape": pygame.K_ESCAPE, "euro": pygame.K_EURO,
        "exclamation": pygame.K_EXCLAIM, "f1": pygame.K_F1, "f2": pygame.K_F2,
        "f3": pygame.K_F3, "f4": pygame.K_F4, "f5": pygame.K_F5,
        "f6": pygame.K_F6, "f7": pygame.K_F7, "f8": pygame.K_F8,
        "f9": pygame.K_F9, "f10": pygame.K_F10, "f11": pygame.K_F11,
        "f12": pygame.K_F12, "greater_than": pygame.K_GREATER,
        "hash": pygame.K_HASH, "help": pygame.K_HELP, "home": pygame.K_HOME,
        "hyphen": pygame.K_MINUS, "insert": pygame.K_INSERT,
        "kp_0": pygame.K_KP0, "kp_1": pygame.K_KP1, "kp_2": pygame.K_KP2,
        "kp_3": pygame.K_KP3, "kp_4": pygame.K_KP4, "kp_5": pygame.K_KP5,
        "kp_6": pygame.K_KP6, "kp_7": pygame.K_KP7, "kp_8": pygame.K_KP8,
        "kp_9": pygame.K_KP9, "kp_divide": pygame.K_KP_DIVIDE,
        "kp_enter": pygame.K_KP_ENTER, "kp_equals": pygame.K_KP_EQUALS,
        "kp_minus": pygame.K_KP_MINUS, "kp_multiply": pygame.K_KP_MULTIPLY,
        "kp_plus": pygame.K_KP_PLUS, "kp_point": pygame.K_KP_PERIOD,
        "left": pygame.K_LEFT, "less_than": pygame.K_LESS,
        "menu": pygame.K_MENU, "meta_left": pygame.K_LMETA,
        "meta_right": pygame.K_RMETA, "mode": pygame.K_MODE,
        "num_lock": pygame.K_NUMLOCK, "pagedown": pygame.K_PAGEDOWN,
        "pageup": pygame.K_PAGEUP, "parenthesis_left": pygame.K_LEFTPAREN,
        "parenthesis_right": pygame.K_RIGHTPAREN, "pause": pygame.K_PAUSE,
        "period": pygame.K_PERIOD, "plus": pygame.K_PLUS,
        "power": pygame.K_POWER, "print_screen": pygame.K_PRINT,
        "question": pygame.K_QUESTION, "quote": pygame.K_QUOTEDBL,
        "right": pygame.K_RIGHT, "scroll_lock": pygame.K_SCROLLOCK,
        "semicolon": pygame.K_SEMICOLON, "shift_left": pygame.K_LSHIFT,
        "shift_right": pygame.K_RSHIFT, "slash": pygame.K_SLASH,
        "space": pygame.K_SPACE, "super_left": pygame.K_LSUPER,
        "super_right": pygame.K_RSUPER, "sysrq": pygame.K_SYSREQ,
        "tab": pygame.K_TAB, "underscore": pygame.K_UNDERSCORE,
        "up": pygame.K_UP}
KEYNAMES = {}
for pair in KEYS.items():
    KEYNAMES[pair[1]] = pair[0]

IMPLEMENTATION = "Pygame 1.9"
ALIGN_LEFT = 2
ALIGN_CENTER = 3
ALIGN_RIGHT = 1
ALIGN_TOP = 8
ALIGN_MIDDLE = 12
ALIGN_BOTTOM = 4
MOUSE_BUTTON_LEFT = 1
MOUSE_BUTTON_RIGHT = 3
MOUSE_BUTTON_MIDDLE = 2
MOUSE_BUTTON_WHEEL_UP = 4
MOUSE_BUTTON_WHEEL_DOWN = 5
MOUSE_BUTTON_WHEEL_LEFT = 6
MOUSE_BUTTON_WHEEL_RIGHT = 7

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


class Game(object):

    """Class which handles the game.

    A Game object must be created before anything else is done.

    All Game objects have the following attributes:
        width: The width of the game's display in pixels.
        height: The height of the game's display in pixels.
        fullscreen: True if the game should be in fullscreen, False
            otherwise.
        scale: A number indicating a fixed scale factor (e.g. 1 for no
            scaling, 2 for doubled size).  If set to 0, scaling is
            automatic (causes the game to fit the window or screen).
        scale_proportional: If set to True, scaling is always
            proportional.  If set to False, the image may be stretched
            to completely fill the game window or screen.  This has no
            effect unless ``scale`` is 0.
        scale_smooth: If set to True, a smooth scaling algorithm will be
            used, if available.  Otherwise, simple scaling (e.g. pixel
            doubling) will always be used.  Support for smooth scaling
            in Stellar Game Engine implementations is optional.  If the
            implementation used does not support smooth scaling, this
            option will always be treated as False.
        fps: The rate the game should run in frames per second.  Note
            that this is only the maximum; if the computer is not fast
            enough, the game may run more slowly.
        delta: If set to True, delta timing will be enabled, which
            adjusts speeds and animation rates if the game cannot run at
            the specified frame rate.
        delta_min: Delta timing can cause the game to be choppy.  This
            setting limits this by pretending that the frame rate is
            never lower than this amount, resulting in the game slowing
            down like normal if it is.
        grab_input: If set to True, all input will be locked into the
            game.

    The following read-only attributes are also available:
        sprites: A dictionary containing all loaded sprites, using their
            names as the keys.
        background_layers: A dictionary containing all loaded background
            layers, using their sprites' names as the keys.
        backgrounds: A dictionary containing all loaded backgrounds,
            using their unique identifiers as the keys.
        fonts: A dictionary containing all loaded fonts, using their
            names as the keys.
        sounds: A dictionary containing all loaded sounds, using their
            file names as the keys.
        music: A dictionary containing all loaded music, using their
            file names as the keys.
        objects: A dictionary containing all StellarClass objects in the
            game, using their unique identifiers as the keys.
        rooms: A list containing all rooms in order of their creation.
        current_room: The Room object which is currently active.
        mouse: A StellarClass object which represents the mouse cursor.
            Its ID is "mouse" and its bounding box is one pixel.
            Speed variables are determined by averaging all mouse
            movement during the last quarter of a second.  Assigning to
            its ``visible`` attribute controls whether or not the mouse
            cursor is shown.  Setting its sprite sets the mouse cursor.

    Game methods:
        start: Start the game at the first room.
        end: Properly end the game.
        pause: Pause the game.
        unpause: Unpause the game.

    Game events are handled by special methods.  The exact timing of
    their calling is implementation-dependent except where otherwise
    noted.  The methods are:
        event_game_start: Called when the game starts.  This is only
            called once (it is not called again when the game restarts)
            and it is always the first event method called.
        event_step: Called once each frame.
        event_key_press: Key press event.
        event_key_release: Key release event.
        event_mouse_move: Mouse move event.
        event_mouse_button_press: Mouse button press event.
        event_mouse_button_release: Mouse button release event.
        event_joystick_axis_move: Joystick axis move event.
        event_joystick_hat_move: Joystick HAT move event.
        event_joystick_button_press: Joystick button press event.
        event_joystick_button_release: Joystick button release event.
        event_close: Close event (e.g. close button).  It is always
            called after any room close events occurring at the same
            time.
        event_mouse_collision: Middle/default mouse collision event.
        event_mouse_collision_left: Left mouse collision event.
        event_mouse_collision_right: Right mouse collision event.
        event_mouse_collision_top: Top mouse collision event.
        event_mouse_collision_bottom: Bottom mouse collision event.
        event_game_end: Called when the game ends.  This is only called
            once and it is always the last event method called.

    The following alternative events are executed when the game is
    paused in place of the corresponding normal events:
        event_paused_key_press
        event_paused_key_release
        event_paused_mouse_move
        event_paused_mouse_button_press
        event_paused_mouse_button_release
        event_paused_joystick_axis_move
        event_paused_joystick_hat_move
        event_paused_joystick_button_press
        event_paused_joystick_button_release
        event_paused_close

    """

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value != self._width:
            self._width = value
            self._set_mode()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value != self._height:
            self._height = value
            self._set_mode()

    @property
    def fullscreen(self):
        return self._fullscreen

    @fullscreen.setter
    def fullscreen(self, value):
        if value != self._fullscreen:
            self._fullscreen = value
            self._set_mode()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        if value != self._scale:
            self._scale = value
            self._set_mode()

    @property
    def scale_proportional(self):
        return self._scale_proportional

    @scale_proportional.setter
    def scale_proportional(self, value):
        if value != self._scale_proportional:
            self._scale_proportional = value
            self._set_mode()

    @property
    def scale_smooth(self):
        return self._scale_smooth

    @scale_smooth.setter
    def scale_smooth(self, value):
        if value != self._scale_smooth:
            self._scale_smooth = value
            self._set_mode()

    @property
    def grab_input(self):
        return pygame.event.get_grab()

    @grab_input.setter
    def grab_input(self, value):
        pygame.event.set_grab(value)

    def __init__(self, width=640, height=480, fullscreen=False, scale=0,
                 scale_proportional=True, scale_smooth=False, fps=60,
                 delta=False, delta_min=15, grab_input=False):
        """Create a new Game object and assign it to ``game``.

        Arguments set the properties of the game.  See Game.__doc__ for
        more information.

        """
        # Settings use CD quality and a smaller buffer size for less lag.
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        pygame.init()

        global game
        game = self

        self._width = width
        self._height = height
        self._window_width = width
        self._window_height = height
        self._fullscreen = fullscreen
        self._scale = scale
        self._scale_proportional = scale_proportional
        self._scale_smooth = scale_smooth
        self.fps = fps
        self.delta = delta
        self.delta_min = delta_min

        self.sprites = {}
        self.background_layers = {}
        self.backgrounds = {}
        self.fonts = {}
        self.sounds = {}
        self.music = {}
        self.objects = {}
        self.rooms = []
        self.current_room = None

        self._set_mode()

        self._background_changed = False
        self._colliders = []
        self._music = None
        self._music_queue = []
        self._running = False
        self._clock = pygame.time.Clock()
        self._joysticks = []
        self._pygame_sprites = pygame.sprite.LayeredDirty()
        self.mouse = Mouse()

        # Setup sound channels
        self._available_channels = []
        if pygame.mixer.get_init():
            for i in xrange(pygame.mixer.get_num_channels()):
                self._available_channels.append(pygame.mixer.Channel(i))

        # Setup joysticks
        if pygame.joystick.get_init():
            for i in xrange(pygame.joystick.get_count()):
                joy = pygame.joystick.Joystick(i)
                joy.init()
                self._joysticks.append(joy)

        if not pygame.font.get_init():
            global Font
            Font = _FakeFont

    def start(self):
        """Start the game at the first room.

        Can be called in the middle of a game to start the game over.
        If you do this, everything will be reset to its original state.

        """
        if self._running:
            for room in self.rooms:
                room._reset()

            self.rooms[0].start()
        else:
            self._running = True
            self._background_changed = True
            self.event_game_start()
            self.rooms[0].start()
            background = None
            numviews = 0
            self._clock.tick()

            while self._running:
                # Pygame events
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        k = KEYNAMES[event.key]
                        self.event_key_press(k)
                        self.current_room.event_key_press(k)
                        for obj in self.current_room.objects:
                            obj.event_key_press(k)
                    elif event.type == pygame.KEYUP:
                        k = KEYNAMES[event.key]
                        self.event_key_release(k)
                        self.current_room.event_key_release(k)
                        for obj in self.current_room.objects:
                            obj.event_key_release(k)
                    elif event.type == pygame.MOUSEMOTION:
                        mx, my = event.pos
                        self.mouse.mouse_x = mx - self._x
                        self.mouse.mouse_y = my - self._y
                        self.event_mouse_move(*event.rel)
                        self.current_room.event_mouse_move(*event.rel)
                        for obj in self.current_room.objects:
                            obj.event_mouse_move(*event.rel)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.event_mouse_button_press(event.button)
                        self.current_room.event_mouse_button_press(
                            event.button)
                        for obj in self.current_room.objects:
                            obj.event_mouse_button_press(event.button)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.event_mouse_button_release(event.button)
                        self.current_room.event_mouse_button_release(
                            event.button)
                        for obj in self.current_room.objects:
                            obj.event_mouse_button_release(event.button)
                    elif event.type == pygame.JOYAXISMOTION:
                        self.event_joystick_axis_move(event.joy, event.axis,
                                                      event.value)
                        self.current_room.event_joystick_axis_move(
                            event.joy, event.axis, event.value)
                        for obj in self.current_room.objects:
                            obj.event_joystick_axis_move(event.joy, event.axis,
                                                         event.value)
                    elif event.type == pygame.JOYBALLMOTION:
                        # Limited support for trackballs by pretending
                        # they're axes.  Since they're acting like axes,
                        # they must be in the range [-1,1] unless the
                        # special variable real_trackballs is True.
                        n = (self._joysticks[event.joy].get_numaxes() +
                             2 * event.ball)
                        
                        if real_trackballs:
                            xvalue = event.rel[0]
                            yvalue = event.rel[1]
                        else:
                            xvalue = min(max(-1, event.rel[0]), 1)
                            yvalue = min(max(-1, event.rel[1]), 1)

                        # x-axis
                        self.event_joystick_axis_move(event.joy, n, xvalue)
                        self.current_room.event_joystick_axis_move(
                            event.joy, n, xvalue)
                        for obj in self.current_room.objects:
                            obj.event_joystick_axis_move(event.joy, n, xvalue)
                        
                        # y-axis
                        self.event_joystick_axis_move(event.joy, n + 1, yvalue)
                        self.current_room.event_joystick_axis_move(
                            event.joy, n + 1, yvalue)
                        for obj in self.current_room.objects:
                            obj.event_joystick_axis_move(event.joy, n + 1,
                                                         yvalue)
                    elif event.type == pygame.JOYHATMOTION:
                        self.event_joystick_hat_move(event.joy, event.hat,
                                                     *event.value)
                        self.current_room.event_joystick_hat_move(
                            event.joy, event.hat, *event.value)
                        for obj in self.current_room.objects:
                            obj.event_joystick_hat_move(event.joy, event.hat,
                                                        *event.value)
                    elif event.type == pygame.JOYBUTTONDOWN:
                        self.event_joystick_button_press(event.joy,
                                                         event.button)
                        self.current_room.event_joystick_button_press(
                            event.joy, event.button)
                        for obj in self.current_room.objects:
                            obj.event_joystick_button_press(event.joy,
                                                            event.button)
                    elif event.type == pygame.JOYBUTTONUP:
                        self.event_joystick_button_release(event.joy,
                                                           event.button)
                        self.current_room.event_joystick_button_release(
                            event.joy, event.button)
                        for obj in self.current_room.objects:
                            obj.event_joystick_button_release(event.joy,
                                                              event.button)
                    elif event.type == pygame.QUIT:
                        self.current_room.event_close()
                        self.event_close()
                    elif event.type == pygame.VIDEORESIZE:
                        self._window_width = event.w
                        self._window_height = event.h
                        self._set_mode()
                        self._background_changed = True

                real_time_passed = self._clock.tick(self.fps)

                if self.delta:
                    time_passed = min(real_time_passed, 1000 / self.delta_min)
                    delta_mult = time_passed / (1000 / self.fps)
                else:
                    time_passed = 1000 / self.fps
                    delta_mult = 1

                # Step events
                self.event_step(real_time_passed)
                self.current_room.event_step(real_time_passed)

                # Update background layers
                for i in self.background_layers:
                    self.background_layers[i]._update(time_passed)

                # Update objects (including mouse)
                for obj in self.current_room.objects:
                    obj._update(time_passed, delta_mult)
                    obj.event_step(real_time_passed)

                # Music control
                if self._music is not None:
                    if pygame.mixer.music.get_busy():
                        time_played = pygame.mixer.music.get_pos()
                        fade_time = self._music._fade_time
                        timeout = self._music._timeout

                        if fade_time:
                            real_volume = self._music.volume / 100
                            if time_played < fade_time:
                                volume = real_volume * time_played / fade_time
                                pygame.mixer.music.set_volume(volume)
                            else:
                                pygame.mixer.music.set_volume(real_volume)

                        if timeout and time_played >= timeout:
                            self._music.stop()
                            
                    elif self._music_queue:
                        music = self._music_queue.pop(0)
                        music[0].play(*music[1:])

                if numviews != len(self.current_room.views):
                    numviews = len(self.current_room.views)
                    self._background_changed = True

                # Redraw
                if self._background_changed or background is None:
                    w = max(1, self._window.get_width())
                    h = max(1, self._window.get_height())
                    background = pygame.Surface((w, h))
                    b = self.current_room.background._get_background()
                    background.blit(b, (self._x, self._y))
                    self._window.blit(background, (0, 0))
                    self._background_changed = False
                    self._pygame_sprites.clear(self._window, background)
                    for sprite in self._pygame_sprites:
                        sprite.rect = pygame.Rect(0, 0, 1, 1)
                        sprite.image = pygame.Surface((1, 1))
                        sprite.image.set_colorkey((0, 0, 0))
                    self._pygame_sprites.update()
                    self._pygame_sprites.draw(self._window)
                    dirty = [self._window.get_rect()]
                else:
                    self._pygame_sprites.clear(self._window, background)
                    self._pygame_sprites.update()
                    dirty = self._pygame_sprites.draw(self._window)

                top_bar = pygame.Rect(0, 0, w, self._y)
                bottom_bar = pygame.Rect(0, h - self._y, w, self._y)
                left_bar = pygame.Rect(0, 0, self._x, h)
                right_bar = pygame.Rect(w - self._x, 0, self._x, h)
                if top_bar.h > 0:
                    self._window.fill((0, 0, 0), top_bar)
                    dirty.append(top_bar)
                if bottom_bar.h > 0:
                    self._window.fill((0, 0, 0), bottom_bar)
                    dirty.append(bottom_bar)
                if left_bar.w > 0:
                    self._window.fill((0, 0, 0), left_bar)
                    dirty.append(left_bar)
                if right_bar.w > 0:
                    self._window.fill((0, 0, 0), right_bar)
                    dirty.append(right_bar)

                if hardware_rendering:
                    pygame.display.flip()
                else:
                    pygame.display.update(dirty)

            self.event_game_end()
            pygame.quit()
            global game
            game = None

    def end(self):
        """Properly end the game."""
        self._running = False

    def pause(self, sprite=None):
        """Pause the game.

        ``sprite`` is the sprite to show when the game is paused.  If
        set to None, a default image will be shown.  The default image
        is at the discretion of the Stellar Game Engine implementation,
        as are any additional visual effects, with the stipulation that
        the following conditions are met:

            1. The default image must unambiguously demonstrate that the
                game is paused (the easiest way to do this is to include
                the word "paused" somewhere in the image).
            2. The view must stay in place.
            3. What was going on within the view before the game was
                paused must remain visible while the game is paused.

        While the game is paused, all game events will be halted.
        Events whose names start with "event_paused_" will occur during
        this time instead.

        """
        if sprite is not None:
            image = sprite._get_image(0)
        else:
            try:
                image = pygame.image.load(
                    os.path.join(os.path.dirname(__file__),
                                 'sge_pause.png')).convert()
                image.set_colorkey((255, 0, 255))
            except pygame.error:
                image = pygame.Surface((16, 16))
                image.fill((255, 255, 255), pygame.Rect(0, 0, 4, 16))
                image.fill((255, 255, 255), pygame.Rect(12, 0, 4, 16))
                image.set_colorkey((0, 0, 0))

        rect = image.get_rect(center=self._window.get_rect().center)

        self._paused = True
        screenshot = self._window.copy()
        background = screenshot.copy()
        dimmer = pygame.Surface(self._window.get_size(), pygame.SRCALPHA)
        dimmer.fill(pygame.Color(0, 0, 0, 128))
        background.blit(dimmer, (0, 0))
        background.blit(image, rect)
        orig_screenshot = screenshot
        orig_background = background
        self._clock.tick()

        while self._paused and self._running:
            # Events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    k = KEYNAMES[event.key]
                    self.event_paused_key_press(k)
                    self.current_room.event_paused_key_press(k)
                    for obj in self.current_room.objects:
                        obj.event_paused_key_press(k)
                elif event.type == pygame.KEYUP:
                    k = KEYNAMES[event.key]
                    self.event_paused_key_release(k)
                    self.current_room.event_paused_key_release(k)
                    for obj in self.current_room.objects:
                        obj.event_paused_key_release(k)
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse.mouse_x, self.mouse.mouse_y = event.pos
                    self.event_paused_mouse_move(*event.rel)
                    self.current_room.event_paused_mouse_move(*event.rel)
                    for obj in self.current_room.objects:
                        obj.event_paused_mouse_move(*event.rel)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.event_paused_mouse_button_press(event.button)
                    self.current_room.event_paused_mouse_button_press(
                        event.button)
                    for obj in self.current_room.objects:
                        obj.event_paused_mouse_button_press(event.button)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.event_paused_mouse_button_release(event.button)
                    self.current_room.event_paused_mouse_button_release(
                        event.button)
                    for obj in self.current_room.objects:
                        obj.event_paused_mouse_button_release(event.button)
                elif event.type == pygame.JOYAXISMOTION:
                    self.event_paused_joystick_axis_move(event.joy, event.axis,
                                                         event.value)
                    self.current_room.event_paused_joystick_axis_move(
                        event.joy, event.axis, event.value)
                    for obj in self.current_room.objects:
                        obj.event_paused_joystick_axis_move(
                            event.joy, event.axis, event.value)
                elif event.type == pygame.JOYBALLMOTION:
                    # Limited support for trackballs by pretending
                    # they're axes.  Since they're acting like axes,
                    # they must be in the range [-1,1] unless the
                    # special variable real_trackballs is True.
                    n = (self._joysticks[event.joy].get_numaxes() +
                         2 * event.ball)

                    if real_trackballs:
                        xvalue = event.rel[0]
                        yvalue = event.rel[1]
                    else:
                        xvalue = min(max(-1, event.rel[0]), 1)
                        yvalue = min(max(-1, event.rel[1]), 1)

                    # x-axis
                    self.event_paused_joystick_axis_move(event.joy, n,
                                                         xvalue)
                    self.current_room.event_paused_joystick_axis_move(
                        event.joy, n, xvalue)
                    for obj in self.current_room.objects:
                        obj.event_paused_joystick_axis_move(event.joy, n,
                                                            xvalue)

                    # y-axis
                    self.event_paused_joystick_axis_move(event.joy, n + 1,
                                                         yvalue)
                    self.current_room.event_paused_joystick_axis_move(
                        event.joy, n + 1, yvalue)
                    for obj in self.current_room.objects:
                        obj.event_paused_joystick_axis_move(
                            event.joy, n + 1, yvalue)
                elif event.type == pygame.JOYHATMOTION:
                    self.event_paused_joystick_hat_move(event.joy, event.hat,
                                                        *event.value)
                    self.current_room.event_paused_joystick_hat_move(
                        event.joy, event.hat, *event.value)
                    for obj in self.current_room.objects:
                        obj.event_paused_joystick_hat_move(
                            event.joy, event.hat, *event.value)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.event_paused_joystick_button_press(event.joy,
                                                            event.button)
                    self.current_room.event_paused_joystick_button_press(
                        event.joy, event.button)
                    for obj in self.current_room.objects:
                        obj.event_paused_joystick_button_press(event.joy,
                                                               event.button)
                elif event.type == pygame.JOYBUTTONUP:
                    self.event_paused_joystick_button_release(event.joy,
                                                              event.button)
                    self.current_room.event_paused_joystick_button_release(
                        event.joy, event.button)
                    for obj in self.current_room.objects:
                        obj.event_paused_joystick_button_release(event.joy,
                                                                 event.button)
                elif event.type == pygame.QUIT:
                    self.current_room.event_paused_close()
                    self.event_paused_close()
                elif event.type == pygame.VIDEORESIZE:
                    self._window_width = event.w
                    self._window_height = event.h
                    self._set_mode()
                    self._background_changed = True
                    screenshot = pygame.transform.scale(orig_screenshot,
                                                        (event.w, event.h))
                    background = pygame.transform.scale(orig_background,
                                                        (event.w, event.h))

            # Time management
            self._clock.tick(self.fps)
            
            # Redraw
            self._window.blit(background, (0, 0))

            if hardware_rendering:
                pygame.display.flip()
            else:
                pygame.display.update()

        # Restore the look of the screen from before it was paused
        self._window.blit(screenshot, (0, 0))
        pygame.display.update()
        self._background_changed = True

    def unpause(self):
        """Unpause the game."""
        self._paused = False

    def event_game_start(self):
        """Game start event.

        Called when the game starts.  This is only called once (it is
        not called again when the game restarts) and it is always the
        first event method called.

        """
        pass

    def event_step(self, time_passed):
        """Global step event.

        Called once each frame.  ``time_passed`` is the number of
        milliseconds that have passed during the last frame.

        """
        pass

    def event_key_press(self, key):
        """Key press event.

        ``key`` is the key that was pressed.

        """
        pass

    def event_key_release(self, key):
        """Key release event.

        ``key`` is the key that was pressed.

        """
        pass

    def event_mouse_move(self, x, y):
        """Mouse move event.

        ``x`` and ``y`` indicate the relative movement of the mouse.

        """
        pass

    def event_mouse_button_press(self, button):
        """Mouse button press event.

        ``button`` is the number of the mouse button that was pressed;
        these numbers may vary by implementation, so MOUSE_BUTTON_*
        constants should be used.

        """
        pass

    def event_mouse_button_release(self, button):
        """Mouse button release event.

        ``button`` is the number of the mouse button that was released;
        these numbers may vary by implementation, so MOUSE_BUTTON_*
        constants should be used.

        """
        pass

    def event_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``axis`` is the number of the axis, where 0 is the
        first axis.  ``value`` is the tilt of the axis, where 0 is in
        the center, -1 is tilted all the way to the left or up, and 1 is
        tilted all the way to the right or down.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``hat`` is the number of the HAT, where 0 is the
        first HAT.  ``x`` and ``y`` indicate the position of the HAT,
        where 0 is in the center, -1 is left or up, and 1 is right or
        down.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_joystick_button_press(self, joystick, button):
        """Joystick button press event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``button`` is the number of the button pressed, where
        0 is the first button.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_joystick_button_release(self, joystick, button):
        """Joystick button release event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``button`` is the number of the button pressed, where
        0 is the first button.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_close(self):
        """Close event (e.g. close button).

        It is always called after any room close events occurring at the
        same time.

        """
        pass

    def event_mouse_collision(self, other):
        """Middle/default mouse collision event."""
        pass

    def event_mouse_collision_left(self, other):
        """Left mouse collision event."""
        self.event_mouse_collision(other)

    def event_mouse_collision_right(self, other):
        """Right mouse collision event."""
        self.event_mouse_collision(other)

    def event_mouse_collision_top(self, other):
        """Top mouse collision event."""
        self.event_mouse_collision(other)

    def event_mouse_collision_bottom(self, other):
        """Bottom mouse collision event."""
        self.event_mouse_collision(other)

    def event_game_end(self):
        """Game end event.

        Called when the game ends.  This is only called once and it is
        always the last event method called.

        """
        pass

    def event_paused_key_press(self, key):
        """Key press event when paused.

        See Game.event_key_press.__doc__ for more information.

        """
        pass

    def event_paused_key_release(self, key):
        """Key release event when paused.

        See Game.event_key_release.__doc__ for more information.

        """
        pass

    def event_paused_mouse_move(self, x, y):
        """Mouse move event when paused.

        See Game.event_mouse_move.__doc__ for more information.

        """
        pass

    def event_paused_mouse_button_press(self, button):
        """Mouse button press event when paused.

        See Game.event_mouse_button_press.__doc__ for more information.

        """
        pass

    def event_paused_mouse_button_release(self, button):
        """Mouse button release event when paused.

        See Game.event_mouse_button_release.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event when paused.

        See Game.event_joystick_axis_move.__doc__ for more information.

        """
        pass

    def event_paused_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event when paused.

        See Game.event_joystick_hat_move.__doc__ for more information.

        """
        pass

    def event_paused_joystick_button_press(self, joystick, button):
        """Joystick button press event when paused.

        See Game.event_joystick_button_press.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_button_release(self, joystick, button):
        """Joystick button release event when paused.

        See Game.event_joystick_button_release.__doc__ for more
        information.

        """
        pass

    def event_paused_close(self):
        """Close event (e.g. close button) when paused.

        See Game.event_close.__doc__ for more information.

        """
        pass

    def _set_mode(self):
        # Set the mode of the screen based on self.width, self.height,
        # and self.fullscreen.
        info = pygame.display.Info()

        if self.scale != 0:
            self._xscale = self.scale
            self._yscale = self.scale

        if self.fullscreen or not info.wm:
            flags = pygame.FULLSCREEN
            if hardware_rendering:
                flags |= pygame.HWSURFACE | pygame.DOUBLEBUF

            self._window = pygame.display.set_mode((0, 0), flags)

            if self.scale == 0:
                self._xscale = info.current_w / self.width
                self._yscale = info.current_h / self.height

                if self.scale_proportional:
                    self._xscale = min(self._xscale, self._yscale)
                    self._yscale = self._xscale

            w = max(1, self._window.get_width())
            h = max(1, self._window.get_height())
            self._x = int(round((w - int(round(self.width * self._xscale))) /
                                2))
            self._y = int(round((h - int(round(self.height * self._yscale))) /
                                2))
        else:
            self._x = 0
            self._y = 0
            # Decide window size
            if self.scale == 0:
                self._xscale = self._window_width / self.width
                self._yscale = self._window_height / self.height

                if self.scale_proportional:
                    self._xscale = min(self._xscale, self._yscale)
                    self._yscale = self._xscale

            flags = pygame.RESIZABLE
            if hardware_rendering:
                flags |= pygame.HWSURFACE | pygame.DOUBLEBUF

            #self._window = pygame.display.set_mode(
            #    (int(round(self.width * self._xscale)),
            #     int(round(self.height * self._yscale))), flags)
            self._window = pygame.display.set_mode(
                (self._window_width, self._window_height), flags)

            w = max(1, self._window.get_width())
            h = max(1, self._window.get_height())
            self._x = int(round((w - int(round(self.width * self._xscale))) /
                                2))
            self._y = int(round((h - int(round(self.height * self._yscale))) /
                                2))

        # Refresh sprites
        for s in self.sprites:
            self.sprites[s]._refresh()

    def _get_channel(self):
        # Return a channel for a sound effect to use.
        assert pygame.mixer.get_init()

        if not self._available_channels:
            self._add_channels()

        return self._available_channels.pop(0)

    def _release_channel(self, channel):
        # Release the given channel for other sounds to use.
        assert pygame.mixer.get_init()
        self._available_channels.append(channel)

    def _add_channels(self):
        # Add four channels for playing sounds.
        assert pygame.mixer.get_init()

        old_num_channels = pygame.mixer.get_num_channels()
        new_num_channels = old_num_channels + 4
        pygame.mixer.set_num_channels(new_num_channels)

        for i in xrange(old_num_channels, new_num_channels):
            self._available_channels.append(pygame.mixer.Channel(i))


class Sprite(object):

    """Class which holds information for images and animations.

    All Sprite objects have the following attributes:
        width: The width of the sprite in pixels.
        height: The height of the sprite in pixels.
        origin_x: The horizontal location of the origin (the pixel
            position in relation to the images to base rendering on),
            where the left edge of the image is 0 and origin_x increases
            toward the right.
        origin_y: The vertical location of the origin (the pixel
            position in relation to the images to base rendering on),
            where the top edge of the image is 0 and origin_y increases
            toward the bottom.
        transparent: True if the image should support transparency,
            False otherwise.  If the image does not have an alpha
            channel or if the implementation used does not support alpha
            transparency, a colorkey will be used, with the transparent
            color being the color of the top-rightmost pixel.
        fps: The suggested rate in frames per second to animate the
            image at.
        bbox_x: The horizontal location of the top-left corner of the
            suggested bounding box to use with this sprite, where
            origin_x is 0 and bbox_x increases toward the right.
        bbox_y: The vertical location of the top-left corner of the
            suggested bounding box to use with this sprite, where
            origin_y is 0 and bbox_y increases toward the bottom.
        bbox_width: The width of the suggested bounding box in pixels.
        bbox_height: The height of the suggested bounding box in pixels.

    The following read-only attributes are also available:
        name: The name of the sprite given when it was created.  See
            Sprite.__init__.__doc__ for more information.

    Sprite methods:
        draw_dot: Draw a single-pixel dot.
        draw_line: Draw a line segment between the given points.
        draw_rectangle: Draw a rectangle at the given position.
        draw_ellipse: Draw an ellipse at the given position.
        draw_circle: Draw a circle at the given position.
        draw_text: Draw the given text at the given position.
        draw_clear: Erase everything from the sprite.

    """

    @property
    def width(self):
        return self._w

    @width.setter
    def width(self, value):
        if self._w != value:
            self._w = value
            self.refresh()

    @property
    def height(self):
        return self._h

    @height.setter
    def height(self, value):
        if self._h != value:
            self._h = value
            self._refresh()

    @property
    def transparent(self):
        return self._transparent

    @transparent.setter
    def transparent(self, value):
        if self._transparent != value:
            self._transparent = value
            self._refresh()

    def __init__(self, name=None, width=None, height=None, origin_x=0,
                 origin_y=0, transparent=True, fps=60, bbox_x=0, bbox_y=0,
                 bbox_width=None, bbox_height=None):
        """Create a new Sprite object.

        ``name`` indicates the base name of the image files.  Files are
        to be located in one of the directories specified in
        ``image_directories``.  If a file with the exact name plus image
        file extensions is not available, numbered images will be
        searched for which have names with one of the following formats,
        where "name" is replaced with the specified base file name and
        "0" can be replaced with any integer:

            name-0
            name_0

        If images are found with names like those, all such images will
        be loaded and become frames of animation.  If not, sprite sheets
        will be searched for which have names with one of the following
        formats, where "name" is replaced with the specified base file
        name and "2" can be replaced with any integer:

            name-strip2
            name_strip2

        The number indicates the number of animation frames in the
        sprite sheet. The sprite sheet will be read like a horizontal
        reel, with the first frame on the far left and the last frame on
        the far right, and no space in between frames.

        ``name`` can also be None, in which case the sprite will be a
        transparent rectangle at the specified size (with both ``width``
        and ``height`` defaulting to 32 if they are set to None).  The
        implementation decides what to assign to the sprite's ``name``
        attribute, but it is always a string.

        If no image is found based on any of the above methods and
        ``name`` is not None, IOError will be raised.

        If ``width`` or ``height`` is set to None, the respective size
        will be taken from the largest animation frame.  If
        ``bbox_width`` or ``bbox_height`` is set to None, the respective
        size will be the respective size of the sprite.

        All remaining arguments set the initial properties of the
        sprite; see Sprite.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        print('Creating sprite "{0}"'.format(name))
        self.name = name

        self._transparent = None
        self._baseimages = []
        self._images = []
        self._masks = {}

        fname_single = None
        fname_frames = []
        fname_strip = None

        print("Current image directories:")
        for d in image_directories:
            print(os.path.normpath(os.path.abspath(d)))

        if name is not None:
            for path in image_directories:
                if os.path.isdir(path):
                    fnames = os.listdir(path)
                    for fname in fnames:
                        full_fname = os.path.join(path, fname)
                        if fname.startswith(name) and os.path.isfile(full_fname):
                            root, ext = os.path.splitext(fname)
                            if root.rsplit('-', 1)[0] == name:
                                split = root.rsplit('-', 1)
                            elif root.split('_', 1)[0] == name:
                                split = root.rsplit('_', 1)
                            else:
                                split = (name, '')

                            if root == name:
                                fname_single = full_fname
                            elif split[1].isdigit():
                                n = int(split[1])
                                while len(fname_frames) - 1 < n:
                                    fname_frames.append(None)
                                fname_frames[n] = full_fname
                            elif (split[1].startswith('strip') and
                                  split[1][5:].isdigit()):
                                fname_strip = full_fname

            if fname_single:
                # Load the single image
                try:
                    img = pygame.image.load(fname_single)
                    self._baseimages.append(img)
                except pygame.error:
                    print("Ignored {0}; not a valid image.".format(fname_single))

            if not self._baseimages and any(fname_frames):
                # Load the multiple images
                for fname in fname_frames:
                    if fname:
                        try:
                            self._baseimages.append(pygame.image.load(fname))
                        except pygame.error:
                            print("Ignored {0}; not a valid image.".format(fname))

            if not self._baseimages and fname_strip:
                # Load the strip (sprite sheet)
                root, ext = os.path.splitext(os.path.basename(fname_strip))
                assert '-' in root or '_' in root
                assert (root.rsplit('-', 1)[0] == name or
                        root.rsplit('_', 1)[0] == name)
                if root.rsplit('-', 1)[0] == name:
                    split = root.rsplit('-', 1)
                else:
                    split = root.rsplit('_', 1)

                try:
                    sheet = pygame.image.load(fname_strip)
                    assert split[1][5:].isdigit()
                    n = int(split[1][5:])

                    img_w = max(1, sheet.get_width()) // n
                    img_h = max(1, sheet.get_height())
                    for x in xrange(0, img_w * n, img_w):
                        rect = pygame.Rect(x, 0, img_w, img_h)
                        img = sheet.subsurface(rect)
                        self._baseimages.append(img)
                except pygame.error:
                    print("Ignored {0}; not a valid image.".format(fname_strip))

            if not self._baseimages:
                msg = 'Files for sprite name "{0}" not found.'.format(name)
                raise IOError(msg)
        else:
            # Name is None; default to a blank rectangle.
            if width is None:
                width = 32
            if height is None:
                height = 32

            # Choose name
            prefix = "sge-pygame-dynamicsprite"
            i = 0
            while "{0}_{1}N".format(prefix, i) in game.sprites:
                i += 1
            self.name = "{0}_{1}N".format(prefix, i)

            img = pygame.Surface((width, height), pygame.SRCALPHA)
            img.fill(pygame.Color(0, 0, 0, 0))
            self._baseimages.append(img)
            print("renamed to {0}".format(self.name))

        if width is None:
            width = 1
            for image in self._baseimages:
                width = max(width, image.get_width())

        if height is None:
            height = 1
            for image in self._baseimages:
                height = max(height, image.get_height())

        if bbox_width is None:
            bbox_width = width

        if bbox_height is None:
            bbox_height = height

        for i in xrange(len(self._baseimages)):
            if game.scale_smooth:
                try:
                    self._baseimages[i] = pygame.transform.smoothscale(
                        self._baseimages[i], (width, height))
                except pygame.error:
                    self._baseimages[i] = pygame.transform.scale(
                        self._baseimages[i], (width, height))
            else:
                self._baseimages[i] = pygame.transform.scale(
                    self._baseimages[i], (width, height))

        self._w = width
        self._h = height
        self.origin_x = origin_x
        self.origin_y = origin_y
        self._transparent = transparent
        self.fps = fps
        self.bbox_x = bbox_x
        self.bbox_y = bbox_y
        self.bbox_width = bbox_width
        self.bbox_height = bbox_height
        self._refresh()
        game.sprites[self.name] = self

    def draw_dot(self, x, y, color, frame=None):
        """Draw a single-pixel dot.

        ``x`` and ``y`` indicate the location in the sprite to draw the
        dot, where x=0, y=0 is the origin and x and y increase toward
        the right and bottom, respectively.  ``color`` indicates the
        color of the dot.  ``frame`` indicates the frame of the sprite
        to draw on, where 0 is the first frame; set to None to draw on
        all frames.

        """
        color = _get_pygame_color(color)
        for i in xrange(len(self._baseimages)):
            if frame is None or frame % len(self._baseimages) == i:
                self._baseimages[i].set_at((x, y), color)

        self._refresh()

    def draw_line(self, x1, y1, x2, y2, color, thickness=1, anti_alias=False,
                  frame=None):
        """Draw a line segment between the given points.

        ``x1``, ``y1``, ``x2``, and ``y2`` indicate the location in the
        sprite of the points between which to draw the line segment,
        where x=0, y=0 is the origin and x and y increase toward the
        right and bottom, respectively.  ``color`` indicates the color
        of the line segment.  ``thickness`` indicates the thickness of
        the line segment in pixels.  ``anti_alias`` indicates whether or
        not anti-aliasing should be used.  ``frame`` indicates the frame
        of the sprite to draw on, where 0 is the first frame; set to
        None to draw on all frames.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this method will act like ``anti_alias`` is
        False.

        """
        color = _get_pygame_color(color)
        thickness = abs(thickness)

        for i in xrange(len(self._baseimages)):
            if frame is None or frame % len(self._baseimages) == i:
                if anti_alias and thickness == 1:
                    pygame.draw.aaline(self._baseimages[i], color, (x1, y1),
                                       (x2, y2))
                else:
                    pygame.draw.line(self._baseimages[i], color, (x1, y1),
                                     (x2, y2), thickness)

        self._refresh()

    def draw_rectangle(self, x, y, width, height, fill=None, outline=None,
                       outline_thickness=1, frame=None):
        """Draw a rectangle at the given position.

        ``x`` and ``y`` indicate the location in the sprite to position
        the top-left corner of the rectangle, where x=0, y=0 is the
        origin and x and y increase toward the right and bottom,
        respectively.  ``width`` and ``height`` indicate the size of the
        rectangle.  ``fill`` indicates the color of the fill of the
        rectangle; set to None for no fill.  ``outline`` indicates the
        color of the outline of the rectangle; set to None for no
        outline.  ``outline_thickness`` indicates the thickness of the
        outline in pixels (ignored if there is no outline).  ``frame``
        indicates the frame of the sprite to draw on, where 0 is the
        first frame; set to None to draw on all frames.

        """
        outline_thickness = abs(outline_thickness)
        if outline_thickness == 0:
            outline = None

        if fill is None and outline is None:
            # There's no point in trying in this case.
            return

        rect = pygame.Rect(x, y, width, height)

        for i in xrange(len(self._baseimages)):
            if frame is None or frame % len(self._baseimages) == i:
                if fill is not None:
                    self._baseimages[i].fill(_get_pygame_color(fill), rect)

                if outline is not None:
                    pygame.draw.rect(self._baseimages[i],
                                     _get_pygame_color(outline), rect,
                                     outline_thickness)

        self._refresh()

    def draw_ellipse(self, x, y, width, height, fill=None, outline=None,
                     outline_thickness=1, anti_alias=False, frame=None):
        """Draw an ellipse at the given position.

        ``x`` and ``y`` indicate the location in the sprite to position
        the top-left corner of the imaginary rectangle containing the
        ellipse, where x=0, y=0 is the origin and x and y increase
        toward the right and bottom, respectively.  ``width`` and
        ``height`` indicate the size of the ellipse.  ``fill`` indicates
        the color of the fill of the ellipse; set to None for no fill.
        ``outline`` indicates the color of the outline of the ellipse;
        set to None for no outline.  ``outline_thickness`` indicates the
        thickness of the outline in pixels (ignored if there is no
        outline).  ``anti_alias`` indicates whether or not anti-aliasing
        should be used on the outline.  ``frame`` indicates the frame of
        the sprite to draw on, where 0 is the first frame; set to None
        to draw on all frames.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this method will act like ``anti_alias`` is
        False.

        """
        outline_thickness = abs(outline_thickness)
        if outline_thickness == 0:
            outline = None

        if fill is None and outline is None:
            # There's no point in trying in this case.
            return

        rect = pygame.Rect(x, y, width, height)

        for i in xrange(len(self._baseimages)):
            if frame is None or frame % len(self._baseimages) == i:
                if fill is not None:
                    c = _get_pygame_color(fill)
                    pygame.draw.ellipse(self._baseimages[i], c, rect)

                if outline is not None:
                    c = _get_pygame_color(outline)
                    pygame.draw.ellipse(self._baseimages[i], c, rect,
                                        outline_thickness)

        self._refresh()

    def draw_circle(self, x, y, radius, fill=None, outline=None,
                    outline_thickness=1, anti_alias=False, frame=None):
        """Draw a circle at the given position.

        ``x`` and ``y`` indicate the location in the sprite to position
        the center of the circle, where x=0, y=0 is the origin and x and
        y increase toward the right and bottom, respectively.
        ``radius`` indicates the radius of the circle in pixels.
        ``fill`` indicates the color of the fill of the circle; set to
        None for no fill.  ``outline`` indicates the color of the
        outline of the circle; set to None for no outline.
        ``outline_thickness`` indicates the thickness of the outline in
        pixels (ignored if there is no outline).  ``anti_alias``
        indicates whether or not anti-aliasing should be used on the
        outline.  ``frame`` indicates the frame of the sprite to draw
        on, where 0 is the first frame; set to None to draw on all
        frames.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this method will act like ``anti_alias`` is
        False.

        """
        outline_thickness = abs(outline_thickness)
        if outline_thickness == 0:
            outline = None

        if fill is None and outline is None:
            # There's no point in trying in this case.
            return

        for i in xrange(len(self._baseimages)):
            if frame is None or frame % len(self._baseimages) == i:
                if fill is not None:
                    c = _get_pygame_color(fill)
                    pygame.draw.circle(self._baseimages[i], c, (x, y), radius)

                if outline is not None:
                    c = _get_pygame_color(outline)
                    pygame.draw.circle(self._baseimages[i], c, (x, y), radius,
                                       outline_thickness)

        self._refresh()

    def draw_sprite(self, sprite, image, x, y, frame=None):
        """Draw the given sprite at the given position.

        ``sprite`` indicates the sprite to draw.  ``image`` indicates
        the frame of ``sprite`` to draw, where 0 is the first frame.
        ``x`` and ``y`` indicate the location in the sprite being drawn
        on to position ``sprite``.  ``frame`` indicates the frame of the
        sprite to draw on, where 0 is the first frame; set to None to
        draw on all frames.

        """
        x -= sprite.origin_x
        y -= sprite.origin_y
        image %= len(sprite._baseimages)

        for i in xrange(len(self._baseimages)):
            if frame is None or frame % len(self._baseimages) == i:
                self._baseimages[i].blit(sprite._baseimages[i], (x, y))

        self._refresh()

    def draw_text(self, font, text, x, y, width=None, height=None,
                  color="black", halign=ALIGN_LEFT, valign=ALIGN_TOP,
                  anti_alias=True, frame=None):
        """Draw the given text at the given position.

        ``font`` indicates the font to use to draw the text.  ``text``
        indicates the text to draw.  ``x`` and ``y`` indicate the
        location in the sprite to position the text, where x=0, y=0 is
        the origin and x and y increase toward the right and bottom,
        respectively.  ``width`` and ``height`` indicate the size of the
        imaginary box the text is drawn in; set to None for no imaginary
        box.  ``color`` indicates the color of the text.  ``halign``
        indicates the horizontal alignment of the text and can be
        ALIGN_LEFT, ALIGN_CENTER, or ALIGN_RIGHT.  ``valign`` indicates
        the vertical alignment and can be ALIGN_TOP, ALIGN_MIDDLE, or
        ALIGN_BOTTOM.  ``anti_alias`` indicates whether or not anti-
        aliasing should be used.  ``frame`` indicates the frame of the
        sprite to draw on, where 0 is the first frame; set to None to
        draw on all frames.

        If the text does not fit into the imaginary box specified, the
        text that doesn't fit will be cut off at the bottom if valign is
        ALIGN_TOP, the top if valign is ALIGN_BOTTOM, or equally the top
        and bottom if valign is ALIGN_MIDDLE.

        Support for anti-aliasing is optional in Stellar Game Engine
        implementations.  If the implementation used does not support
        anti-aliasing, this function will act like ``anti_alias`` is False.

        """
        if not isinstance(font, Font):
            font = game.fonts[font]

        lines = font._split_text(text, width)
        width, height = font.get_size(text, x, y, width, height)
        fake_height = font.get_size(text, x, y, width)[1]
        color = _get_pygame_color(color)

        text_surf = pygame.Surface((width, fake_height), pygame.SRCALPHA)
        box_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        text_rect = text_surf.get_rect()
        box_rect = box_surf.get_rect()

        for i in xrange(len(lines)):
            rendered_text = font._font.render(lines[i], anti_alias, color)
            rect = rendered_text.get_rect()
            rect.top = i * font._font.get_linesize()

            if halign == ALIGN_LEFT:
                rect.left = text_rect.left
            elif halign == ALIGN_RIGHT:
                rect.right = text_rect.right
            elif halign == ALIGN_CENTER:
                rect.centerx = text_rect.centerx

            text_surf.blit(rendered_text, rect)

        if valign == ALIGN_TOP:
            text_rect.top = box_rect.top
        elif valign == ALIGN_BOTTOM:
            text_rect.bottom = box_rect.bottom
        elif valign == ALIGN_MIDDLE:
            text_rect.centery = box_rect.centery

        box_surf.blit(text_surf, text_rect)

        if halign == ALIGN_LEFT:
            box_rect.left = x
        elif halign == ALIGN_RIGHT:
            box_rect.right = x
        elif halign == ALIGN_CENTER:
            box_rect.centerx = x
        else:
            box_rect.left = x

        if valign == ALIGN_TOP:
            box_rect.top = y
        elif valign == ALIGN_BOTTOM:
            box_rect.bottom = y
        elif valign == ALIGN_MIDDLE:
            box_rect.centery = y
        else:
            box_rect.top = y

        for i in xrange(len(self._baseimages)):
            if frame is None or frame % len(self._baseimages) == i:
                self._baseimages[i].blit(box_surf, box_rect)

        self._refresh()

    def draw_clear(self, frame=None):
        """Erase everything from the sprite.

        ``frame`` indicates the frame of the sprite to clear, where 0 is
        the first frame; set to None to clear all frames.

        """
        for i in xrange(len(self._baseimages)):
            if frame is None or frame % len(self._baseimages) == i:
                if self._baseimages[i].get_flags() & pygame.SRCALPHA:
                    color = pygame.Color(0, 0, 0, 0)
                else:
                    color = self._baseimages[i].get_colorkey()

                self._baseimages[i].fill(color)

        self._refresh()

    def _refresh(self):
        # Set the _images list based on the variables.
        game._background_changed = True
        self._images = []
        for image in self._baseimages:
            img = self._set_transparency(image)
            img = _scale(img, self.width, self.height)
            self._images.append({(1, 1, 0, 255, None):img})

    def _set_transparency(self, image):
        # Return a copy of the surface with transparency properly set
        # for this sprite's settings.
        if self.transparent and image.get_width() > 0:
            if image.get_flags() & pygame.SRCALPHA:
                return image.convert_alpha()
            else:
                colorkey_img = image.convert()
                color = image.get_at((image.get_width() - 1, 0))
                colorkey_img.set_colorkey(color, pygame.RLEACCEL)
                return colorkey_img
        else:
            return image.convert()

    def _get_image(self, num, xscale=1, yscale=1, rotation=0, alpha=255,
                   blend=None):
        # Return the properly sized surface.
        if (xscale, yscale, rotation, alpha, blend) in self._images[num]:
            return self._images[num][(xscale, yscale, rotation, alpha, blend)]
        else:
            # Hasn't been scaled to this size yet
            if xscale != 0 and yscale != 0:
                img = self._set_transparency(self._baseimages[num])
                xflip = xscale < 0
                yflip = yscale < 0
                img = pygame.transform.flip(img, xflip, yflip)
                img = _scale(img, self.width * abs(xscale),
                             self.height * abs(yscale))

                if rotation != 0:
                    img = pygame.transform.rotate(img, rotation)

                if alpha < 255:
                    if img.get_flags() & pygame.SRCALPHA:
                        # Have to do this the more difficult way.
                        img.fill((0, 0, 0, 255 - alpha), None,
                                 pygame.BLEND_RGBA_SUB)
                    else:
                        img.set_alpha(alpha, pygame.RLEACCEL)

                if blend is not None:
                    img.fill(_get_pygame_color(blend), None,
                             pygame.BLEND_RGB_MULT)
            else:
                img = pygame.Surface((1, 1))
                img.set_colorkey((0, 0, 0), pygame.RLEACCEL)

            self._images[num][(xscale, yscale, rotation, alpha, blend)] = img
            return img

    def _get_precise_mask(self, num):
        # Return a precise mask (2D list of True/False values) for the
        # given image index.
        if num in self._masks:
            return self._masks[num]
        else:
            image = self._get_image(num)
            image.lock()
            mask = []
            if image.get_flags() & pygame.SRCALPHA:
                for x in xrange(image.get_width()):
                    mask.append([])
                    for y in xrange(image.get_height()):
                        mask[x].append(image.get_at((x, y)).a > 0)
            else:
                colorkey = image.get_colorkey()
                for x in xrange(image.get_width()):
                    mask.append([])
                    for y in xrange(image.get_height()):
                        mask[x].append(image.get_at((x, y)) == colorkey)

            image.unlock()
            self._masks[num] = mask
            return mask


class BackgroundLayer(object):

    """Special class used for background layers.

    All BackgroundLayer objects have the following attributes:
        sprite: The Sprite object used for this layer.  While it will
            always be an actual Sprite object when read, it can also be
            set to the ID of a sprite.
        x: The horizontal offset of the layer.
        y: The vertical offset of the layer.
        z: The Z-axis position of the layer in the room, which
            determines in what order layers are drawn; layers with a
            higher Z value are drawn in front of layers with a lower Z
            value.
        xscroll_rate: The horizontal speed the layer scrolls as a factor
            of the view scroll speed.
        yscroll_rate: The vertical speed the layer scrolls as a factor
            of the view scroll speed.
        xrepeat: Whether or not the layer should be repeated
            horizontally.
        yrepeat: Whether or not the layer should be repeated
            vertically.

    """

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, value):
        if not isinstance(value, Sprite):
            value = game.sprites[value]

        if self._sprite != value:
            self._sprite = value
            game._background_changed = True

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if self._x != value:
            self._x = value
            game._background_changed = True

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if self._y != value:
            self._y = value
            game._background_changed = True

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        if self._z != value:
            self._z = value
            game._background_changed = True

    @property
    def xscroll_rate(self):
        return self._xscroll_rate

    @xscroll_rate.setter
    def xscroll_rate(self, value):
        if self._xscroll_rate != value:
            self._xscroll_rate = value
            game._background_changed = True

    @property
    def yscroll_rate(self):
        return self._yscroll_rate

    @yscroll_rate.setter
    def yscroll_rate(self):
        if self._yscroll_rate != value:
            self._yscroll_rate = value
            game._background_changed = True

    @property
    def xrepeat(self):
        return self._xrepeat

    @xrepeat.setter
    def xrepeat(self, value):
        if self._xrepeat != value:
            self._xrepeat = value
            game._background_changed = True

    @property
    def yrepeat(self):
        return self._yrepeat

    @yrepeat.setter
    def yrepeat(self, value):
        if self._yrepeat != value:
            self._yrepeat = value
            game._background_changed = True

    def __init__(self, sprite, x, y, z, xscroll_rate=1, yscroll_rate=1,
                 xrepeat=True, yrepeat=True):
        """Create a background layer object.

        Arguments set the properties of the layer.  See
        BackgroundLayer.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        self._sprite = sprite
        self._x = x
        self._y = y
        self._z = z
        self._xscroll_rate = xscroll_rate
        self._yscroll_rate = yscroll_rate
        self._xrepeat = xrepeat
        self._yrepeat = yrepeat

        self._image_index = 0
        self._count = 0
        if self.sprite.fps != 0:
            self._frame_time = 1000 / self.sprite.fps
            if not self._frame_time:
                # This would be caused by a round-off to 0 resulting
                # from a much too high frame rate.  It would cause a
                # division by 0 later, so this is meant to prevent that.
                self._frame_time = 0.01
        else:
            self._frame_time = None

    def _update(self, time_passed):
        # Update the animation frame.
        if self._frame_time is not None:
            self._count += time_passed
            self._image_index += int(self._count // self._frame_time)
            self._count %= self._frame_time
            self._image_index %= len(self.sprite._images)

    def _get_image(self):
        return self.sprite._get_image(self._image_index)


class Background(object):

    """Background class.

    All Background objects have the following attributes:
        color: A Stellar Game Engine color used in parts of the
            background where there is no layer.

    The following read-only attributes are also available:
        id: The unique identifier for this background.
        layers: A tuple containing all BackgroundLayer objects used in
            this background.

    """

    def __init__(self, layers, color, id_=None, **kwargs):
        """Create a background with the given color and layers.

        Arguments set the properties of the background.  See
        Background.__doc__ for more information.

        If ``id`` is None, it will be set to an integer not currently
        used as an ID (the exact number chosen is implementation-
        specific and may not necessarily be the same between runs).

        In addition to containing actual BackgroundLayer objects,
        ``layers`` can contain valid names of BackgroundLayer objects'
        sprites.

        A game object must exist before an object of this class is
        created.

        """
        # Since the docs say that ``id`` is a valid keyword argument,
        # you should do this to make sure that that is true.
        id_ = kwargs.setdefault('id', id_)

        self.color = color

        if id_ is not None:
            self.id = id_
        else:
            id_ = 0
            while id_ in game.backgrounds:
                id_ += 1
            self.id = id_

        game.backgrounds[self.id] = self

        unsorted_layers = []
        sorted_layers = []

        for layer in layers:
            if isinstance(layer, BackgroundLayer):
                unsorted_layers.append(layer)
            else:
                if layer in game.background_layers:
                    unsorted_layers.append(game.background_layers[layer])

        for layer in unsorted_layers:
            i = 0
            while i < len(sorted_layers) and layer.z >= sorted_layers[i].z:
                i += 1

            sorted_layers.insert(i, layer)

        self.layers = tuple(sorted_layers)

    def _get_background(self):
        # Return the static background this frame.
        background = pygame.Surface((round(game.width * game._xscale),
                                     round(game.height * game._yscale)))
        background.fill(_get_pygame_color(self.color))

        for view in game.current_room.views:
            view_x = int(round(view.x * game._xscale))
            view_y = int(round(view.y * game._yscale))
            view_xport = max(0, min(int(round(view.xport * game._xscale)),
                                    background.get_width() - 1))
            view_yport = max(0, min(int(round(view.yport * game._yscale)),
                                    background.get_height() - 1))
            view_w = min(int(round((game.width - view.xport) * game._xscale)),
                         background.get_width() - view_xport)
            view_h = min(int(round((game.height - view.yport) * game._yscale)),
                         background.get_height() - view_yport)
            surf = background.subsurface(view_xport, view_yport, view_w,
                                         view_h)
            for layer in self.layers:
                image = layer._get_image()
                x = int(round((layer.x - (view.x * layer.xscroll_rate)) *
                              game._xscale))
                y = int(round((layer.y - (view.y * layer.yscroll_rate)) *
                              game._yscale))
                image_w = max(1, image.get_width())
                image_h = max(1, image.get_height())

                # These equations bring the position to the largest
                # values possible while still being less than the
                # location we're getting the surface at.  This is to
                # minimize the number of repeat blittings.
                if layer.xrepeat:
                    x = (x % image_w) - image_w
                if layer.yrepeat:
                    y = (y % image_h) - image_h

                # Apply the origin so the positions are as expected.
                x -= layer.sprite.origin_x
                y -= layer.sprite.origin_y

                if layer.xrepeat and layer.yrepeat:
                    xstart = x
                    while y < surf.get_height():
                        x = xstart
                        while x < surf.get_width():
                            surf.blit(image, (x, y))
                            x += image_w
                        y += image_h
                elif (layer.xrepeat and y < view_y + view_h and
                      y + image_h > view_y):
                    while x < surf.get_width():
                        surf.blit(image, (x, y))
                        x += image_w
                elif (layer.yrepeat and x < view_x + view_w and
                      x + image_w > view_x):
                    while y < surf.get_height():
                        surf.blit(image, (x, y))
                        y += image_h
                elif (x < surf.get_width() and x + image_w > 0 and
                      y < surf.get_height() and y + image_h > 0):
                    surf.blit(image, (x, y))

        return background


class Font(object):

    """Font handling class.

    All Font objects have the following attributes:
        size: The height of the font in pixels.
        underline: Whether or not underlined rendering is enabled.
        bold: Whether or not bold rendering is enabled.
        italic: Whether or not italic rendering is enabled.

    The following read-only attributes are also available:
        name: The name of the font given when it was created.  See
            Sound.__init__.__doc__ for more information.

    Font methods:
        get_size: Return the size of the given rendered text.

    """

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self._font = None

        for path in font_directories:
            path = os.path.join(path, self.name)
            if os.path.isfile(path):
                self._font = pygame.font.Font(path, self._size)

        if self._font is None:
            self._font = pygame.font.SysFont(self.name, self._size)

    @property
    def underline(self):
        return self._font.get_underline()

    @underline.setter
    def underline(self, value):
        self._font.set_underline(bool(value))

    @property
    def bold(self):
        return self._font.get_bold()

    @bold.setter
    def bold(self, value):
        self._font.set_bold(bool(value))

    @property
    def italic(self):
        return self._font.get_italic()

    @italic.setter
    def italic(self, value):
        self._font.set_italic(bool(value))

    def __init__(self, name=None, size=12, underline=False, bold=False,
                 italic=False):
        """Create a new Font object.

        ``name`` indicates the name of the font.  This can be either the
        name of a font file, to be located in one of the directories
        specified in ``font_directories``, or the name of a system
        font.  If the specified font does not exist in either form, a
        default, implementation-dependent font will be used.

        ``name`` can also be a list or tuple of fonts to choose from in
        order of preference.

        Implementations are supposed, but not required, to attempt to
        use a compatible font where possible.  For example, if the font
        specified is "Times New Roman" and Times New Roman is not
        available, compatible fonts such as Liberation Serif should be
        attempted as well.

        All remaining arguments set the initial properties of the font.
        See Font.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        assert pygame.font.get_init()

        if isinstance(name, basestring):
            name = (name,)

        self.name = ''
        compatible_fonts = (
            ("liberation serif", "tinos", "times new roman",
             "nimbus roman no9 l", "nimbus roman", "freeserif",
             "dejavu serif"),
            ("liberation sans", "arimo", "arial", "nimbus sans l", "freesans",
             "dejavu sans"),
            ("liberation sans narrow", "arial narrow"),
            ("liberation mono", "cousine", "courier new", "courier",
             "nimbus mono l", "freemono", "texgyrecursor", "courier prime",
             "dejavu sans mono"))

        try:
            for n in name:
                for fonts in compatible_fonts:
                    if n.lower() in fonts:
                        n = ','.join((n, ','.join(fonts)))
                        break

                self.name = ','.join((self.name, n))
        except TypeError:
            # Most likely a non-iterable value, such as None, so we
            # assume the default font is to be used.
            self.name = ''

        self.name = self.name[1:]
        self.size = size
        self.underline = underline
        self.bold = bold
        self.italic = italic

    def get_size(self, text, width=None, height=None):
        """Return the size of the given rendered text.

        All arguments correspond with the same arguments in Font.render,
        and the size returned reflects rendering rules therein; see
        Font.render.__doc__ for more information.  Returned value is a
        tuple in the form (width, height).

        """
        lines = self._split_text(text, width)
        text_width = 0
        text_height = self._font.get_linesize() * len(lines)

        for line in lines:
            text_width = max(text_width, self._font.size(line)[0])

        if width is not None:
            text_width = min(text_width, width)

        if height is not None:
            text_height = min(text_height, height)

        return (text_width, text_height)

    def _split_text(self, text, width=None):
        # Split the text into lines of the proper size for ``width`` and
        # return a list of the lines.  If ``width`` is None, only
        # newlines split the text.
        lines = text.split('\n')

        if width is None:
            return lines
        else:
            split_text = []
            for line in lines:
                if self._font.size(line)[0] <= width:
                    split_text.append(line)
                else:
                    words = line.split(' ')
                    while words:
                        current_line = words.pop(0)
                        while (words and self._font.size(
                                ' '.join((current_line, words[0]))) < width):
                            current_line = ' '.join((current_line,
                                                     words.pop(0)))
                        split_text.append(current_line)
            return split_text


class Sound(object):

    """Sound handling class.

    All Sound objects have the following attributes:
        volume: The volume of the sound in percent (0 for no sound, 100
            for max sound).
        balance: The balance of the sound effect on stereo speakers.  A
            value of 0 means centered (an equal amount of play on both
            speakers), -1 means entirely in the left speaker, and 1
            means entirely in the right speaker.  Support for this
            feature in Stellar Game Engine implementations is optional.
            If it is unavailable, all sounds will be played through both
            speakers equally (assuming stereo sound is used).
        max_play: The maximum instances of this sound playing permitted.
            Set to 0 for no limit.

    The following read-only attributes are also available:
        fname: The file name of the sound given when it was created.
            See Sound.__init__.__doc__ for more information.
        length: The length of the sound in milliseconds.
        playing: The number of instances of this sound playing.

    Sound methods:
        Sound.play: Play the sound.
        Sound.stop: Stop the sound.
        Sound.pause: Pause playback of the sound.
        Sound.unpause: Resume playback of the sound if paused.

    """

    @property
    def max_play(self):
        return len(self._channels)

    @max_play.setter
    def max_play(self, value):
        if self._sound is not None:
            value = max(0, value)
            while len(self._channels) < value:
                self._channels.append(game._get_channel())
            while len(self._channels) > value:
                game._release_channel(self._channels.pop(-1))

    @property
    def length(self):
        if self._sound is not None:
            return self._sound.get_length() * 1000
        else:
            return 0

    @property
    def playing(self):
        if self._sound is not None:
            return self._sound.get_num_channels()
        else:
            return 0

    def __init__(self, fname, volume=100, balance=0, max_play=1):
        """Create a new sound object.

        ``fname`` indicates the name of the sound file, to be located in
        one of the directories specified in ``sound_directories``.

        All remaining arguments set the initial properties of the sound.
        See Sound.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        self._sound = None

        if pygame.mixer.get_init():
            for path in sound_directories:
                path = os.path.join(path, fname)
                try:
                    self._sound = pygame.mixer.Sound(path)
                    break
                except pygame.error:
                    pass

        self._channels = []
        self._temp_channels = []
        self.fname = fname
        self.volume = volume
        self.balance = balance
        self.max_play = max_play

    def play(self, loops=0, maxtime=None, fade_time=None):
        """Play the sound.

        ``loops`` indicates the number of extra times to play the sound
        after it is played the first time; set to -1 or None to loop
        indefinitely.  ``maxtime`` indicates the maximum amount of time
        to play the sound in milliseconds; set to 0 or None for no
        limit. ``fade_time`` indicates the time in milliseconds over
        which to fade the sound in; set to 0 or None to immediately play
        the sound at full volume.

        """
        if self._sound is not None:
            if loops is None:
                loops = -1
            if maxtime is None:
                maxtime = 0
            if fade_time is None:
                fade_time = 0

            if self.max_play:
                for channel in self._channels:
                    if not channel.get_busy():
                        channel.play(self._sound, loops, maxtime, fade_time)
                        break
                else:
                    self._channels[0].play(self._sound, loops, maxtime,
                                           fade_time)
            else:
                channel = game._get_channel()
                channel.play(self._sound, loops, maxtime, fade_time)
                self._temp_channels.append(channel)

            # Clean up old temporary channels
            while (self._temp_channels and
                   not self._temp_channels[0].get_busy()):
                game._release_channel(self._temp_channels.pop(0))

    def stop(self, fade_time=None):
        """Stop the sound.

        ``fade_time`` indicates the time in milliseconds over which to
        fade the sound out before stopping; set to 0 or None to
        immediately stop the sound.

        """
        if self._sound is not None:
            self._sound.stop()

    def pause(self):
        """Pause playback of the sound."""
        for channel in self._channels:
            channel.pause()

    def unpause(self):
        """Resume playback of the sound if paused."""
        for channel in self._channels:
            channel.unpause()


class Music(object):

    """Music handling class.

    Music is mostly the same as sound, but only one can be played at a
    time.

    All Music objects have the following attributes:
        volume: The volume of the music in percent (0 for no sound, 100
            for max sound).
        balance: The balance of the music on stereo speakers.  A value
            of 0 means centered (an equal amount of play on both
            speakers), -1 means entirely in the left speaker, and 1
            means entirely in the right speaker.  Support for this
            feature in Stellar Game Engine implementations is optional.
            If it is unavailable, all music will be played through both
            speakers equally (assuming stereo sound is used).

    The following read-only attributes are also available:
        fname: The file name of the music given when it was created.
            See Music.__init__.__doc__ for more information.
        length: The length of the music in milliseconds.
        playing: Whether or not the music is playing.
        position: The current position (time) on the music in
            milliseconds.

    Music methods:
        Music.play: Play the music.
        Music.queue: Queue the music for playback.
        Music.stop: Stop the music.
        Music.pause: Pause playback of the music.
        Music.unpause: Resume playback of the music if paused.
        Music.restart: Restart music from the beginning.

    """

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = min(value, 100)

        if self.playing:
            pygame.mixer.music.set_volume(value / 100)

    @property
    def length(self):
        return self._length

    @property
    def playing(self):
        return game._music is self and pygame.mixer.music.get_busy()

    @property
    def position(self):
        if self.playing:
            return self._start + pygame.mixer.music.get_pos()
        else:
            return 0

    def __init__(self, fname, volume=100, balance=0):
        """Create a new music object.

        ``fname`` indicates the name of the sound file, to be located in
        one of the directories specified in ``music_directories``.

        All remaining arguments set the initial properties of the music.
        See Music.__doc__ for more information.

        A game object must exist before an object of this class is
        created.

        """
        self.fname = fname
        self.volume = volume
        self.balance = balance
        self._timeout = None
        self._fade_time = None
        self._start = 0

        self._full_fname = None
        if pygame.mixer.get_init():
            for path in music_directories:
                path = os.path.join(path, fname)
                if os.path.isfile(path):
                    self._full_fname = path
                    break

    def play(self, start=0, loops=0, maxtime=None, fade_time=None):
        """Play the music.

        If music was already playing when this is called, it will be
        stopped.

        ``start`` indicates the number of milliseconds from the
        beginning to start at.  ``loops`` indicates the number of extra
        times to play the sound after it is played the first time; set
        to -1 or None to loop indefinitely.  ``maxtime`` indicates the
        maximum amount of time to play the sound in milliseconds; set to
        0 or None for no limit.  ``fade_time`` indicates the time in
        milliseconds over which to fade the sound in; set to 0 or None
        to immediately play the music at full volume.

        """
        if self._full_fname is not None:
            if not self.playing:
                pygame.mixer.music.load(self._full_fname)

            if loops is None:
                loops = -1

            game._music = self
            self._timeout = maxtime
            self._fade_time = fade_time

            if self._fade_time > 0:
                pygame.mixer.music.set_volume(0)

            if self.fname.lower().endswith(".mod"):
                # MOD music is handled differently in Pygame: it uses
                # the pattern order number rather than the time to
                # indicate the start time.
                self._start = 0
                pygame.mixer.music.play(loops, start)
            else:
                self._start = start
                try:
                    pygame.mixer.music.play(loops, start / 1000)
                except NotImplementedError:
                    pygame.mixer.music.play(loops)

    def queue(self, start=0, loops=0, maxtime=None, fade_time=None):
        """Queue the music for playback.

        This will cause the music to be added to a list of music to play
        in order, after the previous music has finished playing.

        See Music.play.__doc__ for information about the arguments.

        """
        game._music_queue.append((self, start, loops, maxtime, fade_time))

    def stop(self, fade_time=None):
        """Stop the music.

        ``fade_time`` indicates the time in milliseconds over which to
        fade the sound out before stopping; set to 0 or None to
        immediately stop the music.

        """
        if self.playing:
            if fade_time:
                pygame.mixer.music.fadeout(fade_time)
            else:
                pygame.mixer.music.stop()

    def pause(self):
        """Pause playback of the music."""
        if self.playing:
            pygame.mixer.music.pause()

    def unpause(self):
        """Resume playback of the music if paused."""
        if self.playing:
            pygame.mixer.music.unpause()


class StellarClass(object):

    """Class for game objects.

    All StellarClass objects have the following attributes:
        x: The horizontal position of the object in the room, where the
            left edge is 0 and x increases toward the right.
        y: The vertical position of the object in the room, where the
            top edge is 0 and y increases toward the bottom.
        z: The Z-axis position of the object in the room, which
            determines in what order objects are drawn; objects with a
            higher Z value are drawn in front of objects with a lower Z
            value.
        sprite: The sprite currently in use by this object.  Set to None
            for no (visible) sprite.  While it will always be an actual
            Sprite object or None when read, it can also be set to the
            ID of a sprite.
        visible: Whether or not the object should be drawn.
        detects_collisions: Whether or not the object should be involved
            in collisions.
        bbox_x: The horizontal location of the top-left corner of the
            bounding box in relation to x, where 0 is x and bbox_x
            increases toward the right.
        bbox_y: The vertical location of the top-left corner of the
            bounding box in relation to y, where 0 is y and bbox_y
            increases toward the bottom.
        bbox_width: The width of the bounding box in pixels.
        bbox_height: The height of the bounding box in pixels.
        collision_ellipse: Whether or not an ellipse (rather than a
            rectangle) should be used for collision detection.
        collision_precise: Whether or not precise (pixel-perfect)
            collision detection should be used.
        bbox_left: The position of the left side of the bounding box in
            the room (same as x + bbox_x).
        bbox_right: The position of the right side of the bounding box
            in the room (same as bbox_left + bbox_width).
        bbox_top: The position of the top side of the bounding box
            (same as y + bbox_y).
        bbox_bottom: The position of the bottom side of the bounding
            box (same as bbox_top + bbox_height).
        xvelocity: The velocity of the object toward the right.  Default
            is 0.
        yvelocity: The velocity of the object toward the bottom.
            Default is 0.
        speed: The total (directional) speed of the object.  Default is
            0.
        move_direction: The direction of the object's movement in
            degrees, with 0 being directly to the right and rotation in
            a positive direction being counter-clockwise.  Default is 0.
        image_index: The animation frame currently being displayed, with
            0 being the first one.  Default is 0.
        image_fps: The animation rate in frames per second.  Default is
            the value recommended by the sprite, or 0 if there is no
            sprite.
        image_xscale: The horizontal scale factor for the sprite.
            Default is 1.
        image_yscale: The vertical scale factor for the sprite.  Default
            is 1.
        image_rotation: The rotation of the sprite, with rotation in a
            positive direction being counter-clockwise.  Default is 0.
        image_alpha: The alpha value applied to the entire image, where
            255 is the original image, 128 is half the opacity of the
            original image, 0 is fully transparent, etc.  Default is
            255.
        image_blend: The color to blend with the sprite.  Set to None
            for no color blending.  Default is None.

    The following read-only attributes are also available:
        id: The unique identifier for this object.
        xstart: The initial value of x when the object was created.
        ystart: The initial value of y when the object was created.
        xprevious: The previous value of x.
        yprevious: The previous value of y.

    StellarClass methods:
        collides: Return whether or not this object collides with
            another.
        set_alarm: Set an alarm.
        get_alarm: Return the count on an alarm.
        destroy: Destroy the object.

    StellarClass events are handled by special methods.  The exact
    timing of their calling is implementation-dependent except where
    otherwise noted.  The methods are:
        event_create: Called when the object is created.  It is always
            called after any room start events occurring at the same
            time.
        event_step: Called once each frame.
        event_alarm: Called when an alarm counter reaches 0.
        event_key_press: Key press event.
        event_key_release: Key release event.
        event_mouse_move: Mouse move event.
        event_mouse_button_press: Mouse button press event.
        event_mouse_button_release: Mouse button release event.
        event_joystick_axis_move: Joystick axis move event.
        event_joystick_hat_move: Joystick HAT move event.
        event_joystick_button_press: Joystick button press event.
        event_joystick_button_release: Joystick button release event.
        event_close: Close event (e.g. close button).
        event_collision: Middle/default collision event.
        event_collision_left: Left collision event.
        event_collision_right: Right collision event.
        event_collision_top: Top collision event.
        event_collision_bottom: Bottom collision event.
        event_animation_end: Called when an animation cycle ends.
        event_destroy: Destroy event.

    The following alternative events are executed when the game is
    paused in place of the corresponding normal events:
        event_paused_key_press
        event_paused_key_release
        event_paused_mouse_move
        event_paused_mouse_button_press
        event_paused_mouse_button_release
        event_paused_joystick_axis_move
        event_paused_joystick_hat_move
        event_paused_joystick_button_press
        event_paused_joystick_button_release

    """

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self.xprevious = self._x
        self._x = value
        self._bbox_left = value + self.bbox_x
        self._bbox_right = self.bbox_left + self.bbox_width

        # Cause the Pygame sprite to make itself dirty
        self._pygame_sprite.rect = pygame.Rect(0, 0, 1, 1)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self.yprevious = self._y
        self._y = value
        self._bbox_top = value + self.bbox_y
        self._bbox_bottom = self.bbox_top + self.bbox_height

        # Cause the Pygame sprite to make itself dirty
        self._pygame_sprite.rect = pygame.Rect(0, 0, 1, 1)

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value
        if self._pygame_sprite in game._pygame_sprites:
            self._pygame_sprite.kill()
            game._pygame_sprites.add(self._pygame_sprite, layer=self._z)

        # Cause the Pygame sprite to make itself dirty
        self._pygame_sprite.rect = pygame.Rect(0, 0, 1, 1)

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, value):
        if isinstance(value, Sprite) or value is None:
            self._sprite = value
        else:
            self._sprite = game.sprites[value]

    @property
    def detects_collisions(self):
        return self._detects_collisions

    @detects_collisions.setter
    def detects_collisions(self, value):
        self._detects_collisions = value
        position = None
        for i in xrange(len(game._colliders)):
            if game._colliders[i]() is self:
                position = i
                break

        if self._detects_collisions:
            if position is None:
                game._colliders.append(weakref.ref(self))
        else:
            if position is not None:
                del game._colliders[position]

    @property
    def collision_ellipse(self):
        return self._collision_ellipse

    @collision_ellipse.setter
    def collision_ellipse(self, value):
        if value != self._collision_ellipse:
            self._collision_ellipse = value
            self._set_mask()

    @property
    def collision_precise(self):
        return self._collision_precise

    @collision_precise.setter
    def collision_precise(self, value):
        if value != self._collision_precise:
            self._collision_precise = value
            self._set_mask()

    @property
    def bbox_left(self):
        return self._bbox_left

    @bbox_left.setter
    def bbox_left(self, value):
        self.xprevious = self._x
        self._bbox_left = value
        self._bbox_right = value + self.bbox_width
        self._x = value - self.bbox_x

    @property
    def bbox_right(self):
        return self._bbox_right

    @bbox_right.setter
    def bbox_right(self, value):
        self.xprevious = self._x
        self._bbox_right = value
        self._bbox_left = value - self.bbox_width
        self._x = self.bbox_left - self.bbox_x

    @property
    def bbox_top(self):
        return self._bbox_top

    @bbox_top.setter
    def bbox_top(self, value):
        self.yprevious = self._y
        self._bbox_top = value
        self._bbox_bottom = value + self.bbox_height
        self._y = value - self.bbox_y

    @property
    def bbox_bottom(self):
        return self._bbox_bottom

    @bbox_bottom.setter
    def bbox_bottom(self, value):
        self.yprevious = self._y
        self._bbox_bottom = value
        self._bbox_top = value - self.bbox_height
        self._y = self.bbox_top - self.bbox_y

    @property
    def xvelocity(self):
        return self._xvelocity

    @xvelocity.setter
    def xvelocity(self, value):
        self._xvelocity = value
        self._set_speed()

    @property
    def yvelocity(self):
        return self._yvelocity

    @yvelocity.setter
    def yvelocity(self, value):
        self._yvelocity = value
        self._set_speed()

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value
        self._xvelocity = math.cos(radians(self.move_direction)) * value
        self._yvelocity = math.sin(radians(self.move_direction)) * value

    @property
    def move_direction(self):
        return self._move_direction

    @move_direction.setter
    def move_direction(self, value):
        self._move_direction = value
        self._xvelocity = math.cos(radians(value)) * self.speed
        self._yvelocity = math.sin(radians(value)) * self.speed

    @property
    def image_index(self):
        return self._image_index

    @image_index.setter
    def image_index(self, value):
        if self.sprite is not None:
            self._image_index = value
            while self._image_index >= len(self.sprite._images):
                self._image_index -= len(self.sprite._images)
                self.event_animation_end()
        else:
            self._image_index = 0

    @property
    def image_fps(self):
        return self._fps

    @image_fps.setter
    def image_fps(self, value):
        self._fps = abs(value)
        if self._fps != 0:
            self._frame_time = 1000 / self._fps
            if not self._frame_time:
                # This would be caused by a round-off to 0 resulting
                # from a much too high frame rate.  It would cause a
                # division by 0 later, so this is meant to prevent that.
                self._frame_time = 0.01
        else:
            self._frame_time = None

    def __init__(self, x, y, z, id_=None, sprite=None, visible=True,
                 detects_collisions=True, bbox_x=None, bbox_y=None,
                 bbox_width=None, bbox_height=None, collision_ellipse=False,
                 collision_precise=False, xvelocity=0, yvelocity=0,
                 image_index=0, image_fps=0, image_xscale=1, image_yscale=1,
                 image_rotation=0, image_alpha=255, image_blend=None,
                 **kwargs):
        """Create a new StellarClass object.

        Arguments set the properties of the object.  See
        StellarClass.__doc__ for more information.

        If bbox_x, bbox_y, bbox_width, or bbox_height is None, the
        respective argument will be determined by the sprite's suggested
        bounding box.

        If ``id`` is None, it will be set to an integer not currently
        used as an ID (the exact number chosen is implementation-
        specific and may not necessarily be the same between runs).

        A game object must exist before an object of this class is
        created.

        """
        # Since the docs say that ``id`` is a valid keyword argument,
        # you should do this to make sure that that is true.
        id_ = kwargs.setdefault('id', id_)

        self.xstart = x
        self.ystart = y
        self.xprevious = x
        self.yprevious = y

        self.sprite = sprite
        self.visible = visible
        self.detects_collisions = detects_collisions
        if self.sprite is not None:
            sprite_bbox_x = self.sprite.bbox_x
            sprite_bbox_y = self.sprite.bbox_y
            sprite_bbox_width = self.sprite.bbox_width
            sprite_bbox_height = self.sprite.bbox_height
        else:
            sprite_bbox_x = 0
            sprite_bbox_y = 0
            sprite_bbox_width = 1
            sprite_bbox_height = 1
        self.bbox_x = bbox_x if bbox_x is not None else sprite_bbox_x
        self.bbox_y = bbox_y if bbox_y is not None else sprite_bbox_y
        self.bbox_width = (bbox_width if bbox_width is not None else
                           sprite_bbox_width)
        self.bbox_height = (bbox_height if bbox_height is not None else
                            sprite_bbox_height)
        self._collision_ellipse = collision_ellipse
        self._collision_precise = collision_precise

        if id_ is not None:
            self.id = id_
        else:
            id_ = 0
            while id_ in game.objects:
                id_ += 1
            self.id = id_

        game.objects[self.id] = self

        self._x = x
        self._y = y
        self._z = z
        self._xvelocity = 0
        self._yvelocity = 0
        self._move_direction = 0
        self._speed = 0
        self.xvelocity = xvelocity
        self.yvelocity = yvelocity
        self._anim_count = 0
        self.image_index = image_index
        self.image_fps = (self.sprite.fps if self.sprite is not None else
                          image_fps)
        self.image_xscale = image_xscale
        self.image_yscale = image_yscale
        self.image_rotation = image_rotation
        self.image_alpha = image_alpha
        self.image_blend = image_blend

        self._alarms = {}

        self._rect = pygame.Rect(self.bbox_x, self.bbox_y, self.bbox_width,
                                 self.bbox_height)
        self._pygame_sprite = _PygameSprite(self)
        self._set_mask()

        self.x = x
        self.y = y
        self.z = z

        self._start_x = self.x
        self._start_y = self.y
        self._start_z = self.z
        self._start_sprite = self.sprite
        self._start_visible = self.visible
        self._start_detects_collisions = self.detects_collisions
        self._start_bbox_x = self.bbox_x
        self._start_bbox_y = self.bbox_y
        self._start_bbox_width = self.bbox_width
        self._start_bbox_height = self.bbox_height
        self._start_collision_ellipse = self.collision_ellipse
        self._start_collision_precise = self.collision_precise

    def collides(self, other, x=None, y=None):
        """Return whether or not this object collides with another.

        ``other`` indicates the object to check for a collision with, or
        the name of said object.  ``other`` can also be a class to check
        for collisions with.

        ``x`` and ``y``, indicate the position to check for collisions
        at.  If unspecified or None, this object's current position will
        be used.

        """
        if x is None:
            x = self.x
        if y is None:
            y = self.y

        # Change x and y to be offset values; these are easier to use.
        x -= self.x
        y -= self.y

        if (self.collision_precise or self.collision_ellipse or
                other.collision_precise or other.collision_ellipse):
            # Use masks.
            self_rect = pygame.Rect(round(self.bbox_left + x),
                                    round(self.bbox_top + y),
                                    self.bbox_width, self.bbox_height)
            other_rect = pygame.Rect(round(other.bbox_left),
                                     round(other.bbox_top),
                                     other.bbox_width, other.bbox_height)
            collide_rect = self_rect.clip(other_rect)

            self_xoffset = collide_rect.left - self_rect.left
            self_yoffset = collide_rect.top - self_rect.top
            other_xoffset = collide_rect.left - other_rect.left
            other_yoffset = collide_rect.top - other_rect.top

            for a in xrange(collide_rect.w):
                for b in xrange(collide_rect.h):
                    if (self._hitmask[a + self_xoffset][b + self_yoffset] and
                        other._hitmask[a + other_xoffset][b + other_yoffset]):
                        return True

            return False
                    
        else:
            # Use bounding boxes.
            return (self.bbox_left + x < other.bbox_right and
                    self.bbox_right + x > other.bbox_left and
                    self.bbox_top + y < other.bbox_bottom and
                    self.bbox_bottom + y > other.bbox_top)

    def set_alarm(self, alarm_id, value):
        """Set an alarm.

        Set the alarm with the given ``alarm_id`` with the given
        ``value``.  The alarm will then reduce by 1 each frame until it
        reaches 0 and set off the alarm event with the same ID.
        ``alarm_id`` can be any value.  ``value`` should be a number
        greater than 0.  You can also set ``value`` to None to disable
        the alarm.

        """
        if value is not None:
            self._alarms[alarm_id] = value
        elif alarm_id in self._alarms:
            del self._alarms[alarm_id]

    def get_alarm(self, alarm_id):
        """Return the count on an alarm.

        Get the number of frames before the alarm with ``alarm_id`` will
        go off.  If the alarm has not been set, None will be returned.

        """
        if alarm_id in self._alarms:
            return self._alarms[alarm_id]
        else:
            return None

    def destroy(self):
        """Destroy the object."""
        self.event_destroy()
        self._pygame_sprite.kill()
        del game.objects[self.id]

        for room in game.rooms:
            new_objects = []
            for obj in room.objects:
                if obj is not self:
                    new_objects.append(obj)
            room.objects = tuple(new_objects)

    def event_create(self):
        """Create event.

        Called when the object is created.  It is always called after
        any room start events occurring at the same time.

        """
        pass

    def event_step(self, time_passed):
        """Step event.

        Called once each frame.  ``time_passed`` is the number of
        milliseconds that have passed during the last frame.

        """
        pass

    def event_alarm(self, alarm_id):
        """Alarm event.

        Called when an alarm counter reaches 0.  ``alarm_id`` is the ID
        of the alarm that was set off.

        """
        pass

    def event_key_press(self, key):
        """Key press event.

        ``key`` is the key that was pressed.

        """
        pass

    def event_key_release(self, key):
        """Key release event.

        ``key`` is the key that was pressed.

        """
        pass

    def event_mouse_move(self, x, y):
        """Mouse move event.

        ``x`` and ``y`` indicate the relative movement of the mouse.

        """
        pass

    def event_mouse_button_press(self, button):
        """Mouse button press event.

        ``button`` is the number of the mouse button that was pressed;
        these numbers may vary by implementation, so MOUSE_BUTTON_*
        constants should be used.

        """
        pass

    def event_mouse_button_release(self, button):
        """Mouse button release event.

        ``button`` is the number of the mouse button that was released;
        these numbers may vary by implementation, so MOUSE_BUTTON_*
        constants should be used.

        """
        pass

    def event_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``axis`` is the number of the axis, where 0 is the
        first axis.  ``value`` is the tilt of the axis, where 0 is in
        the center, -1 is tilted all the way to the left or up, and 1 is
        tilted all the way to the right or down.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``hat`` is the number of the HAT, where 0 is the
        first HAT.  ``x`` and ``y`` indicate the position of the HAT,
        where 0 is in the center, -1 is left or up, and 1 is right or
        down.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_joystick_button_press(self, joystick, button):
        """Joystick button press event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``button`` is the number of the button pressed, where
        0 is the first button.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_joystick_button_release(self, joystick, button):
        """Joystick button release event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``button`` is the number of the button pressed, where
        0 is the first button.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_collision(self, other):
        """Middle/default collision event."""
        pass

    def event_collision_left(self, other):
        """Left collision event."""
        self.event_collision(other)

    def event_collision_right(self, other):
        """Right collision event."""
        self.event_collision(other)

    def event_collision_top(self, other):
        """Top collision event."""
        self.event_collision(other)

    def event_collision_bottom(self, other):
        """Bottom collision event."""
        self.event_collision(other)

    def event_animation_end(self):
        """Animation End event.

        Called when an animation cycle ends.

        """
        pass

    def event_destroy(self):
        """Destroy event."""
        pass

    def event_paused_key_press(self, key):
        """Key press event when paused.

        See StellarClass.event_key_press.__doc__ for more information.

        """
        pass

    def event_paused_key_release(self, key):
        """Key release event when paused.

        See StellarClass.event_key_release.__doc__ for more information.

        """
        pass

    def event_paused_mouse_move(self, x, y):
        """Mouse move event when paused.

        See StellarClass.event_mouse_move.__doc__ for more information.

        """
        pass

    def event_paused_mouse_button_press(self, button):
        """Mouse button press event when paused.

        See StellarClass.event_mouse_button_press.__doc__ for more
        information.

        """
        pass

    def event_paused_mouse_button_release(self, button):
        """Mouse button release event when paused.

        See StellarClass.event_mouse_button_release.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event when paused.

        See StellarClass.event_joystick_axis_move.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event when paused.

        See StellarClass.event_joystick_hat_move.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_button_press(self, joystick, button):
        """Joystick button press event when paused.

        See StellarClass.event_joystick_button_press.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_button_release(self, joystick, button):
        """Joystick button release event when paused.

        See StellarClass.event_joystick_button_release.__doc__ for more
        information.

        """
        pass

    def _update(self, time_passed, delta_mult):
        # Update this object (should be called each frame).
        # Update the animation frame.
        if self.image_fps:
            self._anim_count += time_passed
            self.image_index += int(self._anim_count // self._frame_time)
            self._anim_count %= self._frame_time

        # Alarms
        for a in self._alarms:
            self._alarms[a] -= delta_mult
            if self._alarms[a] <= 0:
                del self._alarms[a]
                self.event_alarm(a)

        # Movement
        if self.xvelocity or self.yvelocity:
            if self.id != "mouse":
                self.x += self.xvelocity * delta_mult
                self.y += self.yvelocity * delta_mult

            # Detect collisions
            if self.detects_collisions:
                for other_ref in game._colliders:
                    if other_ref() is not None:
                        other = other_ref()
                    else:
                        continue

                    if self.collides(other):
                        xcollision = not self.collides(other, x=self.xprevious)
                        ycollision = not self.collides(other, y=self.yprevious)

                        if xcollision and ycollision:
                            # Corner collision; determine
                            # direction by distance.
                            if self.xvelocity > 0:
                                xdepth = (self.bbox_right - other.bbox_left)
                            else:
                                xdepth = (other.bbox_right - self.bbox_left)

                            if self.yvelocity > 0:
                                ydepth = (self.bbox_bottom - other.bbox_top)
                            else:
                                ydepth = (other.bbox_bottom - self.bbox_top)

                            if xdepth > ydepth:
                                if self.xvelocity > 0:
                                    self.event_collision_right(other)
                                    other.event_collision_left(self)
                                else:
                                    self.event_collision_left(other)
                                    other.event_collision_right(self)
                            else:
                                if self.yvelocity > 0:
                                    self.event_collision_bottom(other)
                                    other.event_collision_top(self)
                                else:
                                    self.event_collision_top(other)
                                    other.event_collision_bottom(self)

                        elif xcollision:
                            # Horizontal collision only.
                            if self.xvelocity > 0:
                                self.event_collision_right(other)
                                other.event_collision_left(self)
                            else:
                                self.event_collision_left(other)
                                other.event_collision_right(self)

                        elif ycollision:
                            # Vertical collision only.
                            if self.yvelocity > 0:
                                self.event_collision_bottom(other)
                                other.event_collision_top(self)
                            else:
                                self.event_collision_top(other)
                                other.event_collision_bottom(self)

                        elif not self.collides(other, self.xprevious,
                                               self.yprevious):
                            # Wedge collision (both vertical and
                            # horizontal collisions).
                            if self.xvelocity > 0:
                                self.event_collision_right(other)
                                other.event_collision_left(self)
                            else:
                                self.event_collision_left(other)
                                other.event_collision_right(self)
                            if self.yvelocity > 0:
                                self.event_collision_bottom(other)
                                other.event_collision_top(self)
                            else:
                                self.event_collision_top(other)
                                other.event_collision_bottom(self)

                        else:
                            # No directional collision; this is
                            # a continuous collision.
                            self.event_collision(other)
                            other.event_collision(self)

    def _set_mask(self):
        # Properly set the hit mask based on the collision settings.
        if self.collision_precise:
            # Mask based on opacity of the current image.
            left = self.bbox_x + self.sprite.origin_x
            right = left + self.bbox_width
            top = self.bbox_y + self.sprite.origin_y
            bottom = top + self.bbox_height

            mask = self.sprite._get_precise_mask(self.image_index)[left:right]
            for i in xrange(len(mask)):
                mask[i] = mask[i][top:bottom]

            self._hitmask = mask
        elif self.collision_ellipse:
            # Elliptical mask based on bounding box.
            self._hitmask = [[False for y in xrange(self.bbox_height)]
                             for x in xrange(self.bbox_width)]
            a = len(self._hitmask) / 2
            b = len(self._hitmask[0]) / 2
            for x in xrange(len(self._hitmask)):
                for y in xrange(len(self._hitmask[x])):
                    if ((x - a) / a) ** 2 + ((y - b) / b) ** 2 <= 1:
                        self._hitmask[x][y] = True
        else:
            # Mask is all pixels in the bounding box.
            self._hitmask = [[True for y in xrange(self.bbox_height)]
                             for x in xrange(self.bbox_width)]

    def _set_speed(self):
        # Set the speed and move direction based on xvelocity and
        # yvelocity.
        self._speed = math.sqrt(self._xvelocity ** 2 + self._yvelocity ** 2)

        if self._yvelocity == 0:
            base_angle = 0
        elif self._xvelocity == 0:
            base_angle = 90
        else:
            base_angle = math.degrees(math.atan(abs(self._yvelocity) /
                                                abs(self._xvelocity)))

        if self._xvelocity < 0 and self._yvelocity < 0:
            self._move_direction += 180
        elif self._xvelocity < 0:
            self._move_direction = 180 - base_angle
        elif self._yvelocity < 0:
            self._move_direction = 360 - base_angle
        else:
            self._move_direction = base_angle

        self._move_direction %= 360

    def _reset(self):
        # Reset the object back to its original state.
        self.x = self._start_x
        self.y = self._start_y
        self.z = self._start_z
        self.sprite = self._start_sprite
        self.visible = self._start_visible
        self.detects_collisions = self._start_detects_collisions
        self.bbox_x = self._start_bbox_x
        self.bbox_y = self._start_bbox_y
        self.bbox_width = self._start_bbox_width
        self.bbox_height = self._start_bbox_height
        self.collision_ellipse = self._start_collision_ellipse
        self.collision_precise = self._start_collision_precise


class Mouse(StellarClass):

    @property
    def x(self):
        if game.current_room is not None:
            mouse_x = self.mouse_x / game._xscale
            mouse_y = self.mouse_y / game._yscale
            for view in game.current_room.views:
                if (view.xport <= mouse_x <= view.xport + view.width and
                        view.yport <= mouse_y <= view.yport + view.height):
                    # We save this value so that if the mouse is in none of
                    # the views, the last known position in a view is used.
                    self._x = mouse_x - view.x
                    break

            return self._x
        else:
            return 0

    @x.setter
    def x(self, value):
        rel_x = (value - self.x) * game._xscale
        self.mouse_x += rel_x

        self.xprevious = self._x
        self._x = value
        self._bbox_left = value + self.bbox_x
        self._bbox_right = self.bbox_left + self.bbox_width

        # Cause the Pygame sprite to make itself dirty
        self._pygame_sprite.rect = pygame.Rect(0, 0, 1, 1)

        pygame.mouse.set_pos(self.mouse_x, self.mouse_y)

    @property
    def y(self):
        if game.current_room is not None:
            mouse_x = self.mouse_x / game._xscale
            mouse_y = self.mouse_y / game._yscale
            for view in game.current_room.views:
                if (view.xport <= mouse_x <= view.xport + view.width and
                        view.yport <= mouse_y <= view.yport + view.height):
                    # We save this value so that if the mouse is in none of
                    # the views, the last known position in a view is used.
                    self._y = mouse_y - view.y
                    break

            return self._y
        else:
            return 0

    @y.setter
    def y(self, value):
        rel_y = (value - self.y) * game._yscale
        self.mouse_y += rel_y

        self.yprevious = self._y
        self._y = value
        self._bbox_top = value + self.bbox_y
        self._bbox_bottom = self.bbox_top + self.bbox_height

        # Cause the Pygame sprite to make itself dirty
        self._pygame_sprite.rect = pygame.Rect(0, 0, 1, 1)

        pygame.mouse.set_pos(self.mouse_x, self.mouse_y)

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, value):
        if isinstance(value, Sprite) or value is None:
            self._sprite = value
        else:
            self._sprite = game.sprites[value]

        self.set_cursor()

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value
        self.set_cursor()

    def __init__(self):
        self._visible = True
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.mouse_xprevious = self.mouse_x
        self.mouse_yprevious = self.mouse_y
        self.previous_speeds = []
        super(Mouse, self).__init__(0, 0, 0, id='mouse')

    def event_collision(self, other):
        game.event_mouse_collision(other)

    def event_collision_left(self, other):
        game.event_mouse_collision_left(other)

    def event_collision_right(self, other):
        game.event_mouse_collision_right(other)

    def event_collision_top(self, other):
        game.event_mouse_collision_top(other)

    def event_collision_bottom(self, other):
        game.event_mouse_collision_bottom(other)

    def _update(self, time_passed, delta_mult):
        self.update_speed(time_passed)
        super(Mouse, self)._update(time_passed, delta_mult)

    def update_speed(self, time_passed):
        # Update the speed variables.  ``time_passed`` is the number of
        # milliseconds since the last speed update.
        self.previous_speeds.insert(0, (self.mouse_x - self.mouse_xprevious,
                                        self.mouse_y - self.mouse_yprevious,
                                        time_passed))
        time = 0
        num_steps = 0
        total_xvelocity = 0
        total_yvelocity = 0

        for speed in self.previous_speeds:
            time += speed[2]
            if time <= 250:
                num_steps += 1
                total_xvelocity += speed[0]
                total_yvelocity += speed[1]

        self.previous_speeds = self.previous_speeds[:num_steps]

        if num_steps > 0:
            self.xvelocity = total_xvelocity / num_steps
            self.yvelocity = total_yvelocity / num_steps
        else:
            self.xvelocity = 0
            self.yvelocity = 0

        self.mouse_xprevious = self.mouse_x
        self.mouse_yprevious = self.mouse_y
        self.xprevious = self.x
        self.yprevious = self.y

    def set_cursor(self):
        # Set the mouse cursor and visibility state.
        if not game.grab_input:
            pygame.mouse.set_visible(self.visible and self.sprite is None)
        else:
            pygame.mouse.set_visible(False)


class Room(object):

    """Class for rooms.

    All Room objects have the following attributes:
        width: The width of the room in pixels.
        height: The height of the room in pixels.
        views: A list containing all View objects in the room.
        background: The Background object used.  While it will always be
            the actual object when read, it can be set to either an
            actual background object or the ID of a background.

    The following read-only attributes are also available:
        objects: A tuple containing all StellarClass objects in the
            room.
        room_number: The index of this room in the game, where 0 is the
            first room, or None if this room has not been added to a
            game.

    Room methods:
        add: Add a StellarClass object to the room.
        start: Start the room.
        resume: Continue the room from where it left off.
        end: Go to the next room.

    Room events are handled by special methods.  The exact timing of
    their calling is implementation-dependent except where otherwise
    noted.  The methods are:
        event_room_start: Called when the room starts.  It is always
            called after any game start events and before any object
            create events occurring at the same time.
        event_step: Called once each frame.
        event_key_press: Key press event.
        event_key_release: Key release event.
        event_mouse_move: Mouse move event.
        event_mouse_button_press: Mouse button press event.
        event_mouse_button_release: Mouse button release event.
        event_joystick_axis_move: Joystick axis move event.
        event_joystick_hat_move: Joystick HAT move event.
        event_joystick_button_press: Joystick button press event.
        event_joystick_button_release: Joystick button release event.
        event_close: Close event (e.g. close button).  It is always
            called before any game close events occurring at the same
            time.
        event_room_end: Called when the room ends.  It is always called
            before any game end events occurring at the same time.

    The following alternative events are executed when the game is
    paused in place of the corresponding normal events:
        event_paused_key_press
        event_paused_key_release
        event_paused_mouse_move
        event_paused_mouse_button_press
        event_paused_mouse_button_release
        event_paused_joystick_axis_move
        event_paused_joystick_hat_move
        event_paused_joystick_button_press
        event_paused_joystick_button_release
        event_paused_close

    """

    def __init__(self, objects=(), width=640, height=480, views=None,
                 background=None):
        """Create a new Room object.

        Arguments set the properties of the room.  See Room.__doc__ for
        more information.

        If ``views`` is set to None, a new view will be  created with
        x=0, y=0, and all other arguments unspecified, which will become
        the first view of the room.  If ``background`` is set to None, a
        new background is created with no layers and the color set to
        "black".

        In addition to containing actual StellarClass objects,
        ``objects`` can contain valid IDs of StellarClass objects.

        A game object must exist before an object of this class is
        created.

        """
        self.width = width
        self.height = height
        self._start_width = width
        self._start_height = height

        if views is not None:
            self.views = list(views)
        else:
            self.views = [View(0, 0)]
        self._start_views = self.views[:]

        if background is not None:
            self.background = background
        else:
            self.background = Background((), 'black')
        self._start_background = self.background

        self.room_number = len(game.rooms)
        game.rooms.append(self)

        self._started = False

        self.objects = ()
        self.add(game.mouse)
        for obj in objects:
            self.add(obj)
        self._start_objects = self.objects

    def add(self, obj):
        """Add a StellarClass object to the room.

        ``obj`` is the StellarClass object to add.  It can also be an
        object's ID.

        """
        if not isinstance(obj, StellarClass):
            obj = game.objects[obj]

        if obj not in self.objects:
            new_objects = list(self.objects)
            new_objects.append(obj)
            self.objects = tuple(new_objects)
            game._pygame_sprites.add(obj._pygame_sprite, layer=obj.z)
            if game.current_room is self and self._started:
                obj.event_create()

    def start(self):
        """Start the room.

        If the room has been changed, reset it to its original state.

        """
        self._reset()
        self.resume()

    def resume(self):
        """Continue the room from where it left off.

        If the room is unchanged (e.g. has not been started yet), this
        method behaves in the same way that Room.start does.

        """
        for sprite in game._pygame_sprites:
            sprite.kill()

        game.current_room = self
        game._background_changed = True

        for obj in self.objects:
            game._pygame_sprites.add(obj._pygame_sprite, layer=obj.z)

        if not self._started:
            self.event_room_start()
            for obj in self.objects:
                obj.event_create()

        self._started = True

    def end(self, next_room=None, resume=True):
        """End the current room.

        ``next_room`` indicates the room number of the room to go to
        next; if set to None, the room after this one is chosen.
        ``resume`` indicates whether or not to resume the next room
        instead of restarting it.  If the room chosen as the next room
        does not exist, the game is ended.

        This triggers this room's ``event_room_end`` and resets the
        state of this room.

        """
        self.event_room_end()
        self._reset()

        if next_room is None:
            next_room = self.room_number + 1

        if next_room >= -len(game.rooms) and next_room < len(game.rooms):
            if resume:
                game.rooms[next_room].resume()
            else:
                game.rooms[next_room].start()
        else:
            game.end()

    def event_room_start(self):
        """Room start event.

        Called when the room starts.  It is always called after any game
        start events and before any object create events occurring at
        the same time.

        """
        pass

    def event_room_end(self):
        """Room end event.

        Called when the room ends.  It is always called before any game
        end events occurring at the same time.

        """
        pass

    def event_step(self, time_passed):
        """Room step event.

        Called once each frame.  ``time_passed`` is the number of
        milliseconds that have passed during the last frame. 

        """
        pass

    def event_key_press(self, key):
        """Key press event.

        ``key`` is the key that was pressed.

        """
        pass

    def event_key_release(self, key):
        """Key release event.

        ``key`` is the key that was pressed.

        """
        pass

    def event_mouse_move(self, x, y):
        """Mouse move event.

        ``x`` and ``y`` indicate the relative movement of the mouse.

        """
        pass

    def event_mouse_button_press(self, button):
        """Mouse button press event.

        ``button`` is the number of the mouse button that was pressed;
        these numbers may vary by implementation, so MOUSE_BUTTON_*
        constants should be used.

        """
        pass

    def event_mouse_button_release(self, button):
        """Mouse button release event.

        ``button`` is the number of the mouse button that was released;
        these numbers may vary by implementation, so MOUSE_BUTTON_*
        constants should be used.

        """
        pass

    def event_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``axis`` is the number of the axis, where 0 is the
        first axis.  ``value`` is the tilt of the axis, where 0 is in
        the center, -1 is tilted all the way to the left or up, and 1 is
        tilted all the way to the right or down.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``hat`` is the number of the HAT, where 0 is the
        first HAT.  ``x`` and ``y`` indicate the position of the HAT,
        where 0 is in the center, -1 is left or up, and 1 is right or
        down.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_joystick_button_press(self, joystick, button):
        """Joystick button press event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``button`` is the number of the button pressed, where
        0 is the first button.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_joystick_button_release(self, joystick, button):
        """Joystick button release event.

        ``joystick`` is the number of the joystick, where 0 is the first
        joystick.  ``button`` is the number of the button pressed, where
        0 is the first button.

        Support for joysticks in Stellar Game Engine implementations is
        optional.

        """
        pass

    def event_close(self):
        """Close event (e.g. close button).

        It is always called before any game close events occurring at
        the same time.

        """
        pass

    def event_paused_key_press(self, key):
        """Key press event when paused.

        See Room.event_key_press.__doc__ for more information.

        """
        pass

    def event_paused_key_release(self, key):
        """Key release event when paused.

        See Room.event_key_release.__doc__ for more information.

        """
        pass

    def event_paused_mouse_move(self, x, y):
        """Mouse move event when paused.

        See Room.event_mouse_move.__doc__ for more information.

        """
        pass

    def event_paused_mouse_button_press(self, button):
        """Mouse button press event when paused.

        See Room.event_mouse_button_press.__doc__ for more information.

        """
        pass

    def event_paused_mouse_button_release(self, button):
        """Mouse button release event when paused.

        See Room.event_mouse_button_release.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_axis_move(self, joystick, axis, value):
        """Joystick axis move event when paused.

        See Room.event_joystick_axis_move.__doc__ for more information.

        """
        pass

    def event_paused_joystick_hat_move(self, joystick, hat, x, y):
        """Joystick HAT move event when paused.

        See Room.event_joystick_hat_move.__doc__ for more information.

        """
        pass

    def event_paused_joystick_button_press(self, joystick, button):
        """Joystick button press event when paused.

        See Room.event_joystick_button_press.__doc__ for more
        information.

        """
        pass

    def event_paused_joystick_button_release(self, joystick, button):
        """Joystick button release event when paused.

        See Room.event_joystick_button_release.__doc__ for more
        information.

        """
        pass

    def event_paused_close(self):
        """Close event (e.g. close button) when paused.

        See Room.event_close.__doc__ for more information.

        """
        pass

    def _reset(self):
        # Reset the room to its original state.
        self._started = False
        self.width = self._start_width
        self.height = self._start_height
        self.views = self._start_views
        self.background = self._start_background
        self.objects = self._start_objects

        for view in self.views:
            view._reset()

        for obj in self.objects:
            obj._reset()


class View(object):

    """Class for room views.

    All View objects have the following attributes:
        x: The horizontal position of the view in the room, where the
            left edge is 0 and x increases toward the right.
        y: The vertical position of the view in the room, where the top
            edge is 0 and y increases toward the bottom.
        xport: The horizontal position of the view on the screen, where
            the left edge is 0 and xport increases toward the right.
        yport: The vertical position of the view on the screen, where
            the top edge is 0 and yport increases toward the bottom.
        width: The width of the view in pixels.
        height: The height of the view in pixels.

    """

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if self._x != value:
            self._x = value
            game._background_changed = True

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if self._y != value:
            self._y = value
            game._background_changed = True

    @property
    def xport(self):
        return self._xport

    @xport.setter
    def xport(self, value):
        if self._xport != value:
            self._xport = value
            game._background_changed = True

    @property
    def yport(self):
        return self._yport

    @yport.setter
    def yport(self, value):
        if self._yport != value:
            self._yport = value
            game._background_changed = True

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if self._width != value:
            self._width = value
            game._background_changed = True

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if self._height != value:
            self._height = value
            game._background_changed = True

    def __init__(self, x, y, xport=0, yport=0, width=None, height=None):
        """Create a new View object.

        Arguments set the properties of the view.  See View.__doc__ for
        more information.

        If ``width`` or ``height`` is set to None, the respective size
        will be set such that the view takes up all of the space that it
        can (i.e. game.width - xport or game.height - yport).

        """
        self._x = x
        self._y = y
        self._xport = xport
        self._yport = yport
        self._width = width if width else game.width - xport
        self._height = height if height else game.height - yport
        self._start_x = self.x
        self._start_y = self.y
        self._start_xport = self.xport
        self._start_yport = self.yport
        self._start_width = self.width
        self._start_height = self.height

    def _reset(self):
        # Reset the view to its original state.
        self.x = self._start_x
        self.y = self._start_y
        self.xport = self._start_xport
        self.yport = self._start_yport
        self.width = self._start_width
        self.height = self._start_height


class _PygameSprite(pygame.sprite.DirtySprite):

    # Handles drawing in this implementation.
    #
    # Scaling is handled transparently in the update method, which is
    # always called before drawing.  Everything else is the
    # responsibility of StellarClass, including animation (the current
    # frame is grabbed from the _image attribute of the parent object).

    def __init__(self, parent, *groups):
        # See pygame.sprite.DirtySprite.__init__.__doc__.  ``parent``
        # is a StellarClass object that this object belongs to.
        super(_PygameSprite, self).__init__(*groups)
        self.parent = weakref.ref(parent)
        self.image = pygame.Surface((1, 1))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.x_offset = 0
        self.y_offset = 0

    def update(self):
        if self.parent() is not None:
            parent = self.parent()
            if parent.sprite is not None:
                new_image = parent.sprite._get_image(
                    parent.image_index, parent.image_xscale,
                    parent.image_yscale, parent.image_rotation,
                    parent.image_alpha, parent.image_blend)
                if self.image is not new_image:
                    self.must_redraw = False
                    self.image = new_image
                    self.dirty = 1

                    if parent.image_rotation % 90 != 0:
                        # Be prepared for size adjustment
                        rot_size = self.image.get_size()
                        reg_size = parent.sprite._get_image(
                            parent.image_index, parent.image_xscale,
                            parent.image_yscale).get_size()
                        self.x_offset = (rot_size[0] - reg_size[0]) // 2
                        self.y_offset = (rot_size[1] - reg_size[1]) // 2
                    else:
                        self.x_offset = 0
                        self.y_offset = 0

                if self.visible != self.parent().visible:
                    self.visible = int(self.parent().visible)
                    self.dirty = 1

                self.update_rect(parent.x, parent.y, parent.z, parent.sprite)
            else:
                self.image = pygame.Surface((1, 1))
                self.image.set_colorkey((0, 0, 0))
                self.dirty = 1
        else:
            self.kill()

    def update_rect(self, x, y, z, sprite):
        # Update the rect of this Pygame sprite, based on the SGE sprite
        # and coordinates given.  This involves creating "proxy"
        # one-time sprites for multiple views if necessary.
        views = game.current_room.views
        if (len(views) == 1 and views[0].xport == 0 and views[0].yport == 0 and
                views[0].width == game.width and
                views[0].height == game.height):
            # There is only one view that takes up the whole screen, so
            # we don't need to worry about it.
            x = x - views[0].x - sprite.origin_x
            y = y - views[0].y - sprite.origin_y
            new_rect = self.image.get_rect()
            new_rect.left = round(x * game._xscale) - self.x_offset + game._x
            new_rect.top = round(y * game._yscale) - self.y_offset + game._y

            if self.rect != new_rect:
                self.rect = new_rect
                self.dirty = 1
        else:
            # There is something more complicated.  Have to account for
            # the possibility of edges or multiple appearances.
            original_used = False
            self.dirty = 1
            real_x = x
            real_y = y
            for view in views:
                x = real_x - view.x - sprite.origin_x + view.xport
                y = real_y - view.y - sprite.origin_y + view.yport
                w = max(1, self.image.get_width())
                h = max(1, self.image.get_height())
                new_rect = self.image.get_rect()
                new_rect.left = (round(x * game._xscale) - self.x_offset +
                                 game._x)
                new_rect.top = (round(y * game._yscale) - self.y_offset +
                                game._y)
                inside_view = (x >= view.xport and
                               x + w <= view.xport + view.width and
                               y >= view.yport and
                               y + h <= view.yport + view.height)
                within_view = (x + w >= view.xport and
                               x <= view.xport + view.width and
                               y + h >= view.yport and
                               y <= view.yport + view.height)

                if not original_used and inside_view:
                    original_used = True
                    if self.rect == new_rect:
                        self.dirty = 0
                    else:
                        self.rect = new_rect
                elif within_view:
                    if inside_view:
                        img = self.image
                        rect = new_rect
                    else:
                        # Make a cut-off version of the sprite and
                        # adjust the rect accordingly.
                        if x < view.xport:
                            cut_x = view.xport - x
                            x = view.xport
                            w -= cut_x
                        else:
                            cut_x = 0

                        if x + w > view.xport + view.width:
                            w -= (x + w) - (view.xport + view.width)

                        if y < view.yport:
                            cut_y = view.yport - y
                            y = view.yport
                            h -= cut_y
                        else:
                            cut_y = 0

                        if y + h > view.yport + view.height:
                            h -= (y + h) - (view.yport + view.height)

                        x = round(x * game._xscale) - self.x_offset
                        y = round(y * game._yscale) - self.y_offset
                        cut_x = round(cut_x * game._xscale)
                        cut_y = round(cut_y * game._yscale)
                        w = round(w * game._xscale)
                        h = round(h * game._yscale)
                        cut_rect = pygame.Rect(cut_x, cut_y, w, h)
                        img = self.image.subsurface(cut_rect)
                        rect = pygame.Rect(x, y, w, h)

                    # Create proxy one-time sprite
                    proxy = _PygameOneTimeSprite(img, rect)
                    game._pygame_sprites.add(proxy, layer=z)

            if not original_used:
                self.image = pygame.Surface((1, 1))
                self.image.set_colorkey((0, 0, 0))


class _PygameOneTimeSprite(pygame.sprite.DirtySprite):

    # A regular DirtySprite that only displays once, and then destroys
    # itself.

    def __init__(self, image, rect, *groups):
        super(_PygameOneTimeSprite, self).__init__(*groups)
        self.image = image
        self.rect = rect
        self.dirty = 1

    def update(self):
        if not self.dirty:
            self.kill()


class _FakeFont(object):

    # Fake copy of Font for when pygame.font is not available.

    def __init__(self, name=None, size=12, underline=False, bold=False,
                 italic=False):
        self.name = name
        self.size = size
        self.underline = underline
        self.bold = bold
        self.italic = italic

    def render(self, text, x, y, width=None, height=None, color="black",
               halign=ALIGN_LEFT, valign=ALIGN_TOP, anti_alias=True):
        print(text)

    def get_size(self, text, x, y, width=None, height=None):
        return (1, 1)


def create_object(cls, *args, **kwargs):
    """Create an object in the current room.

    ``cls`` is the class (derived from StellarClass) to create an object
    of.  ``args`` and ``kwargs`` are passed on to cls.__init__ as
    arguments.

    Calling this function is equivalent to:
        sge.game.current_room.add(cls(*args, **kwargs))

    """
    game.current_room.add(cls(*args, **kwargs))


def sound_stop_all():
    """Stop playback of all sounds."""
    for i in game.sounds:
        game.sounds[i].stop()


def music_clear_queue():
    """Clear the music queue."""
    game._music_queue = []


def music_stop_all():
    """Stop playback of any music and clear the queue."""
    for i in game.music:
        game.music[i].stop()

    music_clear_queue()


def get_key_pressed(key):
    """Return whether or not a given key is pressed.

    ``key`` is the key to check.

    """
    key = key.lower()
    if key in KEYS:
        return pygame.key.get_pressed()[KEYS[key]]
    else:
        return False


def get_mouse_button_pressed(button):
    """Return whether or not a given mouse button is pressed.

    ``button`` is the number of the mouse button to check, where 0
    is the first mouse button.

    """
    if button < 3:
        return pygame.mouse.get_pressed()[button]
    else:
        return False


def get_joystick_axis(joystick, axis):
    """Return the position of the given axis.

    ``joystick`` is the number of the joystick to check, where 0 is
    the first joystick.  ``axis`` is the number of the axis to
    check, where 0 is the first axis of the joystick.

    Returned value is a float from -1 to 1, where 0 is centered, -1
    is all the way to the left or up, and 1 is all the way to the
    right or down.

    If the joystick or axis requested does not exist, 0 is returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will act like the joystick requested
    does not exist.

    """
    if joystick < len(game._joysticks):
        numaxes = game._joysticks[joystick].get_numaxes()
        if axis < numaxes:
            return game._joysticks[joystick].get_axis(axis)
        else:
            ball = (axis - numaxes) // 2
            direction = (axis - numaxes) % 2
            if ball < game._joysticks[joystick].get_numballs():
                return game._joysticks[joystick].get_ball(ball)[direction]
    else:
        return 0


def get_joystick_hat(joystick, hat):
    """Return the position of the given HAT.

    ``joystick`` is the number of the joystick to check, where 0 is
    the first joystick.  ``hat`` is the number of the HAT to check,
    where 0 is the first HAT of the joystick.

    Returned value is a tuple in the form (x, y), where x is the
    horizontal position and y is the vertical position.  Both x and
    y are 0 (centered), -1 (left or up), or 1 (right or down).

    If the joystick or HAT requested does not exist, (0, 0) is
    returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will act like the joystick requested
    does not exist.

    """
    if joystick < len(game._joysticks):
        if hat < game._joysticks[joystick].get_numhats():
            return game._joysticks[joystick].get_hat(hat)
    else:
        return (0, 0)


def get_joystick_button_pressed(joystick, button):
    """Return whether or not the given button is pressed.

    ``joystick`` is the number of the joystick to check, where 0 is
    the first joystick.  ``button`` is the number of the button to
    check, where 0 is the first button of the joystick.

    If the joystick or button requested does not exist, False is
    returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will act like the joystick requested
    does not exist.

    """
    if joystick < len(game._joysticks):
        if button < game._joysticks[joystick].get_numbuttons():
            return game._joysticks[joystick].get_button(button)
    else:
        return False


def get_joysticks():
    """Return the number of joysticks available.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will always return 0.

    """
    return len(game._joysticks)


def get_joystick_axes(joystick):
    """Return the number of axes available on the given joystick.

    ``joystick`` is the number of the joystick to check, where 0 is
    the first joystick.  If the given joystick does not exist, 0
    will be returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will act like the joystick requested
    does not exist.

    """
    if joystick < len(game._joysticks):
        return (game._joysticks[joystick].get_numaxes() +
                game._joysticks[joystick].get_numballs() * 2)
    else:
        return 0


def get_joystick_hats(joystick):
    """Return the number of HATs available on the given joystick.

    ``joystick`` is the number of the joystick to check, where 0 is
    the first joystick.  If the given joystick does not exist, 0
    will be returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will act like the joystick requested
    does not exist.

    """
    if joystick < len(game._joysticks):
        return game._joysticks[joystick].get_numhats()
    else:
        return 0


def get_joystick_buttons(joystick):
    """Return the number of buttons available on the given joystick.

    ``joystick`` is the number of the joystick to check, where 0 is
    the first joystick.  If the given joystick does not exist, 0
    will be returned.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will act like the joystick requested
    does not exist.

    """
    if joystick < len(game._joysticks):
        return game._joysticks[joystick].get_numbuttons()
    else:
        return 0


def _scale(surface, width, height):
    # Scale the given surface to the given width and height, taking the
    # scale factor of the screen into account.
    width = int(round(width * game._xscale))
    height = int(round(height * game._yscale))

    if game.scale_smooth:
        try:
            new_surf = pygame.transform.smoothscale(surface, (width, height))
        except pygame.error:
            new_surf = pygame.transform.scale(surface, (width, height))
    else:
        new_surf = pygame.transform.scale(surface, (width, height))

    return new_surf


def _get_pygame_color(color):
    # Return the proper Pygame color.
    if isinstance(color, basestring):
        c = color.lower()
        if c in COLORS:
            c = COLORS[c]

        return pygame.Color(bytes(c))
    elif isinstance(color, int):
        r = int((color & 0xff0000) // (256 ** 2))
        g = int((color & 0x00ff00) // 256)
        b = color & 0x0000ff
        return pygame.Color(r, g, b)
    else:
        try:
            while len(color) < 3:
                color.append(0)
            return pygame.Color(*color[:4])
        except TypeError:
            return pygame.Color(color)
