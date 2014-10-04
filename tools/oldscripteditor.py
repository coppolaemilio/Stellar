#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2012, 2014 Emilio Coppola
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

from PyQt4 import QtCore, QtGui
import os, sys
from PyQt4.QtGui import QFont
import json


if sys.version_info.major == 2:
    str = unicode   

class PythonHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)
        self.color_0 = QtGui.QColor(249, 38,  144)
        self.color_1 = QtGui.QColor(102, 217, 239)
        self.color_2 = QtGui.QColor(117, 113, 94 )#comments
        self.color_3 = QtGui.QColor(230, 219, 102)
        self.color_4 = QtGui.QColor(166,226,46)
        self.color_5 = QtGui.QColor(174,129,255)
        self.color_6 = QtGui.QColor(253,151,32)

        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(self.color_0)
        keywordPatterns = keywords = [
            "\\band\\b",       "\\bdel\\b",       "\\bfor\\b",       "\\bis\\b",        "\\braise\\b",
            "\\bassert\\b",    "\\belif\\b",      "\\bfrom\\b",      "\\blambda\\b",    "\\breturn\\b",
            "\\bbreak\\b",     "\\belse\\b",      "\\bglobal\\b",    "\\bnot\\b",       "\\btry\\b",
            "\\bclass\\b",     "\\bexcept\\b",    "\\bif\\b",        "\\bor\\b",        "\\bwhile\\b",
            "\\bcontinue\\b",  "\\bexec\\b",      "\\bimport\\b",    "\\bpass\\b",      "\\byield\\b",
            "\\bdef\\b",       "\\bfinally\\b",   "\\bin\\b",        "\\bprint",        '='
        ]

        self.highlightingRules = [(QtCore.QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]

        classFormat = QtGui.QTextCharFormat()
        classFormat.setForeground(self.color_4)
        self.highlightingRules.append((QtCore.QRegExp("\\bQ[A-Za-z]+\\b"),
                classFormat))

        numberFormat = QtGui.QTextCharFormat()
        numberFormat.setForeground(self.color_5)
        numberPatterns = ['\\b[+-]?[0-9]+[lL]?\\b', '\\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\\b',
        '\\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\\b', '\\btrue\\b', '\\bfalse\\b']
        self.highlightingRules += [(QtCore.QRegExp(pattern), numberFormat)
                for pattern in numberPatterns]

        singleLineCommentFormat = QtGui.QTextCharFormat()
        singleLineCommentFormat.setForeground(self.color_2)
        self.highlightingRules.append((QtCore.QRegExp("#[^\n]*"),
                singleLineCommentFormat))

        quotationFormat = QtGui.QTextCharFormat()
        quotationFormat.setForeground(self.color_3)
        self.highlightingRules.append((QtCore.QRegExp("\".*\""),
                quotationFormat))

        self.highlightingRules.append((QtCore.QRegExp("\'.*\'"),
                quotationFormat))

        functionFormat = QtGui.QTextCharFormat()
        functionFormat.setForeground(self.color_1)
        self.highlightingRules.append((QtCore.QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
                functionFormat))

        self.commentStartExpression = QtCore.QRegExp('/\\*')
        self.commentEndExpression = QtCore.QRegExp("\\*/")

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength,
                    self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text,
                    startIndex + commentLength);



class EELHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(EELHighlighter, self).__init__(parent)
        self.color_0 = QtGui.QColor(249, 38,  144)
        self.color_1 = QtGui.QColor(102, 217, 239)
        self.color_2 = QtGui.QColor(117, 113, 94 )#comments
        self.color_3 = QtGui.QColor(230, 219, 102)
        self.color_4 = QtGui.QColor(166,226,46)
        self.color_5 = QtGui.QColor(174,129,255)
        self.color_6 = QtGui.QColor(253,151,32)

        group1Format = QtGui.QTextCharFormat()
        group1Format.setForeground(self.color_0)
        group1Patterns = ["\\bimport\\b", '\\bif\\b', '\\belse\\b',
                          "\\bfor\\b", "\\bswitch\\b" , "\\bcase\\b",
                          "\\bbreak\\b", "\\breturn\\b", "\\bwhile\\b",
                          "\\blocal\\b"]

        self.highlightingRules = [(QtCore.QRegExp(pattern), group1Format)
                for pattern in group1Patterns]


        keywordFormat = QtGui.QTextCharFormat()
        keywordFormat.setForeground(self.color_1)
        words = ["procedure", "table"]
        keywordPatterns = ["\\bchar\\b", "\\bclass\\b", "\\bconst\\b",
                "\\bdouble\\b", "\\benum\\b", "\\bexplicit\\b", "\\bfriend\\b",
                "\\binline\\b", "\\bint\\b", "\\blong\\b", "\\bnamespace\\b",
                "\\boperator\\b", "\\bprivate\\b", "\\bprotected\\b",
                "\\bpublic\\b", "\\bshort\\b", "\\bsignals\\b", "\\bsigned\\b",
                "\\bslots\\b", "\\bstatic\\b", "\\bstruct\\b",
                "\\btemplate\\b", "\\btypedef\\b", "\\btypename\\b",
                "\\bunion\\b", "\\bunsigned\\b", "\\bvirtual\\b", "\\bvoid\\b",
                "\\bvolatile\\b"]
        for word in words:
            keywordPatterns.append("\\b"+word+"\\b")

        

        self.highlightingRules += [(QtCore.QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]

        classFormat = QtGui.QTextCharFormat()
        classFormat.setForeground(self.color_4)
        self.highlightingRules.append((QtCore.QRegExp("\\bQ[A-Za-z]+\\b"),
                classFormat))

        numberFormat = QtGui.QTextCharFormat()
        numberFormat.setForeground(self.color_5)
        numberPatterns = ['\\b[+-]?[0-9]+[lL]?\\b', '\\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\\b',
        '\\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\\b', '\\btrue\\b', '\\bfalse\\b']
        self.highlightingRules += [(QtCore.QRegExp(pattern), numberFormat)
                for pattern in numberPatterns]

        singleLineCommentFormat = QtGui.QTextCharFormat()
        singleLineCommentFormat.setForeground(self.color_2)
        self.highlightingRules.append((QtCore.QRegExp("//[^\n]*"),
                singleLineCommentFormat))

        self.multiLineCommentFormat = QtGui.QTextCharFormat()
        self.multiLineCommentFormat.setForeground(self.color_2)

        quotationFormat = QtGui.QTextCharFormat()
        quotationFormat.setForeground(self.color_3)
        self.highlightingRules.append((QtCore.QRegExp("\".*\""),
                quotationFormat))

        self.highlightingRules.append((QtCore.QRegExp("<.*>"),
                quotationFormat))

        functionFormat = QtGui.QTextCharFormat()
        functionFormat.setForeground(self.color_1)
        self.highlightingRules.append((QtCore.QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
                functionFormat))

        self.commentStartExpression = QtCore.QRegExp("/\\*")
        self.commentEndExpression = QtCore.QRegExp("\\*/")

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength,
                    self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text,
                    startIndex + commentLength);

def parseObject(text):
    string = ""
    for event in text:
        string += "///"+event+" - START\n"
        for line in text[event]:
            string += line
        string += "\n///"+event+" - END\n\n"
    return string

class ScriptEditor(QtGui.QDialog):
    def __init__(self, main, name, file_path):
        super(ScriptEditor, self).__init__(main)
        self.main = main
        self.filename = file_path
        with open(self.filename) as f:
            self.text = f.read()
        #self.text = parseObject(text) 
        self.title = name

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        if os.path.exists(os.path.join('..','images')):
        	img_path=os.path.join('..','images')
        else:
        	img_path=os.path.join('images')

        saveAction = QtGui.QAction(QtGui.QIcon(os.path.join(img_path, 'save.png')), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.save_file)

        importAction = QtGui.QAction(QtGui.QIcon(os.path.join(img_path, 'open.png')), 'Import', self)
        importAction.triggered.connect(self.import_file)

        tabAction = QtGui.QAction(QtGui.QIcon(os.path.join(img_path, 'open.png')), 'Tab', self)
        tabAction.triggered.connect(self.handleTest)

        fontAction = QtGui.QAction(QtGui.QIcon(os.path.join(img_path, 'font.png')), 'Font', self)
        fontAction.triggered.connect(self.fontChange)

        self.toolbar = QtGui.QToolBar('Script Toolbar')
        self.toolbar.setIconSize(QtCore.QSize(16, 16))
        self.toolbar.addAction(saveAction)
        self.toolbar.addAction(importAction)
        self.toolbar.addAction(tabAction)
        self.toolbar.addAction(fontAction)
        
        self.font = QtGui.QFont()
        self.font.setFamily('ClearSans')
        self.font.setStyleHint(QtGui.QFont.Monospace)
        self.font.setFixedPitch(True)
        self.font.setPointSize(int(13))

        self.ContainerGrid = QtGui.QGridLayout(self)
        self.ContainerGrid.setMargin (0)
        self.ContainerGrid.setSpacing(0)

        self.textedit = QtGui.QTextEdit()
        self.textedit.setTabStopWidth(40)
        self.textedit.insertPlainText(self.text)
        self.textedit.moveCursor(QtGui.QTextCursor.Start)
        self.textedit.setLineWrapMode(0)
        self.textedit.setFont(self.font)

        self.linenumbers=QtGui.QTextEdit()
        numbers= 999
        for number in range(numbers):
            self.linenumbers.insertPlainText(str(number+1)+'\n')
        self.linenumbers.setFont(self.font)
        self.linenumbers.verticalScrollBar().setValue( 0) #FIXME
        self.textedit.verticalScrollBar().valueChanged.connect(
            self.linenumbers.verticalScrollBar().setValue)
        self.linenumbers.verticalScrollBar().valueChanged.connect(
            self.textedit.verticalScrollBar().value)
        self.linenumbers.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.linenumbers.setReadOnly (True)
        self.linenumbers.moveCursor(QtGui.QTextCursor.Start)
        self.linenumbers.setStyleSheet("color:rgb(117, 113, 94)")
        self.linenumbers.setTextColor(QtGui.QColor(117, 113, 94 ))

        self.widget = QtGui.QWidget()
        self.layout=QtGui.QHBoxLayout(self.widget)
        self.layout.addWidget(self.linenumbers)
        self.layout.addWidget(self.textedit)
        self.layout.setContentsMargins(0,0,0,0)
        self.linenumbers.setMaximumWidth(38)

        self.ContainerGrid.addWidget(self.toolbar)
        self.ContainerGrid.addWidget(self.widget)

        self.setLayout(self.ContainerGrid)

        self.highlighter = EELHighlighter(self.textedit.document())

    def handleTest(self):
        tab = "\t"
        cursor = self.textedit.textCursor()

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.setPosition(end)
        cursor.movePosition(cursor.EndOfLine)
        end = cursor.position()

        cursor.setPosition(start)
        cursor.movePosition(cursor.StartOfLine)
        start = cursor.position()
        print(cursor.position(), end)

        while cursor.position() < end:
            cursor.movePosition(cursor.StartOfLine)
            cursor.insertText(tab)
            end += tab.count(end)
            cursor.movePosition(cursor.EndOfLine)

    def save_file(self):
        step_event = self.text.split("///step_event - START\n")[1].split("///step_event - END")[0]
        create_event = self.text.split("///create_event - START\n")[1].split("///create_event - END")[0]
        draw_event = self.text.split("///draw_event - START\n")[1].split("///draw_event - END")[0]

        info_create = {"create_event":create_event}
        #info["step_event"] = step_event
        #info["draw_event"] = draw_event

        json_data=open(self.main.projectdir)
        self.data = json.load(json_data)
        self.data["objects"][self.title]["create_event"]=info_create
        #self.data["objects"][self.title]["step_event"]=info["step_event"]
        #self.data["objects"][self.title]["draw_event"]=info["draw_event"]

        with open('dataa.txt', 'w') as outfile:
          json.dump(self.data, outfile)

    def import_file(self):
        target = str(QtGui.QFileDialog.getOpenFileName(self, "Select File"))
        with open(target, 'r') as f:
            self.textedit.setText(f.read())
        self.main.statusBar().showMessage(str(target)+' Imported!', 2000)

    def fontChange(self):
        font, ok = QtGui.QFontDialog.getFont(self.font)
        if ok:
            self.textedit.setFont(font)

    def closeEvent(self, event):
            del self.main.window_index[self.title]

class Editor(QtGui.QMainWindow):
    def __init__(self):
        super(Editor, self).__init__()
        target="none"
        pathtofile="scripteditor.py"

        self.ShowFrame = QtGui.QFrame()
        self.showlayout = QtGui.QGridLayout()
        self.showlayout.setMargin(0)

        self.textedit = ScriptEditor(self, target, pathtofile)

        self.showlayout.addWidget(self.textedit)
        self.ShowFrame.setLayout(self.showlayout)

        self.setCentralWidget(self.ShowFrame)
        self.setWindowTitle("TextEditor - " + self.textedit.title )
        self.resize(640, 480)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    f = open('../themes/default.css')
    style = f.read()
    f.close()
    app.setStyleSheet(style)
    app.setStyle(QtGui.QStyleFactory.create("plastique"))
    mainWin = Editor()
    mainWin.show()
    mainWin.raise_() #Making the window get focused on OSX
    sys.exit(app.exec_())
