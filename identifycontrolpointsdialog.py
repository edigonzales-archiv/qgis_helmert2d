# -*- coding: utf-8 -*-
from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import os

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_identifycontrolpoints.ui'))

class IdentifyControlPointsDialog(QDialog, FORM_CLASS):
    
    controlPointsLayerChosen = pyqtSignal(QgsMapLayer, QgsMapLayer, str, str)
    
    def __init__(self, parent=None):
        super(IdentifyControlPointsDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)
        self.okButton.setText(self.tr(u"Identify"))
        self.connect(self.okButton, SIGNAL("accepted()"), self.accept)        
        
        # Connect layer comboboxes with the field comboboxes.
        # New style PyQt connections syntax!
        self.globalLayerCombo.layerChanged.connect(self.globalLayerChanged)
        self.globalLayerCombo.setLayer(self.globalLayerCombo.currentLayer()) # Emits signal on initialisation. Why is it necessary?
        
        self.localLayerCombo.layerChanged.connect(self.localLayerChanged)
        self.localLayerCombo.setLayer(self.localLayerCombo.currentLayer()) # Emits signal on initialisation. Why is it necessary?
    
    def tr(self, message):
        return QCoreApplication.translate('Helmert2D', message)

    @pyqtSlot(QgsMapLayer)
    def globalLayerChanged(self, layer):
        self.globalFieldCombo.setLayer(layer)

    @pyqtSlot(QgsMapLayer)
    def localLayerChanged(self, layer):
        self.localFieldCombo.setLayer(layer)
        
    def accept(self):
        if self.globalLayerCombo.currentLayer() in (None, '') or self.localLayerCombo.currentLayer() in (None, ''):
            QMessageBox.information(None, "Helmert2D", _translate("Helmert2D", "Missing global or local layer.", None))
            return
    
        if self.globalFieldCombo.currentField() in (None, '') or self.localFieldCombo.currentField() in (None, ''):
            QMessageBox.information(None, "Helmert2D", _translate("Helmert2D", "Missing global or local identifiere attribute.", None))
            return
    
        if self.globalLayerCombo.currentIndex() == self.localLayerCombo.currentIndex():
            reply = QMessageBox.question(None, "Helmert2D", _translate("Helmert2D", "Do you want to use the same layer twice?", None), QMessageBox.Yes|QMessageBox.No)
            if reply == QMessageBox.No:
                return

        self.controlPointsLayerChosen.emit(self.globalLayerCombo.currentLayer(), self.localLayerCombo.currentLayer(), self.globalFieldCombo.currentField(), self.localFieldCombo.currentField())
        
