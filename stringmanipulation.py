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

from PyQt4 import QtGui

def StatementFound(Text):
    String = str(Text)
    bln = False
    for lastchar in String:
        if lastchar !=" ":
            if lastchar == ":":
                bln = True
            else:
                bln = False
    if bln == True:
        return(4*" ")
    else:
        return("")

def TabifyRegion(Text):
    String = str(Text)
    Count = 0
    try:
        while String[0] == " ":
            String = String[1:]
            Count += 1
    except IndexError:
        return (Count*" ")
    return (Count*" ")

def UnTabifyRegion(self,Text):
    String = str(Text)
    cur = self
    Count = 0
    chars = 0
    for x in Text:
        if x == " ":
            Count += 1
        else:
            Count = 0
    if Count%4 == 0:
        if Count == 0:
            chars = 1
        else:
            chars = 4
    else:
        chars = 1
    for i in range(chars):
        cur.deletePreviousChar()
