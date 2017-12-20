import sys
from PyQt4 import QtCore, QtGui, uic
from skilld_tools import __main__

app = QtGui.QApplication(sys.argv)
window = __main__.main(None)
window.show()
app.exec_()
