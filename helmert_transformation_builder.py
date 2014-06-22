# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from numpy import *

class HelmertTransformationBuilder(QObject):    
    def __init__(self, control_points):
        QObject.__init__(self)
        
        self.control_points = control_points
        
        self.calculate_scale = True
        self.calculate_rotation = True
        
        self.A = None
        self.l = None
        self.x = None
        self.v = None
        
    def estimate_scale(self, flag):
        self.calculate_scale = flag

    def estimate_rotation(self, flag):
        self.calculate_rotation = flag

    def run(self):
        # 4-Parameter-Loesung wird IMMER gerechnet. Fuer die
        # 2 und 3 Parameter-Loesung dient sie als Naeherungsloesung.
        for gcp in self.control_points:  
            
            if gcp.is_checked() == False:
                continue
            
            if self.A is None:
                self.A = array( [ [1,  0,  float(gcp.get_x_local()),-1*float(gcp.get_y_local())] ] )
                self.A = append(self.A, [ [0,  1,  float(gcp.get_y_local()), float(gcp.get_x_local())] ], axis=0 )
            else:
                self.A = append(self.A, [ [1,  0,  float(gcp.get_x_local()), -1*float(gcp.get_y_local())] ], axis=0 )
                self.A = append(self.A, [ [0,  1,  float(gcp.get_y_local()), float(gcp.get_x_local())] ], axis=0 )
                
            if self.l is None:
                self.l = array( [ [float(gcp.get_x_global())], [float(gcp.get_y_global())] ] )
            else:
                self.l = append(self.l, [[float(gcp.get_x_global())]],  axis=0)
                self.l = append(self.l, [[float(gcp.get_y_global())]],  axis=0)
        
        self.x = dot( dot( linalg.inv( dot( transpose(self.A),  self.A)),  transpose(self.A) ),  self.l)
        self.v = dot( self.A,  self.x ) - self.l

        a = self.x[0]
        a = a[0]
        b = self.x[1]
        b = b[0]
        
        c = self.x[2]
        c = c[0]
        d = self.x[3]
        d = d[0]
        
        m = (c**2 + d**2 )**0.5
        alpha = math.degrees(math.acos ( c / m ) ) / 0.9
        
        # Parameter fuer die iterativen Loesungen (2-3-Parameter).
        self.alpha_diff = None
        self.alpha_tmp = math.radians(alpha * 0.9)
        self.scale_diff = None
        self.scale_tmp = m
        self.tx_tmp = a
        self.ty_tmp = b
        
        print "scale: " + str(m)
        print "rotation: " + str(alpha)
        print "a: " + str(a)
        print "b: " + str(b)
        
        print "Massstab: " + str(self.calculate_scale)
        print "Rotation: " + str(self.calculate_rotation)
        
        # 4-Parameter-Loesung, fertig.
        if self.calculate_scale is True and self.calculate_rotation is True:
            print  [a, b, c, d]
            return [a, b, c, d, None, None]
            
        # 2-Parameter-Loesung, nur Translation.
        if self.calculate_scale is False and self.calculate_rotation is False:
            for i in range(0, 1000):
                print i
                
                self.A = None
                self.l = None
                
                for gcp in self.control_points:  
                    if gcp.is_checked() is False:
                        continue
                        
                    if self.A is None:
                        self.A = array( [ [1,  0] ] )
                        self.A = append(self.A, [ [0,  1] ], axis=0 )
                    else:
                        self.A = append(self.A, [ [1,  0] ], axis=0 )
                        self.A = append(self.A, [ [0,  1] ], axis=0 )

                    # f(tx0,ty0)
                    f0_x = self.tx_tmp + 1*math.cos(0)*float(gcp.get_x_local()) - 1*math.sin(0)*float(gcp.get_y_local())
                    f0_y = self.ty_tmp + 1*math.sin(0)*float(gcp.get_x_local()) + 1*math.cos(0)*float(gcp.get_y_local())

                    if self.l is None:
                        self.l = array( [ [float(gcp.get_x_global()) - f0_x],  [float(gcp.get_y_global()) - f0_y] ] )
                    else:
                        self.l = append(self.l,  [[float(gcp.get_x_global()) - f0_x]],  axis=0)
                        self.l = append(self.l,  [[float(gcp.get_y_global()) - f0_y]],  axis=0)

                self.x = dot( dot( linalg.inv( dot( transpose(self.A),  self.A)),  transpose(self.A) ),  self.l)
                self.v = dot( self.A,  self.x ) - self.l

                self.tx_diff = self.x[0][0]
                self.ty_diff = self.x[1][0]

                self.tx_tmp = self.tx_tmp + self.x[0][0]
                self.ty_tmp = self.ty_tmp + self.x[1][0]

                if math.fabs(self.tx_diff) < 0.0001 and math.fabs(self.ty_diff) < 0.0001:
                    a = self.tx_tmpisChe
                    b = self.ty_tmp
                    c = 1
                    d = 0
                    print  [a, b, c, d]
                    return [a, b, c, d, None, None]
            
        # 3-Parameter-Loesung, Rotation wird nicht geschaetzt.
        if self.calculate_scale is True and self.calculate_rotation is False:
            for i in range(0, 1000):
                print i
                
                self.A = None
                self.l = None
                
                for gcp in self.control_points:  
                    if gcp.is_checked() == False:
                        continue

                    if self.A is None:
                        self.A = array( [ [1,  0, math.cos(0)*float(gcp.get_x_local()) - math.sin(0)*float(gcp.get_y_local())] ] )
                        self.A = append(self.A, [ [0,  1, math.sin(0)*float(gcp.get_x_local()) - math.cos(0)*float(gcp.get_y_local())] ], axis=0 )
                    else:
                        self.A = append(self.A, [ [1,  0,  math.cos(0)*float(gcp.get_x_local()) - math.sin(0)*float(gcp.get_y_local())] ], axis=0 )
                        self.A = append(self.A, [ [0,  1,  math.sin(0)*float(gcp.get_x_local()) - math.cos(0)*float(gcp.get_y_local())] ], axis=0 )

                    # f(tx0,ty0,scale0)
                    f0_x = self.tx_tmp + self.scale_tmp*math.cos(0)*float(gcp.get_x_local()) - self.scale_tmp*math.sin(0)*float(gcp.get_y_local())
                    f0_y = self.ty_tmp + self.scale_tmp*math.sin(0)*float(gcp.get_x_local()) + self.scale_tmp*math.cos(0)*float(gcp.get_y_local())

                    if self.l is None:
                        self.l = array( [ [float(gcp.get_x_global()) - f0_x],  [float(gcp.get_y_global()) - f0_y] ] )
                    else:
                        self.l = append(self.l,  [[float(gcp.get_x_global()) - f0_x]],  axis=0)
                        self.l = append(self.l,  [[float(gcp.get_y_global()) - f0_y]],  axis=0)

                self.x = dot( dot( linalg.inv( dot( transpose(self.A),  self.A)),  transpose(self.A) ),  self.l)
                self.v = dot( self.A,  self.x ) - self.l

                self.tx_diff = self.x[0][0]
                self.ty_diff = self.x[1][0]
                self.scale_diff = self.x[2][0]

                self.tx_tmp = self.tx_tmp + self.x[0][0]
                self.ty_tmp = self.ty_tmp + self.x[1][0]
                self.scale_tmp =  self.scale_tmp + self.x[2][0]

                if math.fabs(self.scale_diff) < 0.00000001 and math.fabs(self.tx_diff) < 0.0001 and math.fabs(self.ty_diff) < 0.0001:
                    a = self.tx_tmp
                    b = self.ty_tmp
                    c = self.scale_tmp
                    d = 0
                    print  [a, b, c, d]
                    return [a, b, c, d, None, None]

        # 3-Parameter-Loesung, Massstab wird nicht geschaetzt.
        if self.calculate_scale is False and self.calculate_rotation is True:
            for i in range(0, 1000):
                print i
                
                self.A = None
                self.l = None
                
                for gcp in self.control_points:  
                    if gcp.is_checked() == False:
                        continue

                    if self.A is None:
                        self.A = array( [ [1,  0,  -1*float(gcp.get_x_local())*math.sin(self.alpha_tmp) - 1*float(gcp.get_y_local())*math.cos(self.alpha_tmp)] ] )
                        self.A = append(self.A, [ [0,  1,  float(gcp.get_x_local())*math.cos(self.alpha_tmp) - 1*float(gcp.get_y_local())*math.sin(self.alpha_tmp)] ], axis=0 )
                    else:
                        self.A = append(self.A, [ [1,  0,  -1*float(gcp.get_x_local())*math.sin(self.alpha_tmp) - 1*float(gcp.get_y_local())*math.cos(self.alpha_tmp)] ], axis=0 )
                        self.A = append(self.A, [ [0,  1,  float(gcp.get_x_local())*math.cos(self.alpha_tmp) - 1*float(gcp.get_y_local())*math.sin(self.alpha_tmp)] ], axis=0 )

                    # f(tx0,ty0,alpha0)
                    f0_x = self.tx_tmp + math.cos(self.alpha_tmp)*float(gcp.get_x_local()) - math.sin(self.alpha_tmp)*float(gcp.get_y_local())
                    f0_y = self.ty_tmp + math.sin(self.alpha_tmp)*float(gcp.get_x_local()) + math.cos(self.alpha_tmp)*float(gcp.get_y_local())
          
                    if self.l is None:
                        self.l = array( [ [float(gcp.get_x_global()) - f0_x],  [float(gcp.get_y_global()) - f0_y] ] )
                    else:
                        self.l = append(self.l,  [[float(gcp.get_x_global()) - f0_x]],  axis=0)
                        self.l = append(self.l,  [[float(gcp.get_y_global()) - f0_y]],  axis=0)

                self.x = dot( dot( linalg.inv( dot( transpose(self.A),  self.A)),  transpose(self.A) ),  self.l)
                self.v = dot( self.A,  self.x ) - self.l

                self.tx_diff = self.x[0][0]
                self.ty_diff = self.x[1][0]
                self.alpha_diff = self.x[2][0]

                self.tx_tmp = self.tx_tmp + self.x[0][0]
                self.ty_tmp = self.ty_tmp + self.x[1][0]
                self.alpha_tmp =  self.alpha_tmp + self.x[2][0]

                if math.fabs(self.alpha_diff) < 0.000001 and math.fabs(self.tx_diff) < 0.0001 and math.fabs(self.ty_diff) < 0.0001:
                    a = self.tx_tmp
                    b = self.ty_tmp
                    c = math.cos(self.alpha_tmp)
                    d = math.sin(self.alpha_tmp)
                    print  [a, b, c, d]
                    return [a, b, c, d, None, None]
                    
            # Not able to find a solution.    
            return None

