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


__all__ = ['Font', '_FakeFont']


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

        for path in sge.font_directories:
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
