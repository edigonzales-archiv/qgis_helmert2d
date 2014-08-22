# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from point import Point

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class ControlPointsTable(QTableWidget):
    def __init__(self, parent = None):
        super(QTableWidget, self).__init__(parent)
        
        self.settings = QSettings("CatAIS","Helmert2D")

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
                
    def insertControlPoints(self, control_points):
        self.clearContents()
        self.setRowCount(len(control_points))
        
        decimal_places = str(self.settings.value("settings/decimal_places", 3))

        i = 0
        for control_point in control_points:
            text = str("%."+decimal_places+"f") % float(control_point.get_x_local())
            item = QTableWidgetItem(text)  
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)    
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
            self.setItem(i, 0, item)  

            text = str("%."+decimal_places+"f") % float(control_point.get_y_local())
            item = QTableWidgetItem(text)  
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)    
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
            self.setItem(i, 1, item)  

            text = str("%."+decimal_places+"f") % float(control_point.get_x_global())
            item = QTableWidgetItem(text)  
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)    
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
            self.setItem(i, 2, item)  
            
            text = str("%."+decimal_places+"f") % float(control_point.get_y_global())
            item = QTableWidgetItem(text)  
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)    
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
            self.setItem(i, 3, item)  
            
            item = QTableWidgetItem()  
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)    
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.setItem(i, 4, item)    
            
            item = QTableWidgetItem()  
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)    
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.setItem(i, 5, item)              
            
            text = str(control_point.get_ident())
            item = QTableWidgetItem(text)  
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)    
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
            self.setItem(i, 6, item)  
            
            cb = QCheckBox()
            cb.setCheckState(Qt.Checked) 
            
            layout1 = QHBoxLayout()
            layout1.addWidget(cb)
            layout1.setMargin(2)
            layout1.insertSpacing(0, 10)
            layout1.setAlignment(Qt.AlignCenter)
            
            frame1 = QFrame()
            frame1.setLayout(layout1)       

            self.setCellWidget(i, 7, frame1)                    
            
            i += 1
        
