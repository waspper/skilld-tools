import os
import sys
from collections import OrderedDict
from PyQt4 import QtCore, QtGui, uic
from skilld_tools import __skilld_tools_vars__
from .__skilld import __common as skilldToolsCommon


form_class = uic.loadUiType(__skilld_tools_vars__['INSTALL_DIR'] + "/ui/invoice.ui")[0]
class invoiceUI(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        #Custom variables.
        self.__sdTools = skilldToolsCommon()
        # Custom actions.
        btn = QtGui.QPushButton(self.tableWidget)
        btn.setText('Remove')
        btn.setDisabled(True)
        self.tableWidget.setCellWidget(0, 5, btn)
        self.btnInvoiceAddItem.clicked.connect(self.addInvoiceItem)
        self.btnInvoiceGenerate.clicked.connect(self.generateInvoice)
        self.tableWidget.itemChanged.connect(lambda item: self.updatedItem(item))


    def updatedItem(self, item):
        row = item.row()
        column = item.column()
        #raw_value = item.text()

        total__calculated = 0
        price__calculated = 0

        units = self.tableWidget.item(row, 2)
        units__num = 0;
        if units:
          units__num = float(units.text())

        price = self.tableWidget.item(row, 3)
        price__num = 0
        if price:
          price__num = float(price.text())

        total = self.tableWidget.item(row, 4)
        total__num = 0
        if total:
          total__num = float(total.text())

        # If "Units" or "Price" is changed:
        if column == 2 or column == 3:
          total__calculated = units__num * price__num
          self.tableWidget.setItem(row, 4, QtGui.QTableWidgetItem(str(total__calculated)))

        # If "Total" is changed:
        if column == 4:
          price__calculated = total__num / units__num
          self.tableWidget.setItem(row, 3, QtGui.QTableWidgetItem(str(price__calculated)))


    def addInvoiceItem(self):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        btn = QtGui.QPushButton(self.tableWidget)
        btn.setText('Remove')
        index = QtCore.QPersistentModelIndex(self.tableWidget.model().index(rowPosition, 5))
        btn.clicked.connect(lambda: self.removeInvoiceItem(index))
        self.tableWidget.setCellWidget(rowPosition, 5, btn)


    def removeInvoiceItem(self, index):
        if index.isValid():
          self.tableWidget.removeRow(index.row())


    def generateInvoice(self):
        file_name = QtGui.QFileDialog.getSaveFileName(self, 'Save file', 'invoice.pdf', filter = 'pdf (*.pdf *.)')

        filepath = os.environ['HOME'] + '/.skilld-tools/settings/invoice.json'
        banking_items = {}
        if os.path.isfile(filepath):
          conf = self.__sdTools.getConf(filepath)
          banking_items = OrderedDict(sorted(conf['banking_items']['elements'].items()))
          data = {
            'billing_items': {
              'elements': {},
              'amount': 0,
              'billing_name': conf['billing_items']['username']
            },
            'banking_items': {
              'elements': banking_items,
              'amount': 0
            }
          }
        allRows = self.tableWidget.rowCount()
        for row in range(0, allRows):
          element = {
            'billing_code': '',
            'billing_concept': '',
            'billing_units': '',
            'billing_value': '',
            'billing_total': ''
          }
          # Let's get needed values.
          code = self.tableWidget.item(row, 0)
          if code:
            element['billing_code'] = code.text()
          description = self.tableWidget.item(row, 1)
          if description:
            element['billing_concept'] = description.text()
          units = self.tableWidget.item(row, 2)
          if units:
            element['billing_units'] = units.text()
          price = self.tableWidget.item(row, 3)
          if price:
            element['billing_value'] = price.text()
          total = self.tableWidget.item(row, 4)
          if total:
            element['billing_total'] = total.text()

          data['billing_items']['amount'] += 1
          data['billing_items']['elements'][row] = element
        # Now, output file.
        template_path = __skilld_tools_vars__['INSTALL_DIR'] + '/templates/default/default.html'
        self.__sdTools.generate(template_path, data, file_name)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = invoiceUI(None)
    window.show()
    app.exec_()
 
