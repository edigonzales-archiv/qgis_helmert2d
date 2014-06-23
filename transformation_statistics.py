# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import os, time

class TransformationStatistics(QObject):
    
    def __init__(self, points, transformation_type, estimate_scale, estimate_rotation):
        
            self.u = None
            self.num_gcp = 0
            sum_vx = 0
            sum_vy = 0
            
            self.m0 = None
            self.mpkt = None

            for point in points:
                
                if point.is_checked() == False:
                    continue
                
                self.num_gcp += 1
                
                vx = (float(point.get_x_trans()) - float(point.get_x_global())) * 1000
                vy = (float(point.get_y_trans()) - float(point.get_y_global())) * 1000

                sum_vx = sum_vx + vx*vx
                sum_vy = sum_vy + vy*vy
            
            if transformation_type == 1:
                self.u = 2
                if estimate_scale == True:
                   self.u += 1
                if estimate_rotation == True:
                   self.u += 1
            elif transformation_type == 2:
                self.u = 6
    
            self.m0 = ((sum_vx + sum_vy) / (2*self.num_gcp - self.u))**0.5
            self.mpkt = 2**0.5 * self.m0

    def number_of_gcp(self):
        return self.num_gcp
        
    def number_of_parameters(self):
        return self.u
        
    def deviation_of_residual(self):
        return self.m0
        s
    def deviation_of_point(self):
        return self.mpkt
    
    

        
