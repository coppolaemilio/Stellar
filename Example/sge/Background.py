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


__all__ = ['Background']


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
            while id_ in sge.game.backgrounds:
                id_ += 1
            self.id = id_

        sge.game.backgrounds[self.id] = self

        unsorted_layers = []
        sorted_layers = []

        for layer in layers:
            if isinstance(layer, sge.BackgroundLayer):
                unsorted_layers.append(layer)
            else:
                if layer in sge.game.background_layers:
                    unsorted_layers.append(sge.game.background_layers[layer])

        for layer in unsorted_layers:
            i = 0
            while i < len(sorted_layers) and layer.z >= sorted_layers[i].z:
                i += 1

            sorted_layers.insert(i, layer)

        self.layers = tuple(sorted_layers)

    def _get_background(self):
        # Return the static background this frame.
        background = pygame.Surface((round(sge.game.width * sge.game._xscale),
                                     round(sge.game.height * sge.game._yscale)))
        background.fill(sge._get_pygame_color(self.color))

        for view in sge.game.current_room.views:
            view_x = int(round(view.x * sge.game._xscale))
            view_y = int(round(view.y * sge.game._yscale))
            view_xport = max(0, min(int(round(view.xport * sge.game._xscale)),
                                    background.get_width() - 1))
            view_yport = max(0, min(int(round(view.yport * sge.game._yscale)),
                                    background.get_height() - 1))
            view_w = min(int(round((sge.game.width - view.xport) *
                                   sge.game._xscale)),
                         background.get_width() - view_xport)
            view_h = min(int(round((sge.game.height - view.yport) *
                                   sge.game._yscale)),
                         background.get_height() - view_yport)
            surf = background.subsurface(view_xport, view_yport, view_w,
                                         view_h)
            for layer in self.layers:
                image = layer._get_image()
                x = int(round((layer.x - (view.x * layer.xscroll_rate)) *
                              sge.game._xscale))
                y = int(round((layer.y - (view.y * layer.yscroll_rate)) *
                              sge.game._yscale))
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
