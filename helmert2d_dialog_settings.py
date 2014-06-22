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
    os.path.dirname(__file__), 'helmert2d_dialog_settings.ui'))


class Helmert2DDialogSettings(QDialog, FORM_CLASS):
        
    def __init__(self, parent=None):
        """Constructor."""
        super(Helmert2DDialogSettings, self).__init__(parent)
        self.setupUi(self)
        
        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)        
        self.connect(self.okButton, SIGNAL("accepted()"), self.accept)        
        
        self.settings = QSettings("CatAIS","Helmert2D")
        self.export_directory = self.settings.value("settings/export_directory")
        self.decimal_places = self.settings.value("settings/decimal_places", 3)
        
        self.lineEditExport.setText(self.export_directory)
        self.spinBoxDecimalPlaces.setValue(int(self.decimal_places))
        
    def tr(self, message):
        return QCoreApplication.translate('Helmert2D', message)

    @pyqtSignature("on_pushButtonExport_clicked()")    
    def on_pushButtonExport_clicked(self):
        dir = QFileDialog.getExistingDirectory(self, self.tr("Choose export directory"), self.export_directory)
        dir_info = QFileInfo(dir)
        self.lineEditExport.setText(dir_info.absoluteFilePath())
        
    def accept(self):
        print "ACCEPT99999"
        self.settings.setValue("settings/export_directory", self.lineEditExport.text())
        self.settings.setValue("settings/decimal_places", self.spinBoxDecimalPlaces.value())
        self.close()
        
