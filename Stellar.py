import os, sys, json
import sip
sip.setapi('QVariant', 2)
from PyQt4 import QtCore, QtGui

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.header().setResizeMode(QtGui.QHeaderView.Stretch)
        self.treeWidget.setHeaderLabel("Project")
        self.setCentralWidget(self.treeWidget)

        self.createActions()
        self.createMenus()

        self.item = None

        style = self.treeWidget.style()

        self.folderIcon = QtGui.QIcon()
        self.bookmarkIcon = QtGui.QIcon()
        self.folderIcon.addPixmap(style.standardPixmap(QtGui.QStyle.SP_DirClosedIcon),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.folderIcon.addPixmap(style.standardPixmap(QtGui.QStyle.SP_DirOpenIcon),
                QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.bookmarkIcon.addPixmap(style.standardPixmap(QtGui.QStyle.SP_FileIcon))

        self.statusBar().showMessage("Ready")

        self.setWindowTitle("Stellar")
        self.resize(300, 320)

    def open(self):
        self.statusBar().showMessage("Opening project...")
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                "Open Project File", QtCore.QDir.currentPath(),
                "Project Files (*.JSON)")
        #fileName=os.path.join("example","example.JSON")

        if not fileName:
            return
        self.treeWidget.clear()
        
        decoded_data=json.loads(open(fileName,'r').read())
        self.format_main_response(decoded_data)

    def format_main_response(self, json_string):
        for key, value in json_string.iteritems():
            #print key
            if key=='classes':
                self.item = self.createChildItem(key)
                self.item.setFlags(self.item.flags() | QtCore.Qt.ItemIsEditable)
                self.item.setIcon(0, self.folderIcon)
                self.item.setText(0, key)
                self.treeWidget.setItemExpanded(self.item, False)
                
                for val in value:
                    self.item = self.createChildItem(value)
                    self.item.setFlags(self.item.flags() | QtCore.Qt.ItemIsEditable)
                    self.item.setIcon(0, self.bookmarkIcon)
                    self.item.setText(0, val)
                    self.item = self.item.parent()

                self.item = self.item.parent()

        self.statusBar().showMessage("File loaded", 2000)

    def createChildItem(self, Name):
        if self.item:
            childItem = QtGui.QTreeWidgetItem(self.item)
        else:
            childItem = QtGui.QTreeWidgetItem(self.treeWidget)

        childItem.setData(0, QtCore.Qt.UserRole, Name)
        return childItem


    def saveAs(self):
        pass

    def createActions(self):
        self.openAct = QtGui.QAction("&Open...", self, shortcut="Ctrl+O",
                triggered=self.open)

        self.saveAsAct = QtGui.QAction("&Save As...", self, shortcut="Ctrl+S",
                triggered=self.saveAs)

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+X",
                triggered=self.close)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addAction(self.exitAct)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    mainWin.open()
    mainWin.raise_()
    sys.exit(app.exec_())