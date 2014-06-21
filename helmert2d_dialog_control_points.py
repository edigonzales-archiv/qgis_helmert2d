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
from qgis.core import *
from qgis.gui import *


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'helmert2d_dialog_control_points.ui'))


class Helmert2DDialogControlPoints(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(Helmert2DDialogControlPoints, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        # Rename OK button and connect to custom accept method.
        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.okButton.setText(self.tr(u"Identify"))
        self.connect(self.okButton, SIGNAL("accepted()"), self.accept)        
        
        # Connect layer comboboxes with the field comboboxes.
        # New style PyQt connections syntax!
        self.globalLayerCombo.layerChanged.connect(self.globalLayerChanged)
        self.globalLayerCombo.setLayer(self.globalLayerCombo.currentLayer()) # Emits signal on initialisation. Why it is necessary?
        
        self.localLayerCombo.layerChanged.connect(self.localLayerChanged)
        self.localLayerCombo.setLayer(self.localLayerCombo.currentLayer()) # Emits signal on initialisation. Why it is necessary?
        
        self.bar = QgsMessageBar(self)
        self.bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        self.gridLayout.addWidget(self.bar, 0, 0, Qt.AlignTop)  

    @pyqtSlot(QgsMapLayer)
    def globalLayerChanged(self, layer):
        print "globalLayerChanged"
        self.globalFieldCombo.setLayer(layer)

    @pyqtSlot(QgsMapLayer)
    def localLayerChanged(self, layer):
        print "localLayerChanged"
        self.localFieldCombo.setLayer(layer)
        
    def accept(self):
        print "ACCEPT"
        
        if self.globalLayerCombo.currentLayer() in (None, '') or self.localLayerCombo.currentLayer() in (None, ''):
            self.bar.pushMessage(self.tr(u"Warning"), self.tr(u"Missing global or local layer."), level=QgsMessageBar.WARNING)
            return
    
        if self.globalFieldCombo.currentField() in (None, '') or self.localFieldCombo.currentField() in (None, ''):
#            self.bar.pushMessage(QCoreApplication.translate('Helmert2D', "Warning"), QCoreApplication.translate('Helmert2D', "Missing global or local identifier attribute."), level=QgsMessageBar.WARNING)
            QMessageBox.information(None, "Helmert2D", self.tr(u"Missing global or local identifier attribute."))
            return
    
        if self.globalLayerCombo.currentIndex() == self.localLayerCombo.currentIndex():
            reply = QMessageBox.question(None, "Helmert2D", self.tr(u"Do you want to use the same layer twice?"), QMessageBox.Yes|QMessageBox.No)
            if reply == QMessageBox.No:
                return
            print "gagagagagaga"
            return   
        
    def tr(self, message):
        return QCoreApplication.translate('Helmert2D', message)
