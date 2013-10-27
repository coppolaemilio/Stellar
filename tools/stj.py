#!/usr/bin/env python2

# STJ - Stellar JSON Library
# Copyright (C) 2013 Julian Marchant <onpon4@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
This module contains functions to read and write Stellar JSON files.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys
import os
import json
import weakref
import warnings

CODE_TAB_WIDTH = 4
DOCSTRING_LINE_SIZE = 72


class StellarJSON(object):

    """Object representing a JSON file.

    Objects of this class represent the contents of a JSON file which
    has meta-data for a SGE game.

    .. attribute:: fname

       The name of the JSON file this object is associated with.

    .. attribute:: copyright_notice

       The copyright notice to be placed at the start of the Python code
       file as a string, without Python markup.

    .. attribute:: game_class

       The class to use to create the game object as a
       Python-interpretable string, valid within the context of
       generated Python code.

    .. attribute:: game_kwargs

       A list of :class:`Variable` objects indicating the keyword
       arguments to pass on to the game object.

    .. attribute:: modules

       A list of :class:`Module` objects indicating the Python modules
       to import.

    .. attribute:: constants

       A list of :class:`Variable` objects indicating global constants.

    .. attribute:: global_variables

       A list of :class:`Variable` objects indicating global variables.

    .. attribute:: classes

       A list of :class:`Class` objects indicating class definitions.

    .. attribute:: functions

       A list of :class:`Function` objects indicating function
       definitions.

    .. attribute:: sprites

       A list of :class:`Object` objects indicating sprites.  Their
       class is ``"sge.Sprite"`` by default.

    .. attribute:: background_layers

       A list of :class:`Object` objects indicating background layers.
       Their class is ``"sge.BackgroundLayer"`` by default.

    .. attribute:: backgrounds

       A list of :class:`Object` objects indicating backgrounds.  Their
       class is ``"sge.Background"`` by default.

    .. attribute:: sounds

       A list of :class:`Object` objects indicating sounds.  Their class
       is ``"sge.Sound"`` by default.

    .. attribute:: music

       A list of :class:`Object` objects indicating music.  Their class
       is ``"sge.Music"`` by default.

    .. attribute:: fonts

       A list of :class:`Object` objects indicating fonts.  Their class
       is ``"sge.Font"`` by default.

    .. attribute:: objects

       A list of :class:`Object` objects indicating global objects.

    .. attribute:: rooms

       A list of :class:`Room` objects indicating rooms.

    """

    def __init__(self, fname):
        self.fname = fname

        try:
            self.load()
        except IOError:
            self.copyright_notice = ""
            self.game_class = "sge.Game"
            self.game_kwargs = []
            self.modules = []
            self.constants = []
            self.global_variables = []
            self.classes = []
            self.functions = []
            self.sprites = []
            self.background_layers = []
            self.backgrounds = []
            self.sounds = []
            self.music = []
            self.fonts = []
            self.objects = []
            self.rooms = []

    def load(self):
        """Load the corresponding JSON file onto this object."""
        with open(self.fname, 'r') as f:
            data = json.load(f)

        self.copyright_notice = data.setdefault("copyright_notice", "")
        self.game_class = data.setdefault("game_class", "sge.Game")
        self.game_kwargs = []
        self.modules = []
        self.constants = []
        self.global_variables = []
        self.classes = []
        self.functions = []
        self.sprites = []
        self.background_layers = []
        self.backgrounds = []
        self.sounds = []
        self.music = []
        self.fonts = []
        self.objects = []
        self.rooms = []

        for kwarg in data.setdefault("game_kwargs", []):
            self.game_kwargs.append(Variable(self.fname, kwarg))

        for module in data.setdefault("modules", []):
            self.modules.append(Module(self.fname, module))

        for constant in data.setdefault("constants", []):
            self.constants.append(Variable(self.fname, constant))

        for global_variable in data.setdefault("global_variables", []):
            self.global_variables.append(Variable(self.fname, global_variable))

        for cls in data.setdefault("classes", []):
            self.classes.append(Class(self.fname, cls))

        for function in data.setdefault("functions", []):
            self.functions.append(Function(self.fname, function))

        for sprite in data.setdefault("sprites", []):
            self.sprites.append(Object(self.fname, sprite,
                                       default_class="sge.Sprite"))

        for background_layer in data.setdefault("background_layers", []):
            self.background_layers.append(
                Object(self.fname, background_layer,
                       default_class="sge.BackgroundLayer"))

        for background in data.setdefault("backgrounds", []):
            self.backgrounds.append(Object(self.fname, background,
                                           default_class="sge.Background"))

        for sound in data.setdefault("sounds", []):
            self.sounds.append(Object(self.fname, sound,
                                      default_class="sge.Sound"))

        for music in data.setdefault("music", []):
            self.music.append(Object(self.fname, music,
                                     default_class="sge.Music"))

        for font in data.setdefault("fonts", []):
            self.fonts.append(Object(self.fname, font,
                                     default_class="sge.Font"))

        for obj in data.setdefault("objects", []):
            self.objects.append(Object(self.fname, obj))

        for room in data.setdefault("rooms", []):
            self.rooms.append(Room(self.fname, room))

    def save(self):
        """Save this object to its corresponding JSON file."""
        data = {"copyright_notice": self.copyright_notice,
                "game_class": self.game_class, "game_kwargs": [],
                "modules": [], "constants": [], "global_variables": [],
                "classes": [], "functions": [], "sprites": [],
                "background_layers": [], "backgrounds": [], "sounds": [],
                "music": [], "fonts": [], "objects": [], "rooms": []}

        for kwarg in self.game_kwargs:
            data["game_kwargs"].append(kwarg.get_data())

        for module in self.modules:
            data["modules"].append(module.get_data())

        for constant in self.constants:
            data["constants"].append(constant.get_data())

        for global_variable in self.global_variables:
            data["global_variables"].append(global_variable.get_data())

        for cls in self.classes:
            data["classes"].append(cls.get_data())

        for function in self.functions:
            data["functions"].append(function.get_data())

        for sprite in self.sprites:
            data["sprites"].append(sprite.get_data())

        for background_layer in self.background_layers:
            data["background_layers"].append(background_layer.get_data())

        for background in self.backgrounds:
            data["backgrounds"].append(background.get_data())

        for sound in self.sounds:
            data["sounds"].append(sound.get_data())

        for music in self.music:
            data["music"].append(music.get_data())

        for font in self.fonts:
            data["fonts"].append(font.get_data())

        for obj in self.objects:
            data["objects"].append(obj.get_data())

        for room in self.rooms:
            data["rooms"].append(room.get_data())

        with open(self.fname, 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)


class DataElement(object):

    """Object representing a data element.

    This is a superclass of several others representing complex data in
    a JSON file.

    .. attribute:: fname

       The name of the JSON file this object is associated with.  Note
       that this is the JSON file that the data form of this object is
       actually stored in, which may be different from the top-level
       JSON file associated with a :class:`StellarJSON` object.

    """

    def __init__(self, fname, data):

        """Return a data element object.

        Arguments:

        - ``parent`` -- The :class:`StellarJSON` object this object is a
          part of.
        - ``data`` -- The data form of the object.  What type of data
          this should be depends on the class; see the documentation for
          the respective class for more information.

        """
        self.fname = fname
        self.data = data

    def get_data(self):
        """Return the data form of this object.

        What type of data this will be depends on the class; see the
        documentation for the respective class for more information.

        """
        return self.data

    def get_code(self):
        """Return the Python code of this object.

        This Python code is the code that would be placed within a
        game's Python code file, minus any indentation needed.
        Depending on the object, it might be one line or multiple lines.

        """
        return "pass"


class Module(DataElement):

    """Object representing a module import.

    An object of this class represents the importation of a module.  Its
    data form is a dictionary with the following keys:

    - ``"module"`` -- The value of :attr:`module`.
    - ``"source"`` -- The value of :attr:`source`.
    - ``"name"`` -- The value of :attr:`name`.

    .. attribute:: fname

       See the documentation for :attr:`DataElement.fname`.

    .. attribute:: module

       The name of the module to import (i.e. the name to put after the
       ``import`` keyword).

    .. attribute:: source

       The name of the module to import :attr:`module` from (i.e. the
       name to put after the ``from`` keyword).  Set to :const:`None` to
       not import from another module.

    .. attribute:: name

       The name to assign :attr:`module` to (i.e. the name to put after
       the ``as`` keyword).  Set to :const:`None` to keep the name as it
       is.

    """

    def __init__(self, fname, data):
        self.fname = fname
        self.source = data.setdefault("source")
        self.name = data.setdefault("name")
        self.module = data.setdefault("module", self.name)

    def get_data(self):
        return {"module": self.module, "source": self.source,
                "name": self.name}

    def get_code(self):
        base_form = "import {0}"

        if self.source:
            base_form = ' '.join(("from {1}", base_form))

        if self.name:
            base_form = ' '.join((base_form, "as {2}"))

        return base_form.format(self.module, self.source, self.name)


class Variable(DataElement):

    """Object representing a variable assignment.

    An object of this class represents the assignment of a value to a
    variable.  Its data form is a dictionary with the following keys:

    - ``"name"`` -- The value of :attr:`name`.
    - ``"value"`` -- The value of :attr:`value`.

    .. attribute:: fname

       See the documentation for :attr:`DataElement.fname`.

    .. attribute:: name

       The name of the variable as a string.  May be preceded with the
       ``global`` keyword in the usual way, e.g. ``"global spam"``
       instead of just ``"spam"``, to force the variable to be global.

    .. attribute:: value

       The value of the variable as a Python-interpretable string, valid
       within the context of generated Python code.

    """

    def __init__(self, fname, data):
        self.fname = fname
        self.name = data.setdefault("name", "bacon")
        self.value = data.setdefault("value", "None")

    def get_data(self):
        return {"name": self.name, "value": self.value}

    def get_code(self):
        name_parts = self.name.split(maxsplit=1)

        if len(name_parts) >= 2 and name_parts[0] == "global":
            return "global {0}\n{0} = {1}".format(name_parts[1], self.value)
        else:
            return "{0} = {1}".format(self.name, self.value)


class Class(DataElement):

    """Object representing a class definition.

    An object of this class represents the definition of a class.  Its
    data form is a dictionary with the following keys:

    - ``"name"`` -- The value of :attr:`name`.
    - ``"parents"`` -- The value of :attr:`parents`.
    - ``"docstring"`` -- The value of :attr:`docstring`.
    - ``"class_attributes"`` -- A list of the data forms of the
      respective objects in :attr:`class_attributes`.
    - ``"properties"`` -- A list of the data forms of the respective
      objects in :attr:`properties`.
    - ``"methods"`` -- A list of the data forms of the respective
      objects in :attr:`methods`.
    - ``"class_methods"`` -- A list of the data forms of the respective
      objects in :attr:`class_methods`.
    - ``"static_methods"`` -- A list of the data forms of the respective
      objects in :attr:`static_methods`.

    .. attribute:: fname

       See the documentation for :attr:`DataElement.fname`.

    .. attribute:: name

       The name of the class.

    .. attribute:: parents

       A list of parent classes of the class.

    .. attribute:: docstring

       The text which describes and documents the class.  Newlines and
       indentation for the sake of good appearance within the code file
       may be omitted; these features will be added automatically during
       code generation.

    .. attribute:: class_attributes

       A list of :class:`Variable` objects indicating the class
       attributes of the class.

    .. attribute:: properties

       A list of :class:`Property` objects indicating the properties of
       the class.

    .. attribute:: methods

       A list of :class:`Function` objects indicating the methods of the
       class.

    .. attribute:: class_methods

       A list of :class:`Function` objects indicating the class methods
       of the class.

    .. attribute:: static_methods

       A list of :class:`Function` objects indicating the static methods
       of the class.

    .. attribute:: external

       The name of a separate file to store the class in.  Set to
       :const:`False` to store the class in the same file, or
       :const:`True` to choose a name automatically.

    """

    @property
    def external(self):
        return self._external

    @external.setter
    def external(self, value):
        if value:
            if isinstance(value, basestring):
                self._external = value
            else:
                self._external = "{0}.json".format(self.name)
        else:
            self._external = False

    def __init__(self, fname, data):
        if isinstance(data, basestring):
            self._external = data
            path = get_path(data, os.path.dirname(fname))
            with open(path, 'r') as f:
                data = json.load(f)
        else:
            self._external = False

        self.fname = fname
        self.name = data.setdefault("name", "Spam")
        self.parents = data.setdefault("parents", ["object"])
        self.docstring = data.setdefault("docstring", "")
        self.class_attributes = []
        self.properties = []
        self.methods = []
        self.class_methods = []
        self.static_methods = []

        fname = self.external if self.external else self.fname

        for attr in data.setdefault("class_attributes", []):
            self.class_attributes.append(Variable(fname, attr))

        for prop in data.setdefault("properties", []):
            self.properties.append(Property(fname, prop))

        for meth in data.setdefault("methods", []):
            self.methods.append(Function(fname, meth))

        for meth in data.setdefault("class_methods", []):
            self.class_methods.append(Function(fname, meth))

        for meth in data.setdefault("static_methods", []):
            self.static_methods.append(Function(fname, meth))

    def get_data(self):
        data = {"name": self.name, "parents": self.parents,
                "docstring": self.docstring, "class_attributes": [],
                "properties": [], "methods": [], "class_methods": [],
                "static_methods": []}

        for attr in self.class_attributes:
            data["class_attributes"].append(attr.get_data())

        for prop in self.properties:
            data["properties"].append(prop.get_data())

        for meth in self.methods:
            data["methods"].append(meth.get_data())

        for meth in self.class_methods:
            data["class_methods"].append(meth.get_data())

        for meth in self.static_methods:
            data["static_methods"].append(meth.get_data())

        if self.external:
            path = get_path(self.external, os.path.dirname(self.fname))
            with open(path, 'w') as f:
                json.dump(data, f, indent=4, sort_keys=True)

            data = self.external

        return data

    def get_code(self):
        # Header
        parents = ', '.join(self.parents)
        header = "class {0}({1}):".format(self.name, parents)

        # Body
        lines = [header, ""]

        docstring_lines = []
        for line in self.docstring.splitlines():
            line = line.rstrip()
            if line:
                line = ''.join((" " * CODE_TAB_WIDTH, line))

                indent_level = CODE_TAB_WIDTH
                while line[indent_level] == " ":
                    indent_level += 1

                while len(line) > DOCSTRING_LINE_SIZE:
                    i = DOCSTRING_LINE_SIZE
                    while line[i] != " " and i > indent_level:
                        i -= 1

                    if i <= indent_level:
                        # This means that there were no spaces at all in
                        # the line (other than indentation).
                        docstring_lines.append(line[:DOCSTRING_LINE_SIZE])
                        line = line[DOCSTRING_LINE_SIZE + 1:]
                    else:
                        docstring_lines.append(line[:i])
                        line = line[i + 1:]

                    line = ''.join((" " * indent_level, line))

                if line.rstrip():
                    docstring_lines.append(line)
            else:
                # This is a blank line, but we still want to include
                # blank lines.
                docstring_lines.append("")

        if len(docstring_lines) == 1:
            lines.append('"""{0}"""'.format(docstring_lines[0]))
        elif docstring_lines:
            firstline = docstring_lines.pop(0).strip()
            lines.append('"""{0}'.format(firstline))
            lines.extend(docstring_lines)
            lines.append('\n"""')
        else:
            lines.append('""""""')

        if self.class_attributes:
            lines.append("")
            for attr in self.class_attributes:
                attribute_lines = attr.get_code().splitlines()
                for line in attribute_lines:
                    line = ''.join((" " * CODE_TAB_WIDTH, line)).rstrip()
                    lines.append(line)

        if self.properties:
            for prop in self.properties:
                lines.append("")
                property_lines = prop.get_code().splitlines()
                for line in property_lines:
                    line = ''.join((" " * CODE_TAB_WIDTH, line)).rstrip()
                    lines.append(line)

        if self.methods:
            for meth in self.methods:
                lines.append("")
                method_lines = meth.get_code().splitlines()
                for line in method_lines:
                    line = ''.join((" " * CODE_TAB_WIDTH, line)).rstrip()
                    lines.append(line)

        if self.class_methods:
            for meth in self.class_methods:
                lines.append("")
                dec = ''.join((" " * CODE_TAB_WIDTH, "@classmethod"))
                lines.append(dec)
                method_lines = meth.get_code().splitlines()
                for line in method_lines:
                    line = ''.join((" " * CODE_TAB_WIDTH, line)).rstrip()
                    lines.append(line)

        if self.static_methods:
            for meth in self.static_methods:
                lines.append("")
                dec = ''.join((" " * CODE_TAB_WIDTH, "@staticmethod"))
                lines.append(dec)
                method_lines = meth.get_code().splitlines()
                for line in method_lines:
                    line = ''.join((" " * CODE_TAB_WIDTH, line)).rstrip()
                    lines.append(line)

        return '\n'.join(lines)


class Function(DataElement):

    """Object representing a function definition.

    An object of this class represents the definition of a function.
    Its data form is a dictionary with the following keys:

    - ``"name"`` -- The value of :attr:`name`.
    - ``"arguments"`` -- The value of :attr:`arguments`.
    - ``"code"`` -- The value of :attr:`code` if :attr:`external` is
      :const:`False`; otherwise, the name of the file containing the
      value of :attr:`code` as a POSIX path relative to the location of
      :attr:`fname`.

    .. attribute:: fname

       See the documentation for :attr:`DataElement.fname`.

    .. attribute:: name

       The name of the function.

    .. attribute:: arguments

       A list of :class:`FunctionArgument` objects indicating the
       arguments of the function.

    .. attribute:: code

       The function as a Python-interpretable string, valid within the
       context of generated Python code.

    .. attribute:: external

       The name of a separate file to store the value of :attr:`code`.
       Set to :const:`False` to store the value in the same file, or
       :const:`True` to choose a name automatically.

    """

    @property
    def external(self):
        return self._external

    @external.setter
    def external(self, value):
        if value:
            if isinstance(value, basestring):
                self._external = value
            else:
                self._external = "{0}.spy".format(self.name)
        else:
            self._external = False

    def __init__(self, fname, data):
        self.fname = fname
        self.name = data.setdefault("name", "eggs")
        self.arguments = []

        for arg in data.setdefault("arguments", []):
            self.arguments.append(FunctionArgument(self.fname, arg))

        self.code = data.setdefault("code", "pass")
        self.external = False

        path = get_path(self.code, os.path.dirname(self.fname))
        if os.path.isfile(path):
            self.external = self.code
            with open(path, 'r') as f:
                self.code = f.read()

    def get_data(self):
        data = {"name": self.name, "arguments": [], "code": self.code}

        for arg in self.arguments:
            data["arguments"].append(arg.get_data())

        if self.external:
            data["code"] = self.external
            path = get_path(self.external, os.path.dirname(self.fname))
            with open(path, 'w') as f:
                f.write(self.code)

        return data

    def get_code(self):
        args_list = []
        for arg in self.arguments:
            args_list.append(arg.get_code)

        args = ', '.join(args_list)
        header = "def {0}({1}):".format(self.name, args)

        lines = [header]

        for line in self.code.splitlines():
            line = ''.join((" " * CODE_TAB_WIDTH, line))
            lines.append(line)

        return '\n'.join(lines)


class Property(DataElement):

    """Object representing a class property definition.

    An object of this class represents the definition of a class
    property.  Its data form is a dictionary with the following keys:

    - ``"name"`` -- The value of :attr:`name`.
    - ``"getter"`` -- The value of :attr:`getter` if
      :attr:`getter_external` is :const:`False`; otherwise, the name of
      the file containing the value of :attr:`getter` as a POSIX path
      relative to the location of :attr:`fname`.
    - ``"setter"`` -- The value of :attr:`setter` if
      :attr:`setter_external` is :const:`False`; otherwise, the name of
      the file containing the value of :attr:`setter` as a POSIX path
      relative to the location of :attr:`fname`.

    .. attribute:: fname

       See the documentation for :attr:`DataElement.fname`.

    .. attribute:: name

       The name of the property.

    .. attribute:: getter

       The getter method code as a Python-interpretable string, valid
       within the context of generated Python code.  The method is
       assumed to have its arguments list set to: ``(self)``.

    .. attribute:: getter_external

       The name of a separate file to store the value of :attr:`getter`.
       Set to :const:`False` to store the value in the same file, or
       :const:`True` to choose a name automatically.

    .. attribute:: setter

       The setter method code as a Python-interpretable string, valid
       within the context of generated Python code.  The method is
       assumed to have its arguments list set to: ``(self, value)``.

    .. attribute:: setter_external

       The name of a separate file to store the value of :attr:`setter`.
       Set to :const:`False` to store the value in the same file, or
       :const:`True` to choose a name automatically.

    """

    @property
    def getter_external(self):
        return self._getter_external

    @getter_external.setter
    def getter_external(self, value):
        if value:
            if isinstance(value, basestring):
                self._getter_external = value
            else:
                self._getter_external = "{0}_getter.spy".format(self.name)
        else:
            self._getter_external = False

    @property
    def setter_external(self):
        return self._setter_external

    @setter_external.setter
    def setter_external(self, value):
        if value:
            if isinstance(value, basestring):
                self._setter_external = value
            else:
                self._setter_external = "{0}_setter.spy".format(self.name)
        else:
            self._setter_external = False

    def __init__(self, fname, data):
        self.fname = fname
        self.name = data.setdefault("name", "eggs")
        self.arguments = []

        for arg in data.setdefault("arguments", []):
            self.arguments.append(FunctionArgument(self.fname, arg))

        self.getter = data.setdefault("getter", "pass")
        self.setter = data.setdefault("setter", "pass")
        self.getter_external = False
        self.setter_external = False

        path = get_path(self.getter, os.path.dirname(self.fname))
        if os.path.isfile(path):
            self.getter_external = self.getter
            with open(path, 'r') as f:
                self.getter = f.read()

        path = get_path(self.setter, os.path.dirname(self.fname))
        if os.path.isfile(path):
            self.setter_external = self.setter
            with open(path, 'r') as f:
                self.setter = f.read()

    def get_data(self):
        data = {"name": self.name, "getter": self.getter,
                "setter": self.setter}

        if self.getter_external:
            data["getter"] = self.getter_external
            path = get_path(self.getter_external, os.path.dirname(self.fname))
            with open(path, 'w') as f:
                f.write(self.getter)

        if self.setter_external:
            data["setter"] = self.setter_external
            path = get_path(self.setter_external, os.path.dirname(self.fname))
            with open(path, 'w') as f:
                f.write(self.setter)

        return data


class FunctionArgument(Variable):

    """Object representing an argument in a function definition.

    An object of this class represents an argument in the definition of
    a function.  Its data form is a dictionary with the following keys:

    - ``"name"`` -- The value of :attr:`name`.
    - ``"default"`` -- The value of :attr:`default`.

    .. attribute:: fname

       See the documentation for :attr:`DataElement.fname`.

    .. attribute:: name

       The name of the argument.  Values such as ``"*args"`` and
       ``"**kwargs"`` are acceptable.

    .. attribute:: default

       The default value of the argument as a Python-interpretable
       string, valid within the context of generated Python code.  Set
       to :const:`None` for no default.

    """

    @property
    def default(self):
        return self.value

    @default.setter
    def default(self, value):
        self.value = value

    def get_data(self):
        return {"name": self.name, "default": self.default}

    def get_code(self):
        if self.default is None:
            return self.name
        else:
            return "{0}={1}".format(self.name, self.default)


class Object(DataElement):

    """Object representing the creation of an object.

    An object of this class represents the creation of an object.  Its
    data form is a dictionary with the following keys:

    - ``"name"`` -- The value of :attr:`name`.
    - ``"class"`` -- The value of :attr:`cls`.
    - ``"arguments"`` -- The value of :attr:`arguments`.
    - ``"keyword_arguments"`` -- A list of the data forms of the
      respective objects in :attr:`keyword_arguments`.

    .. attrubute:: fname

       See the documentation for :attr:`DataElement.fname`.

    .. attribute:: name

       The name of the variable to assign the object to.  Set to
       :const:`None` for no assignment.  May be preceded with the
       ``global`` keyword in the usual way, e.g. ``"global spam"``
       instead of ``"spam"``, to force the variable to be global.

    .. attribute:: cls

       The name of the class to create an object of.

    .. attribute:: arguments

       A list of values to pass as arguments to the object's constructor
       method as Python-interpretable strings, valid within the context
       of generated Python code.

    .. attribute:: keyword_arguments

       A list of :class:`Variable` objects indicating the keyword
       arguments to pass on to the object's constructor method.

    """

    def __init__(self, fname, data, default_class="sge.StellarClass"):
        self.fname = fname
        self.name = data.setdefault("name")
        self.cls = data.setdefault("class", default_class)
        self.arguments = data.setdefault("arguments", [])
        self.keyword_arguments = []

        for kwarg in data.setdefault("keyword_arguments", []):
            self.keyword_arguments.append(Variable(self.fname, kwarg))

    def get_data(self):
        data = {"name": self.name, "class": self.cls,
                "arguments": self.arguments, "keyword_arguments": []}

        for kwarg in self.keyword_arguments:
            data["keyword_arguments"].append(kwarg.get_data())

        return data


class Room(DataElement):

    """Object representing a room.

    An object of this class represents the creation of a room.  Its data
    form is a dictionary with the following keys:

    - ``"name"`` -- The value of :attr:`name`.
    - ``"class"`` -- The value of :attr:`cls`.
    - ``"arguments"`` -- The value of :attr:`arguments`.
    - ``"keyword_arguments"`` -- A list of the data forms of the
      respective objects in :attr:`keyword_arguments`.
    - ``"objects"`` -- A list of data forms of the respective objects in
      :attr:`objects`.

    .. attrubute:: fname

       See the documentation for :attr:`DataElement.fname`.

    .. attribute:: name

       The name of the variable to assign the object to.  Set to
       :const:`None` for no assignment.  The variable name may be
       preceded with the ``global`` keyword in the usual way, e.g.
       ``"global spam"``, to force the variable assigned to to be
       global.

    .. attribute:: cls

       The name of the class to create an object of.

       .. note::

          The constructor method for the class MUST support a keyword
          argument called ``objects``.  This is expected to be passed on
          to the constructor method of ``sge.Room`` and is how the
          objects in :attr:`objects` are added to the room in the built
          game.

    .. attribute:: arguments

       A list of values to pass as arguments to the room's constructor
       method as Python-interpretable strings, valid within the context
       of generated Python code.

       .. note::

          The first argument of the constructor method of ``sge.Room``,
          ``objects``, is passed as a keyword argument, so this
          attribute should be kept as ``[]`` unless your room class's
          constructor method has extra arguments in front of
          ``objects``.  Otherwise, use :attr:`keyword_arguments`.

    .. attribute:: keyword_arguments

       A list of :class:`Variable` objects indicating the keyword
       arguments to pass on to the room's constructor method.

    .. attribute:: objects

       A list of :class:`Object` objects indicating the objects to start
       the room with.

    .. attribute:: external

       The name of a separate file to store the room in.  Set to
       :const:`False` to store the room in the same file, or
       :const:`True` to choose a name automatically.

    """

    @property
    def external(self):
        return self._external

    @external.setter
    def external(self, value):
        if value:
            if isinstance(value, basestring):
                self._external = value
            else:
                self._external = "{0}.json".format(self.name)
        else:
            self._external = False

    def __init__(self, fname, data):
        if isinstance(data, basestring):
            self._external = data
            path = get_path(data, os.path.dirname(fname))
            with open(path, 'r') as f:
                data = json.load(f)
        else:
            self._external = False

        self.fname = fname
        self.name = data.setdefault("name")
        self.cls = data.setdefault("class", "sge.Room")
        self.arguments = data.setdefault("arguments", [])
        self.keyword_arguments = []
        self.objects = []

        fname = self.external if self.external else self.fname

        for kwarg in data.setdefault("keyword_arguments", []):
            self.keyword_arguments.append(Variable(fname, kwarg))

        for obj in data.setdefault("objects", []):
            self.objects.append(Object(fname, obj))

    def get_data(self):
        data = {"name": self.name, "class": self.cls,
                "arguments": self.arguments, "keyword_arguments": [],
                "objects": []}

        for kwarg in self.keyword_arguments:
            data["keyword_arguments"].append(kwarg.get_data())

        for obj in self.objects:
            data["objects"].append(obj.get_data())

        if self.external:
            path = get_path(self.external, os.path.dirname(self.fname))
            with open(path, 'w') as f:
                json.dump(data, f, indent=4, sort_keys=True)

            data = self.external

        return data


def get_path(s, wd=os.getcwd()):
    """Return a valid path for this system based on a POSIX path.

    Arguments:

    - ``s`` -- The string to change into a valid path for this system.
    - ``wd`` -- The directory to search from.

    This function does not allow absolute paths.

    """
    parts = s.split("/")

    # Make sure paths are relative to the right place.
    if parts[0] == ".":
        parts[0] = wd
    else:
        parts.insert(0, wd)

    for i in xrange(len(parts)):
        if parts[i] == ".":
            parts[i] = os.curdir
        elif parts[i] == "..":
            parts[i] = os.pardir

    return os.path.join(*parts)


if __name__ == '__main__':
    # Test case
    stj = StellarJSON("test.json")
    stj.copyright_notice = "Permission to do whatever you want, no restrictions."
    stj.constants.append(Variable(stj.fname, {"name": "FOO", "value": "42"}))
    stj.classes.append(Class(stj.fname, {"name": "Bar"}))
    stj.classes[0].methods.append(Function(stj.fname, {"name": "baz", "code": "pass"}))
    stj.rooms.append(Room(stj.fname, {}))
    stj.rooms[0].objects.append(Object(stj.fname, {}))
    stj.save()
