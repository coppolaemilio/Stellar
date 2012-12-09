#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 Emilio Coppola
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

import os
import ConfigParser

config = ConfigParser.RawConfigParser()
<<<<<<< HEAD
config.read(os.getcwd() + '/config.ini')
    
=======
config.read('config.ini')

>>>>>>> 59c92839dd2a70c13224e7145ae38ffdc211926e
recentproject = config.get('stellar', 'recentproject')
__version__ = config.get('stellar', 'version')

    
