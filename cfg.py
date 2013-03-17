#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012, 2013 Emilio Coppola
#
# This file is part of Stellar.
#
# Stellar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Stellar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Stellar.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

VERSION = '0.0.3'

import sys
if sys.version_info.major > 2:
    import configparser
    def get(section, option, default_value = None):
        try:
            return config.get(section, option)
        except configparser.NoOptionError:
            return default_value
        except configparser.NoSectionError:
            return default_value
    def set(section, option, value):
        return config.set(section, option, value)
else:
    import ConfigParser as configparser
    def get(section, option, default_value = None):
        try:
            return config.get(section, option).decode('utf-8')
        except configparser.NoOptionError:
            return default_value
        except configparser.NoSectionError:
            return default_value
    def set(section, option, value):
        return config.get(section, option, value.encode('utf-8'))

config = configparser.RawConfigParser()
config.read('config.ini')

def save():
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

__version__ = get('stellar', 'version', VERSION)
recentproject = get('stellar', 'recentproject', '')
codeeditor = get('stellar', 'codeeditor', '')
soundeditor = get('stellar', 'soundeditor', '')
imageeditor = get('stellar', 'imageeditor', '')
terminalcom = get('stellar', 'terminal', 'xterm')
