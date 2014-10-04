import sys
import os
from PyQt4 import QtCore, QtGui, QtWebKit
from PyQt4.QtWebKit import QWebSettings

class CodeEditor(QtGui.QDialog):
    def __init__(self, main, current_file):
        super(CodeEditor, self).__init__(main)
        self.main = main
        self.webkit = QtWebKit.QWebView()
        self.realpath = os.path.dirname(os.path.realpath(__file__))

        self.current_file = current_file
        if ".md" in self.current_file:
            self.syntax_mode = "markdown"
        elif ".py" in self.current_file:
            self.syntax_mode = "python"
        else:
            self.syntax_mode = "markdown"

        #Reading the template
        with open(os.path.join(self.realpath,'html','template.html')) as f:
            template = f.read()
            template = template.replace("MODE", self.syntax_mode)

        #Reading the target file
        if self.current_file!="":
            with open(self.current_file) as f:
                target = f.read()
        else:
            target = self.current_file
        
        new_file = template.replace("TEXTPLACEHOLDER", target)

        with open(os.path.join(self.realpath,'currentfile.html'),'w') as f:
            f.write(new_file)

        url = "file:///" + os.path.join(self.realpath,'currentfile.html')
        url = url.replace("\\", "/")
        self.webkit.load(QtCore.QUrl(url))

        self.ContainerGrid = QtGui.QGridLayout(self)
        self.ContainerGrid.setMargin (0)
        self.ContainerGrid.setSpacing(0)
        self.ContainerGrid.addWidget(self.webkit)
        self.setLayout(self.ContainerGrid)

        #saveAction = QtGui.QAction(QtGui.QIcon(), '&Save', self)        
        #saveAction.setShortcut('Ctrl+S')
        #saveAction.triggered.connect(self.save)
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+S"), self, self.save)

    def save(self):
        jscript = "editor.getValue();"     
        current_text = self.webkit.page().mainFrame().evaluateJavaScript(jscript)  
        current_text = current_text.toPyObject()

        self.main.statusBar().showMessage(self.current_file + ' Saved', 2000)
        with open(self.current_file,'w') as f:
            try:
                f.write(current_text)
            except Exception, e:
                print e

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainWin = CodeEditor("C:\\Users\\Loremi\\Documents\\GitHub\\Stellar\\Stellar.py")
    mainWin.show()
    mainWin.raise_() #Making the window get focused on OSX
    sys.exit(app.exec_())