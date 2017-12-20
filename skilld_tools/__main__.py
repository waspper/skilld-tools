import sys
from PyQt4 import QtCore, QtGui, uic
from skilld_tools import __skilld_tools_vars__
from .invoice import invoiceUI
from .invoice_settings import invoice_settings
from .about import AboutDialog


form_class = uic.loadUiType(__skilld_tools_vars__['INSTALL_DIR'] + '/ui/main.ui')[0]
class main(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Workaround to set the right path to a picture.
        self.logo.setPixmap(QtGui.QPixmap(__skilld_tools_vars__['INSTALL_DIR'] + '/resources/logo__2.png'))
        self.btnInvoice.clicked.connect(self.setupInvoiceGUI)
        # Menu items.
        self.actionInvoiceSettings.triggered.connect(self.setupInvoiceSettingsGUI)
        self.actionExit.triggered.connect(self.exitApp)
        self.actionAbout.triggered.connect(self.about)


    def setupInvoiceGUI(self):
        invoice_ui = invoiceUI(self)
        invoice_ui.show()


    def setupInvoiceSettingsGUI(self):
        invoiceSettings = invoice_settings(self)
        invoiceSettings.show()


    def about(self):
        about = AboutDialog(self)
        about.show()


    def exitApp(self):
        self.close()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = main(None)
    window.show()
    app.exec_()
