# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from numpy import *

class TransformationBuilder(QObject):    
    def __init__(self, control_points):
        QObject.__init__(self)
        
        self.gcps = control_points
        
        self.calcScale = True
        self.calcRotation = True
        
        self.A = None
        self.l = None
        self.x = None
        self.v = None
        
    def estimateScale(self, flag):
        self.calcScale = flag

    def estimateRotation(self, flag):
        self.calcRotation = flag

    def run(self):
        # 4-Parameter-Loesung wird IMMER gerechnet. Fuer die
        # 2 und 3 Parameter-Loesung dient sie als Naeherungsloesung.
        for gcp in self.gcps:  
            
            if gcp.isChecked() == False:
                continue
            
            if self.A == None:
                self.A = array( [ [1,  0,  float(gcp.getXlocal()),-1*float(gcp.getYlocal())] ] )
                self.A = append(self.A, [ [0,  1,  float(gcp.getYlocal()), float(gcp.getXlocal())] ], axis=0 )
            else:
                self.A = append(self.A, [ [1,  0,  float(gcp.getXlocal()), -1*float(gcp.getYlocal())] ], axis=0 )
                self.A = append(self.A, [ [0,  1,  float(gcp.getYlocal()), float(gcp.getXlocal())] ], axis=0 )
                
            if self.l == None:
                self.l = array( [ [float(gcp.getXglobal())], [float(gcp.getYglobal())] ] )
            else:
                self.l = append(self.l, [[float(gcp.getXglobal())]],  axis=0)
                self.l = append(self.l, [[float(gcp.getYglobal())]],  axis=0)
        
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
        
        print "Massstab: " + str(self.calcScale)
        print "Rotation: " + str(self.calcRotation)
        
        # 4-Parameter-Loesung, fertig.
        if self.calcScale == True and self.calcRotation == True:
            print  [a, b, c, d]
            return [a, b, c, d, None, None]
            
        # 2-Parameter-Loesung, nur Translation.
        if self.calcScale == False and self.calcRotation == False:
            for i in range(0, 1000):
                print i
                
                self.A = None
                self.l = None
                
                for gcp in self.gcps:  
                    if gcp.isChecked() == False:
                        continue
                        
                    if self.A == None:
                        self.A = array( [ [1,  0] ] )
                        self.A = append(self.A, [ [0,  1] ], axis=0 )
                    else:
                        self.A = append(self.A, [ [1,  0] ], axis=0 )
                        self.A = append(self.A, [ [0,  1] ], axis=0 )

                    # f(tx0,ty0)
                    f0_x = self.tx_tmp + 1*math.cos(0)*float(gcp.getXlocal()) - 1*math.sin(0)*float(gcp.getYlocal())
                    f0_y = self.ty_tmp + 1*math.sin(0)*float(gcp.getXlocal()) + 1*math.cos(0)*float(gcp.getYlocal())

                    if self.l == None:
                        self.l = array( [ [float(gcp.getXglobal()) - f0_x],  [float(gcp.getYglobal()) - f0_y] ] )
                    else:
                        self.l = append(self.l,  [[float(gcp.getXglobal()) - f0_x]],  axis=0)
                        self.l = append(self.l,  [[float(gcp.getYglobal()) - f0_y]],  axis=0)

                self.x = dot( dot( linalg.inv( dot( transpose(self.A),  self.A)),  transpose(self.A) ),  self.l)
                self.v = dot( self.A,  self.x ) - self.l

                self.tx_diff = self.x[0][0]
                self.ty_diff = self.x[1][0]

                self.tx_tmp = self.tx_tmp + self.x[0][0]
                self.ty_tmp = self.ty_tmp + self.x[1][0]

                if math.fabs(self.tx_diff) < 0.0001 and math.fabs(self.ty_diff) < 0.0001:
                    a = self.tx_tmp
                    b = self.ty_tmp
                    c = 1
                    d = 0
                    print  [a, b, c, d]
                    return [a, b, c, d, None, None]
            
        # 3-Parameter-Loesung, Rotation wird nicht geschaetzt.
        if self.calcScale == True and self.calcRotation == False:
            for i in range(0, 1000):
                print i
                
                self.A = None
                self.l = None
                
                for gcp in self.gcps:  
                    if gcp.isChecked() == False:
                        continue

                    if self.A == None:
                        self.A = array( [ [1,  0, math.cos(0)*float(gcp.getXlocal()) - math.sin(0)*float(gcp.getYlocal())] ] )
                        self.A = append(self.A, [ [0,  1, math.sin(0)*float(gcp.getXlocal()) - math.cos(0)*float(gcp.getYlocal())] ], axis=0 )
                    else:
                        self.A = append(self.A, [ [1,  0,  math.cos(0)*float(gcp.getXlocal()) - math.sin(0)*float(gcp.getYlocal())] ], axis=0 )
                        self.A = append(self.A, [ [0,  1,  math.sin(0)*float(gcp.getXlocal()) - math.cos(0)*float(gcp.getYlocal())] ], axis=0 )

                    # f(tx0,ty0,scale0)
                    f0_x = self.tx_tmp + self.scale_tmp*math.cos(0)*float(gcp.getXlocal()) - self.scale_tmp*math.sin(0)*float(gcp.getYlocal())
                    f0_y = self.ty_tmp + self.scale_tmp*math.sin(0)*float(gcp.getXlocal()) + self.scale_tmp*math.cos(0)*float(gcp.getYlocal())

                    if self.l == None:
                        self.l = array( [ [float(gcp.getXglobal()) - f0_x],  [float(gcp.getYglobal()) - f0_y] ] )
                    else:
                        self.l = append(self.l,  [[float(gcp.getXglobal()) - f0_x]],  axis=0)
                        self.l = append(self.l,  [[float(gcp.getYglobal()) - f0_y]],  axis=0)

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
        if self.calcScale == False and self.calcRotation == True:
            for i in range(0, 1000):
                print i
                
                self.A = None
                self.l = None
                
                for gcp in self.gcps:  
                    if gcp.isChecked() == False:
                        continue

                    if self.A == None:
                        self.A = array( [ [1,  0,  -1*float(gcp.getXlocal())*math.sin(self.alpha_tmp) - 1*float(gcp.getYlocal())*math.cos(self.alpha_tmp)] ] )
                        self.A = append(self.A, [ [0,  1,  float(gcp.getXlocal())*math.cos(self.alpha_tmp) - 1*float(gcp.getYlocal())*math.sin(self.alpha_tmp)] ], axis=0 )
                    else:
                        self.A = append(self.A, [ [1,  0,  -1*float(gcp.getXlocal())*math.sin(self.alpha_tmp) - 1*float(gcp.getYlocal())*math.cos(self.alpha_tmp)] ], axis=0 )
                        self.A = append(self.A, [ [0,  1,  float(gcp.getXlocal())*math.cos(self.alpha_tmp) - 1*float(gcp.getYlocal())*math.sin(self.alpha_tmp)] ], axis=0 )

                    # f(tx0,ty0,alpha0)
                    f0_x = self.tx_tmp + math.cos(self.alpha_tmp)*float(gcp.getXlocal()) - math.sin(self.alpha_tmp)*float(gcp.getYlocal())
                    f0_y = self.ty_tmp + math.sin(self.alpha_tmp)*float(gcp.getXlocal()) + math.cos(self.alpha_tmp)*float(gcp.getYlocal())
          
                    if self.l == None:
                        self.l = array( [ [float(gcp.getXglobal()) - f0_x],  [float(gcp.getYglobal()) - f0_y] ] )
                    else:
                        self.l = append(self.l,  [[float(gcp.getXglobal()) - f0_x]],  axis=0)
                        self.l = append(self.l,  [[float(gcp.getYglobal()) - f0_y]],  axis=0)

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

