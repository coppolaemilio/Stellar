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

import sge


__all__ = ['BackgroundLayer']


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
        if not isinstance(value, sge.Sprite):
            value = sge.game.sprites[value]

        if self._sprite != value:
            self._sprite = value
            sge.game._background_changed = True

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if self._x != value:
            self._x = value
            sge.game._background_changed = True

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if self._y != value:
            self._y = value
            sge.game._background_changed = True

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        if self._z != value:
            self._z = value
            sge.game._background_changed = True

    @property
    def xscroll_rate(self):
        return self._xscroll_rate

    @xscroll_rate.setter
    def xscroll_rate(self, value):
        if self._xscroll_rate != value:
            self._xscroll_rate = value
            sge.game._background_changed = True

    @property
    def yscroll_rate(self):
        return self._yscroll_rate

    @yscroll_rate.setter
    def yscroll_rate(self):
        if self._yscroll_rate != value:
            self._yscroll_rate = value
            sge.game._background_changed = True

    @property
    def xrepeat(self):
        return self._xrepeat

    @xrepeat.setter
    def xrepeat(self, value):
        if self._xrepeat != value:
            self._xrepeat = value
            sge.game._background_changed = True

    @property
    def yrepeat(self):
        return self._yrepeat

    @yrepeat.setter
    def yrepeat(self, value):
        if self._yrepeat != value:
            self._yrepeat = value
            sge.game._background_changed = True

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
