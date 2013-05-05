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


__all__ = ['View']


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
    def xport(self):
        return self._xport

    @xport.setter
    def xport(self, value):
        if self._xport != value:
            self._xport = value
            sge.game._background_changed = True

    @property
    def yport(self):
        return self._yport

    @yport.setter
    def yport(self, value):
        if self._yport != value:
            self._yport = value
            sge.game._background_changed = True

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if self._width != value:
            self._width = value
            sge.game._background_changed = True

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if self._height != value:
            self._height = value
            sge.game._background_changed = True

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
        self._width = width if width else sge.game.width - xport
        self._height = height if height else sge.game.height - yport
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
