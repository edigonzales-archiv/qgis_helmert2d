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
import math

from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from helmert2d_dialog_control_points import Helmert2DDialogControlPoints
from helmert2d_dialog_settings import Helmert2DDialogSettings
from helmert_transformation_builder import HelmertTransformationBuilder
from helmert_transformation import HelmertTransformation 
from transformation_statistics import TransformationStatistics
from point import Point

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'helmert2d_dialog_base.ui'))


class Helmert2DDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(Helmert2DDialog, self).__init__(parent)
        self.setupUi(self)

        self.settings = QSettings("CatAIS","Helmert2D")
        
    def initGui(self):
        self.init_table_widget()
        self.init_transformation_tab()
        
    def tr(self, message):
        return QCoreApplication.translate('Helmert2D', message)

    @pyqtSignature("on_transformBtn_clicked()")    
    def on_transformBtn_clicked(self):
        self.estimate_parameters()        

    @pyqtSignature("on_toolBtnSettings_clicked()")    
    def on_toolBtnSettings_clicked(self):
        self.dlg = Helmert2DDialogSettings()
        self.dlg.show()
        
    @pyqtSignature("on_toolBtnIdentify_clicked()")    
    def on_toolBtnIdentify_clicked(self):
        self.dlg = Helmert2DDialogControlPoints()
        self.dlg.show()
        self.dlg.identifyControlPoints.connect(self.identify_control_points)

    @pyqtSlot(QgsMapLayer, QgsMapLayer, str, str)
    def identify_control_points(self, global_layer, local_layer, global_field, local_field):
        control_points = []
        
        global_iter = global_layer.getFeatures()
        for global_feature in global_iter:
            idx = global_layer.fieldNameIndex(global_field)
            global_ident = global_feature.attributes()[idx]
            global_geom = global_feature.geometry()

            local_iter = local_layer.getFeatures()
            for local_feature in local_iter:
                idx = local_layer.fieldNameIndex(local_field)
                local_ident = local_feature.attributes()[idx]
                local_geom = local_feature.geometry()

                if local_ident == global_ident:
                    gcp = Point(global_ident)
                    gcp.set_x_global(global_geom.asPoint().x())
                    gcp.set_y_global(global_geom.asPoint().y())
                    gcp.set_x_local(local_geom.asPoint().x())
                    gcp.set_y_local(local_geom.asPoint().y())
                    
                    control_points.append(gcp)
                    break
        
        # insert points into table widget
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(control_points))
        
        # get decimal places from settings
        decimal_places = str(self.settings.value("settings/decimal_places", 3))

        i = 0
        for control_point in control_points:
            text = str("%."+decimal_places+"f") % float(control_point.get_x_local())
            item = QTableWidgetItem(text)  
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)    
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tableWidget.setItem(i, 0, item)  

            text = str("%."+decimal_places+"f") % float(control_point.get_y_local())
            item = QTableWidgetItem(text)  
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)    
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tableWidget.setItem(i, 1, item)  

            text = str("%."+decimal_places+"f") % float(control_point.get_x_global())
            item = QTableWidgetItem(text)  
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)    
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tableWidget.setItem(i, 2, item)  
            
            text = str("%."+decimal_places+"f") % float(control_point.get_y_global())
            item = QTableWidgetItem(text)  
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)    
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tableWidget.setItem(i, 3, item)  
            
            item = QTableWidgetItem()  
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)    
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tableWidget.setItem(i, 4, item)    
            
            item = QTableWidgetItem()  
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)    
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tableWidget.setItem(i, 5, item)              
            
            text = str(control_point.get_ident())
            item = QTableWidgetItem(text)  
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)    
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tableWidget.setItem(i, 6, item)  
            
            cb = QCheckBox()
            cb.setCheckState(Qt.Checked) 
            
            layout1 = QHBoxLayout()
            layout1.addWidget(cb)
            layout1.setMargin(2)
            layout1.insertSpacing(0, 10)
            layout1.setAlignment(Qt.AlignCenter)
            
            frame1 = QFrame()
            frame1.setLayout(layout1)       

            self.tableWidget.setCellWidget(i, 7, frame1)                    
            
            i += 1
        
    @pyqtSignature("on_comboTransformationType_currentIndexChanged(int)")      
    def on_comboTransformationType_currentIndexChanged(self, idx):    
        self.lineEditParameterA.clear()
        self.lineEditParameterB.clear()
        self.lineEditParameterC.clear()
        self.lineEditParameterD.clear()        
        self.lineEditParameterE.clear()
        self.lineEditParameterF.clear()
        self.lineEditParameterX0.clear()
        self.lineEditParameterY0.clear()
        self.lineEditParameterRotation.clear()
        self.lineEditParameterScale.clear()
        self.lineEditParameterM0.clear()
        self.lineEditParameterMPoint.clear()

        self.trans_type = self.comboTransformationType.itemData(idx)
        if self.trans_type == 1:
            self.labelParameterE.setEnabled(False)
            self.labelParameterF.setEnabled(False)
            self.lineEditParameterE.setEnabled(False)
            self.lineEditParameterF.setEnabled(False)
            self.cbEstimateScale.setEnabled(True)
            self.cbEstimateRotation.setEnabled(True)
            self.labelEstimateScale.setEnabled(True)
            self.labelEstimateRotation.setEnabled(True)            
            
            self.labelParameterY0.setEnabled(True)
            self.labelParameterX0.setEnabled(True)
            self.labelParameterRotation.setEnabled(True)
            self.labelParameterScale.setEnabled(True)
            self.lineEditParameterY0.setEnabled(True)
            self.lineEditParameterX0.setEnabled(True)
            self.lineEditParameterRotation.setEnabled(True)
            self.lineEditParameterScale.setEnabled(True)
            
        elif self.trans_type == 2:
            self.labelParameterE.setEnabled(True)
            self.labelParameterF.setEnabled(True)
            self.lineEditParameterE.setEnabled(True)
            self.lineEditParameterF.setEnabled(True)
            self.cbEstimateScale.setEnabled(False)
            self.cbEstimateRotation.setEnabled(False)
            self.labelEstimateScale.setEnabled(False)
            self.labelEstimateRotation.setEnabled(False)

            self.labelParameterY0.setEnabled(False)
            self.labelParameterX0.setEnabled(False)
            self.labelParameterRotation.setEnabled(False)
            self.labelParameterScale.setEnabled(False)
            self.lineEditParameterY0.setEnabled(False)
            self.lineEditParameterX0.setEnabled(False)
            self.lineEditParameterRotation.setEnabled(False)
            self.lineEditParameterScale.setEnabled(False)
        
    def estimate_parameters(self):
        if self.tableWidget.rowCount() == 0:
            QMessageBox.information(None, "Helmert2D", self.tr(u"No control points found."))
            return
            
        QApplication.setOverrideCursor(Qt.WaitCursor)            
        try:
            # Read control points from the table.
            control_points = []
            checked_points = 0
            
            for i in range(self.tableWidget.rowCount()):
                check_state = self.tableWidget.cellWidget(i, 7).layout().itemAt(1).widget().checkState()
                checked = False
                if check_state == Qt.Checked:
                    checked = True
                    checked_points += 1
                    
                item = self.tableWidget.item(i, 6)
                id = item.text()
                
                item = self.tableWidget.item(i, 0)            
                x_local = item.text()

                item = self.tableWidget.item(i, 1)            
                y_local = item.text()
                
                item = self.tableWidget.item(i, 2)            
                x_global = item.text()

                item = self.tableWidget.item(i, 3)            
                y_global = item.text()
                
                gcp = Point(id)
                gcp.set_x_local(x_local)
                gcp.set_y_local(y_local)
                gcp.set_x_global(x_global)
                gcp.set_y_global(y_global)
                gcp.set_checked(checked)
                
                control_points.append(gcp)

            # Check if there are enough points for the transformation 
            # (-> different for helmert and affine).        
            if self.trans_type == 1:
                if checked_points < 2:
                    QMessageBox.warning( None, "Helmert2D", self.tr("No enough control points for helmert transformation." ))
                    return    
            elif self.trans_type == 2:
                if checked_points < 3:
                    QMessageBox.warning( None, "Helmert2D", self.tr("No enough control points for affine transformation." ))
                    return    

            # Calculate transformation parameters.
            transformation_parameters = None
            if self.trans_type == 1:
                builder = HelmertTransformationBuilder(control_points)
                builder.estimate_scale(self.cbEstimateScale.isChecked())
                builder.estimate_rotation(self.cbEstimateRotation.isChecked())
                transformation_parameters = builder.run()

            # Transformed coordinates of the control points.
            if transformation_parameters:
                transformation = HelmertTransformation(transformation_parameters)
                transformed_control_points = transformation.transform_simple_points(control_points)
    #            print "Anzahl Passpunkte (inkl. unchecked ones): " + str(len(transformed_control_points))
        
            # Write residuals into control points table.
            # We delete everything first.
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(len(transformed_control_points))
            
            decimal_places = str(self.settings.value("settings/decimal_places", 3))
            decimal_places_residuals = str(self.settings.value("settings/decimal_places_residuals", 1))
            unit_residual = str(self.settings.value("settings/unit_residuals", "mm"))
            if unit_residual == "mm":
                residual_factor = 1000
            else:
                residual_factor = 1

            i = 0
            for control_point in transformed_control_points:
                text = str("%."+decimal_places+"f") % float(control_point.get_x_local())
                item = QTableWidgetItem(text)  
                if not control_point.is_checked():
                    item.setTextColor(Qt.gray)
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)    
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.tableWidget.setItem(i, 0, item)  

                text = str("%."+decimal_places+"f") % float(control_point.get_y_local())
                item = QTableWidgetItem(text)  
                if not control_point.is_checked():
                    item.setTextColor(Qt.gray)            
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)    
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.tableWidget.setItem(i, 1, item)  

                text = str("%."+decimal_places+"f") % float(control_point.get_x_global())
                item = QTableWidgetItem(text)  
                if not control_point.is_checked():
                    item.setTextColor(Qt.gray)            
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)    
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.tableWidget.setItem(i, 2, item)  
                
                text = str("%."+decimal_places+"f") % float(control_point.get_y_global())
                item = QTableWidgetItem(text)  
                if not control_point.is_checked():
                    item.setTextColor(Qt.gray)            
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)    
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.tableWidget.setItem(i, 3, item)  
                
                vx = (float(control_point.get_x_trans()) - float(control_point.get_x_global())) * residual_factor
                text = str("%."+decimal_places_residuals+"f") % vx
                item = QTableWidgetItem(text)  
                if not control_point.is_checked():
                    item.setTextColor(Qt.gray)                        
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)    
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.tableWidget.setItem(i, 4, item)    
                
                vy = (float(control_point.get_y_trans()) - float(control_point.get_y_global())) * residual_factor
                text = str("%."+decimal_places_residuals+"f") % vy
                item = QTableWidgetItem(text)  
                if not control_point.is_checked():
                    item.setTextColor(Qt.gray)                        
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)    
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.tableWidget.setItem(i, 5, item)              
                
                text = str(control_point.get_ident())
                item = QTableWidgetItem(text)  
                if not control_point.is_checked():
                    item.setTextColor(Qt.gray)            
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)    
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.tableWidget.setItem(i, 6, item)  
                
                cb = QCheckBox()
                if control_point.is_checked():
                    cb.setCheckState(Qt.Checked) 
                else:
                    cb.setCheckState(Qt.Unchecked) 
                
                cb.clicked.connect(self.estimate_parameters)

                layout1 = QHBoxLayout()
                layout1.addWidget(cb)
                layout1.setMargin(2)
                layout1.insertSpacing(0, 10)
                layout1.setAlignment(Qt.AlignCenter)
                
                frame1 = QFrame()
                frame1.setLayout(layout1)       

                self.tableWidget.setCellWidget(i, 7, frame1)                    
                
                i += 1

            # Update transformation parameters in GUI.
            a = str("%.12f") % transformation_parameters[0]
            b = str("%.12f") % transformation_parameters[1]
            c = str("%.12f") % transformation_parameters[2]
            d = str("%.12f") % transformation_parameters[3]
            if transformation_parameters[4]:
                e= str("%.12f") % transformation_parameters[4]
            else:
                e = None
            if transformation_parameters[5]:
                f = str("%.12f") % transformation_parameters[d]
            else:
                f = None

            self.lineEditParameterA.setText(a)
            self.lineEditParameterB.setText(b)
            self.lineEditParameterC.setText(c)
            self.lineEditParameterD.setText(d)
            if e:
                self.lineEditParameterE.setText(e)
            else:
                self.lineEditParameterE.setText("")
            if f:
                self.lineEditParameterF.setText(f)
            else:
                self.lineEditParameterF.setText("")

            if not e  and not f:            
                a = transformation_parameters[0]
                b = transformation_parameters[1] 
                c = transformation_parameters[2] 
                d = transformation_parameters[3] 

                tx = str("%.4f") % a
                ty = str("%.4f") % b

                rot = math.degrees(math.atan(float(d)/float(c))) / 0.9
                m = float(c) / math.cos(rot)
                ppm = (1 - m) * 1000000
                
                ppm = str("%.4f") % ppm
                rot = str("%.8f") % rot
            
                self.lineEditParameterX0.setText(tx)
                self.lineEditParameterY0.setText(ty)
                self.lineEditParameterRotation.setText(rot)
                self.lineEditParameterScale.setText(ppm)
                
                statistics = TransformationStatistics(transformed_control_points, self.trans_type, self.cbEstimateScale.isChecked(), self.cbEstimateRotation.isChecked())
                m0 = statistics.deviation_of_residual()
                mpnt = statistics.deviation_of_point()
            
                m0 = str("%.1f") % m0
                mpnt = str("%.1f") % mpnt
                
                self.lineEditParameterM0.setText(m0)
                self.lineEditParameterMPoint.setText(mpnt)
                
        except:
            QApplication.restoreOverrideCursor()
        QApplication.restoreOverrideCursor()
        
    def init_transformation_tab(self):
        self.comboTransformationType.addItem(self.tr("Helmert (2 - 4 parameter)"),  int(1))
        self.comboTransformationType.addItem(self.tr("Affine (6 parameter)"),  int(2))

    def init_table_widget(self):
        self.tableWidget.setRowCount(0)       
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(8)

        item = QTableWidgetItem()
        item.setText(self.tr("X local"))
        self.tableWidget.setHorizontalHeaderItem(0, item)
        
        item = QTableWidgetItem()
        item.setText(self.tr("Y local"))
        self.tableWidget.setHorizontalHeaderItem(1, item)        
        
        item = QTableWidgetItem()
        item.setText(self.tr("X global"))
        self.tableWidget.setHorizontalHeaderItem(2, item)
        
        item = QTableWidgetItem()
        item.setText(self.tr("Y global"))
        self.tableWidget.setHorizontalHeaderItem(3, item)             
        
        item = QTableWidgetItem()
        item.setText(self.tr("vx"))
        self.tableWidget.setHorizontalHeaderItem(4, item)
        
        item = QTableWidgetItem()
        item.setText(self.tr("vy"))
        self.tableWidget.setHorizontalHeaderItem(5, item)             

        item = QTableWidgetItem()
        item.setText(self.tr("Control point"))
        self.tableWidget.setHorizontalHeaderItem(6, item)             

        item = QTableWidgetItem()
        item.setText(self.tr("use it"))
        self.tableWidget.setHorizontalHeaderItem(7, item)
