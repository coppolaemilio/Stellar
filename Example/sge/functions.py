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

import pygame

import sge


__all__ = ['get_key_pressed', 'get_mouse_button_pressed', 'get_joystick_axis',
           'get_joystick_hat', 'get_joystick_button_pressed', 'get_joysticks',
           'get_joystick_axes', 'get_joystick_hats', 'get_joystick_buttons',
           '_scale', '_get_pygame_color']


def get_key_pressed(key):
    """Return whether or not a given key is pressed.

    ``key`` is the key to check.

    """
    key = key.lower()
    if key in sge.KEYS:
        return pygame.key.get_pressed()[sge.KEYS[key]]
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
    if joystick < len(sge.game._joysticks):
        numaxes = sge.game._joysticks[joystick].get_numaxes()
        if axis < numaxes:
            return sge.game._joysticks[joystick].get_axis(axis)
        else:
            ball = (axis - numaxes) // 2
            direction = (axis - numaxes) % 2
            if ball < sge.game._joysticks[joystick].get_numballs():
                value =  sge.game._joysticks[joystick].get_ball(ball)[direction]

                if sge.real_trackballs:
                    return value
                else:
                    return max(-1, min(value, 1))
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
    if joystick < len(sge.game._joysticks):
        if hat < sge.game._joysticks[joystick].get_numhats():
            return sge.game._joysticks[joystick].get_hat(hat)
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
    if joystick < len(sge.game._joysticks):
        if button < sge.game._joysticks[joystick].get_numbuttons():
            return sge.game._joysticks[joystick].get_button(button)
    else:
        return False


def get_joysticks():
    """Return the number of joysticks available.

    Support for joysticks in Stellar Game Engine implementations is
    optional.  If the implementation used does not support
    joysticks, this function will always return 0.

    """
    return len(sge.game._joysticks)


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
    if joystick < len(sge.game._joysticks):
        return (sge.game._joysticks[joystick].get_numaxes() +
                sge.game._joysticks[joystick].get_numballs() * 2)
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
    if joystick < len(sge.game._joysticks):
        return sge.game._joysticks[joystick].get_numhats()
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
    if joystick < len(sge.game._joysticks):
        return sge.game._joysticks[joystick].get_numbuttons()
    else:
        return 0


def _scale(surface, width, height):
    # Scale the given surface to the given width and height, taking the
    # scale factor of the screen into account.
    width = int(round(width * sge.game._xscale))
    height = int(round(height * sge.game._yscale))

    if sge.game.scale_smooth:
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
        if c in sge.COLORS:
            c = sge.COLORS[c]

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
