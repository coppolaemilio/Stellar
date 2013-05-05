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

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os

import pygame

import sge


__all__ = ['Game']


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

        sge.game = self

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
        self.mouse = sge.Mouse()

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
                        k = sge.KEYNAMES[event.key]
                        self.event_key_press(k)
                        self.current_room.event_key_press(k)
                        for obj in self.current_room.objects:
                            obj.event_key_press(k)
                    elif event.type == pygame.KEYUP:
                        k = sge.KEYNAMES[event.key]
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
                        
                        if sge.real_trackballs:
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

                if sge.hardware_rendering:
                    pygame.display.flip()
                else:
                    pygame.display.update(dirty)

            self.event_game_end()
            pygame.quit()
            sge.game = None

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
                    k = sge.KEYNAMES[event.key]
                    self.event_paused_key_press(k)
                    self.current_room.event_paused_key_press(k)
                    for obj in self.current_room.objects:
                        obj.event_paused_key_press(k)
                elif event.type == pygame.KEYUP:
                    k = sge.KEYNAMES[event.key]
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

                    if sge.real_trackballs:
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

            if sge.hardware_rendering:
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
            if sge.hardware_rendering:
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
            if sge.hardware_rendering:
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
