# -*- coding: latin1 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *


class HelmertTransformation(QObject):    
    def __init__(self, parameters):
        QObject.__init__(self)
 
        self.a = parameters[0]
        self.b = parameters[1]
        self.c = parameters[2]
        self.d = parameters[3]

    def transform_simple_points(self, points):
        transformed_points = []
        for point in points:
            x, y = self.transform_simple_point(point)
            point.set_x_trans(x)
            point.set_y_trans(y)
            transformed_points.append(point)
        return transformed_points
            
    def transform_simple_point(self, point):
            x = self.a + self.c*float(point.get_x_local()) - self.d*float(point.get_y_local())
            y = self.b + self.d*float(point.get_x_local()) + self.c*float(point.get_y_local())
            return x, y
        

