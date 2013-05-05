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


__all__ = ['Sprite']


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
        for d in sge.image_directories:
            print(os.path.normpath(os.path.abspath(d)))

        if name is not None:
            for path in sge.image_directories:
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
            while "{0}_{1}N".format(prefix, i) in sge.game.sprites:
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
            if sge.game.scale_smooth:
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
        sge.game.sprites[self.name] = self

    def draw_dot(self, x, y, color, frame=None):
        """Draw a single-pixel dot.

        ``x`` and ``y`` indicate the location in the sprite to draw the
        dot, where x=0, y=0 is the origin and x and y increase toward
        the right and bottom, respectively.  ``color`` indicates the
        color of the dot.  ``frame`` indicates the frame of the sprite
        to draw on, where 0 is the first frame; set to None to draw on
        all frames.

        """
        color = sge._get_pygame_color(color)
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
        color = sge._get_pygame_color(color)
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
                    self._baseimages[i].fill(sge._get_pygame_color(fill), rect)

                if outline is not None:
                    pygame.draw.rect(self._baseimages[i],
                                     sge._get_pygame_color(outline), rect,
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
                    c = sge._get_pygame_color(fill)
                    pygame.draw.ellipse(self._baseimages[i], c, rect)

                if outline is not None:
                    c = sge._get_pygame_color(outline)
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
                    c = sge._get_pygame_color(fill)
                    pygame.draw.circle(self._baseimages[i], c, (x, y), radius)

                if outline is not None:
                    c = sge._get_pygame_color(outline)
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
                  color="black", halign=sge.ALIGN_LEFT, valign=sge.ALIGN_TOP,
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
        if not isinstance(font, sge.Font):
            font = sge.game.fonts[font]

        lines = font._split_text(text, width)
        width, height = font.get_size(text, width, height)
        fake_height = font.get_size(text, width)[1]
        color = sge._get_pygame_color(color)

        text_surf = pygame.Surface((width, fake_height), pygame.SRCALPHA)
        box_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        text_rect = text_surf.get_rect()
        box_rect = box_surf.get_rect()

        for i in xrange(len(lines)):
            rendered_text = font._font.render(lines[i], anti_alias, color)
            rect = rendered_text.get_rect()
            rect.top = i * font._font.get_linesize()

            if halign == sge.ALIGN_LEFT:
                rect.left = text_rect.left
            elif halign == sge.ALIGN_RIGHT:
                rect.right = text_rect.right
            elif halign == sge.ALIGN_CENTER:
                rect.centerx = text_rect.centerx

            text_surf.blit(rendered_text, rect)

        if valign == sge.ALIGN_TOP:
            text_rect.top = box_rect.top
        elif valign == sge.ALIGN_BOTTOM:
            text_rect.bottom = box_rect.bottom
        elif valign == sge.ALIGN_MIDDLE:
            text_rect.centery = box_rect.centery

        box_surf.blit(text_surf, text_rect)

        if halign == sge.ALIGN_LEFT:
            box_rect.left = x
        elif halign == sge.ALIGN_RIGHT:
            box_rect.right = x
        elif halign == sge.ALIGN_CENTER:
            box_rect.centerx = x
        else:
            box_rect.left = x

        if valign == sge.ALIGN_TOP:
            box_rect.top = y
        elif valign == sge.ALIGN_BOTTOM:
            box_rect.bottom = y
        elif valign == sge.ALIGN_MIDDLE:
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
        sge.game._background_changed = True
        self._images = []
        for image in self._baseimages:
            img = self._set_transparency(image)
            img = sge._scale(img, self.width, self.height)
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
                img = sge._scale(img, self.width * abs(xscale),
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
                    img.fill(sge._get_pygame_color(blend), None,
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
