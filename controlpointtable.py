# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class ControlPointTable(QTableWidget):
    def __init__(self, parent = None):
        super(QTableWidget, self).__init__(parent)

    def initGui(self):
        self.setRowCount(0)       
        self.setAlternatingRowColors(True)
        self.setColumnCount(8)

        item = QTableWidgetItem()
        item.setText(_translate("Helmert2D", "X local", None))
        self.setHorizontalHeaderItem(0, item)
        
        item = QTableWidgetItem()
        item.setText(_translate("Helmert2D", "Y local", None))
        self.setHorizontalHeaderItem(1, item)        
        
        item = QTableWidgetItem()
        item.setText(_translate("Helmert2D", "X global", None))
        self.setHorizontalHeaderItem(2, item)
        
        item = QTableWidgetItem()
        item.setText(_translate("Helmert2D", "Y local", None))
        self.setHorizontalHeaderItem(3, item)             
        
        item = QTableWidgetItem()
        item.setText(_translate("Helmert2D", "vx", None))
        self.setHorizontalHeaderItem(4, item)
        
        item = QTableWidgetItem()
        item.setText(_translate("Helmert2D", "vy", None))
        self.setHorizontalHeaderItem(5, item)             

        item = QTableWidgetItem()
        item.setText(_translate("Helmert2D", "Control point", None))
        self.setHorizontalHeaderItem(6, item)             

        item = QTableWidgetItem()
        item.setText(_translate("Helmert2D", "use it", None))
        self.setHorizontalHeaderItem(7, item)
        
        print "fooo"
