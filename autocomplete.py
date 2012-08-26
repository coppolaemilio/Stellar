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

from PyQt4 import QtGui, QtCore
from dictionary import all_words
from stringmanipulation import TabifyRegion, UnTabifyRegion , StatementFound

min_show=2

class DictionaryCompleter(QtGui.QCompleter):
    def __init__(self, parent=None):
        self.words = all_words
        QtGui.QCompleter.__init__(self, self.words, parent)
        
    def append(self,list):
        self.words=self.words+list
        fix=[]
        for word in self.words:
            if not word in fix:
                fix.append(word)
        self.words=fix
            
        QtGui.QCompleter.__init__(self, self.words, parent=None)
        
class CompletionTextEdit(QtGui.QTextEdit):
    def __init__(self):
        super(CompletionTextEdit, self).__init__()
        self.completer = None
        self.moveCursor(QtGui.QTextCursor.End)
        self.dictionary = DictionaryCompleter()
        self.setCompleter(self.dictionary)
        self.center()
        
        
    def Update_dictionary(self,list):
        self.dictionary.append(list)
        self.setCompleter(self.dictionary)
        self.setFocus()
    
    def setCompleter(self, completer):
        #if self.completer:
            #self.disconnect(self.completer, 0, self, 0)
        if not completer:
            return
        
        completer.setWidget(self)
        completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer = completer
        self.connect(self.completer,
            QtCore.SIGNAL("activated(const QString&)"), self.insertCompletion)
    

    def insertCompletion(self, completion):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        tc.removeSelectedText()
        tc.insertText(completion)
        self.setTextCursor(tc)     
        
        self.clearFocus()
        self.setFocus()        
        
    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self);
        QtGui.QTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, event):
        #REPLACING TAB BUTTON
        if event.key() == QtCore.Qt.Key_Tab:
                if self.completer and self.completer.popup().isVisible():
                        event.ignore()
                        return
                else:
                    space = "    "
                    self.insertPlainText(space)
                    return

        if event.key() == QtCore.Qt.Key_Return:
                if self.completer and self.completer.popup().isVisible():
                        event.ignore()
                        return
                else:
                        Tabs = TabifyRegion(self.textCursor().block().text().toAscii())
                        ExtraTab = StatementFound(self.textCursor().block().text().toAscii())
                        space = "\n" + Tabs
                        self.insertPlainText(space + ExtraTab)
                        return

        if event.key() == QtCore.Qt.Key_Backspace:
                UnTabifyRegion(self.textCursor(),self.textCursor().block().text().toAscii())
                if self.completer and self.completer.popup().isVisible(): self.completer.popup().hide()
                return

        if self.completer and self.completer.popup().isVisible():
            if event.key() in (
            QtCore.Qt.Key_Enter,
            QtCore.Qt.Key_Return,
            QtCore.Qt.Key_Escape,
            QtCore.Qt.Key_Tab,
            QtCore.Qt.Key_Backtab):
                event.ignore()
                return

        ## has ctrl-Space been pressed??
        isShortcut = (event.modifiers() == QtCore.Qt.ControlModifier and
                      event.key() == QtCore.Qt.Key_Space)
        if (not self.completer or not isShortcut):
            QtGui.QTextEdit.keyPressEvent(self, event)

        ## ctrl or shift key on it's own??
        ctrlOrShift = event.modifiers() in (QtCore.Qt.ControlModifier ,
                QtCore.Qt.ShiftModifier)
        if ctrlOrShift and event.text().isEmpty():
            # ctrl or shift key on it's own
            return

        eow = QtCore.QString("~!@#$%^&*()+{}|\"<>?/'[]\\-=L") #end of word

        hasModifier = ((event.modifiers() != QtCore.Qt.NoModifier) and
                        not ctrlOrShift)

        completionPrefix = self.textUnderCursor()

        if (not isShortcut and (hasModifier or event.text().isEmpty() or
        completionPrefix.length() < min_show or
        eow.contains(event.text().right(1)))):
            self.completer.popup().hide()
            return

        if (completionPrefix != self.completer.completionPrefix()):
            self.completer.setCompletionPrefix(completionPrefix)
            popup = self.completer.popup()
            popup.setCurrentIndex(
                self.completer.completionModel().index(0,0))

        cr = self.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(0)
            + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr) ## popup it up!

    def ShowMe(self):
        self.show()
        
    def HideMe(self):
        self.hide()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
