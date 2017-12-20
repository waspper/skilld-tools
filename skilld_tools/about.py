from PyQt4 import uic, QtGui, QtCore
from skilld_tools import __skilld_tools_vars__


dialog_class = uic.loadUiType(__skilld_tools_vars__['INSTALL_DIR'] + "/ui/about.ui")[0]
class AboutDialog(QtGui.QDialog, dialog_class):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        # Workaround to set right image.
        self.lblLogo.setPixmap(QtGui.QPixmap(__skilld_tools_vars__['INSTALL_DIR'] + '/resources/logo__1.png'))
        self.btnCloseDialog.clicked.connect(self.closeDialog)


    def closeDialog(self):
        self.close()


if __name__ == "__main__":
    app = QtGui.QApplication([])
    dialog = AboutDialog()
    dialog.show()
    dialog.raise_()
    app.exec_()