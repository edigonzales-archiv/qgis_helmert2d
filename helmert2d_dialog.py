# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Helmert2DDialog
                                 A QGIS plugin
 Helmert2D transformation
                             -------------------
        begin                : 2014-06-09
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Stefan Ziegler
        email                : edi.gonzales@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from helmert2d_dialog_control_points import Helmert2DDialogControlPoints


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'helmert2d_dialog_base.ui'))


class Helmert2DDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(Helmert2DDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # Headers etc of the table widget.
        self.initTableWidget()


    @pyqtSignature("on_toolBtnIdentify_clicked()")    
    def on_toolBtnIdentify_clicked(self):
        self.dlg = Helmert2DDialogControlPoints()
        self.dlg.show()
        result = self.dlg.exec_()
        print result
        
        
    def initTableWidget(self):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(8)

#        self.tableWidget.setColumnWidth(0, 45)
#        self.tableWidget.setColumnWidth(1, 85)
#        self.tableWidget.setColumnWidth(2, 85)
#        self.tableWidget.setColumnWidth(3, 85)        
#        self.tableWidget.setColumnWidth(4, 85)
#        self.tableWidget.setColumnWidth(5, 85)
#        self.tableWidget.setColumnWidth(6, 65)                
#        self.tableWidget.setColumnWidth(7, 65) 

        item = QTableWidgetItem()
#        item.setFont(self.sansFont)
        item.setText(QCoreApplication.translate('Helmert2D', "X local"))
        self.tableWidget.setHorizontalHeaderItem(0, item)
        
        item = QTableWidgetItem()
#        item.setFont(self.sansFont)
        item.setText(QCoreApplication.translate('Helmert2D', "Y local"))
        self.tableWidget.setHorizontalHeaderItem(1, item)        
        
        item = QTableWidgetItem()
#        item.setFont(self.sansFont)
        item.setText(QCoreApplication.translate('Helmert2D', "X global"))
        self.tableWidget.setHorizontalHeaderItem(2, item)
        
        item = QTableWidgetItem()
#        item.setFont(self.sansFont)
        item.setText(QCoreApplication.translate('Helmert2D', "Y global"))
        self.tableWidget.setHorizontalHeaderItem(3, item)             
        
        item = QTableWidgetItem()
#        item.setFont(self.sansFont)
        item.setText(QCoreApplication.translate('Helmert2D', "vx"))
        self.tableWidget.setHorizontalHeaderItem(4, item)
        
        item = QTableWidgetItem()
#        item.setFont(self.sansFont)
        item.setText(QCoreApplication.translate('Helmert2D', "vy"))
        self.tableWidget.setHorizontalHeaderItem(5, item)             

        item = QTableWidgetItem()
#        item.setFont(self.sansFont)
        item.setText(QCoreApplication.translate('Helmert2D', "Control point"))
        self.tableWidget.setHorizontalHeaderItem(6, item)             

        item = QTableWidgetItem()
#        item.setFont(self.sansFont)
        item.setText("use it")
        self.tableWidget.setHorizontalHeaderItem(7, item)
