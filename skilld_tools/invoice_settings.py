import os
import sys
from collections import OrderedDict
from PyQt4 import QtCore, QtGui, uic
from skilld_tools import __skilld_tools_vars__
from .__skilld import __common as skilldToolsCommon

form_class = uic.loadUiType(__skilld_tools_vars__['INSTALL_DIR'] + "/ui/settings-invoice.ui")[0]
class invoice_settings(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        # Custom variables.
        self.__sdTools = skilldToolsCommon()
        self.conf_directory = os.environ['HOME'] + '/.skilld-tools/settings'
        self.conf_filename = 'invoice.json'
        # Actions.
        self.btnAddBankItem.clicked.connect(self.addBankItem)
        self.btnSaveInvoiceSettings.clicked.connect(self.saveInvoiceSettings)
        # Helper methods.
        self.initInvoiceConf()


    def addBankItem(self, row_data = {}):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        if bool(row_data) and 'label' in row_data and 'value' in row_data:
          self.tableWidget.setItem(rowPosition, 0, QtGui.QTableWidgetItem(row_data['label']))
          self.tableWidget.setItem(rowPosition, 1, QtGui.QTableWidgetItem(row_data['value']))
        self.setRowOpts(self.tableWidget, rowPosition, 2)


    def removeBankItem(self, index):
        if index.isValid():
          self.tableWidget.removeRow(index.row())


    def saveInvoiceSettings(self):
        __str_billing_name = self.txtBillingName.text()
        data = {'billing_items': {'username': __str_billing_name}, 'banking_items': { 'elements': {}, 'amount': 0}}

        filepath = self.conf_directory + '/' + self.conf_filename
        self.__sdTools.init_dir(self.conf_directory)

        allRows = self.tableWidget.rowCount()
        for row in range(0, allRows):
          element = {}
          label = self.tableWidget.item(row, 0)
          if label:
            element['banking_label'] = label.text()
          value = self.tableWidget.item(row, 1)
          if value:
            element['banking_value'] = value.text()

          data['banking_items']['elements'][row] = element
          data['banking_items']['amount'] += 1

        self.__sdTools.saveConf(filepath, data)


    def setRowOpts(self, tableWidget, row, col):
        btn = QtGui.QPushButton(tableWidget)
        btn.setText('Remove')
        index = QtCore.QPersistentModelIndex(tableWidget.model().index(row, col))
        btn.clicked.connect(lambda: self.removeBankItem(index))
        tableWidget.setCellWidget(row, col, btn)


    def initInvoiceConf(self):
        filepath = self.conf_directory + '/' + self.conf_filename
        if os.path.isfile(filepath):
          conf = self.__sdTools.getConf(filepath)
          billing_name = conf['billing_items']['username']
          self.txtBillingName.setText(billing_name)
          banking_items = OrderedDict(sorted(conf['banking_items']['elements'].items()))
          for key in banking_items:
            row_values = {
              'label': banking_items[key]['banking_label'],
              'value': banking_items[key]['banking_value']
            }
            self.addBankItem(row_values)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = invoice_settings(None)
    window.show()
    app.exec_()
