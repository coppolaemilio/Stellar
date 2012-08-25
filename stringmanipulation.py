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
