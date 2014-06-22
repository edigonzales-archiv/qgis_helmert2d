# -*- coding: utf-8 -*-

class Point():
    def __init__(self, id):
        self.id = id
        self.x_global = None
        self.y_global = None
        self.x_local = None
        self.y_local = None
        self.x_trans = None
        self.y_trans = None 
        self.x_inter = None
        self.y_inter = None
        self.checked = None
        
    def set_x_global(self, x):
        self.x_global = x
        
    def set_y_global(self, y):
        self.y_global = y        
        
    def set_x_local(self, x):
        self.x_local = x        
        
    def set_y_local(self, y):
        self.y_local = y             
        
    def set_x_trans(self, x):
        self.x_trans = x        
        
    def set_y_trans(self, y):
        self.y_trans = y         
       
    def set_x_Inter(self, x):
        self.x_inter = x
        
    def set_y_Inter(self, y):
        self.y_inter = y
        
    def set_checked(self, flag):
        self.checked = flag
        
    def get_ident(self):
        return self.id        
        
    def get_x_global(self):
        return self.x_global
        
    def get_y_global(self):
        return self.y_global        
        
    def get_x_local(self):
        return self.x_local

    def get_y_local(self):
        return self.y_local
        
    def get_x_trans(self):
        return self.x_trans

    def get_y_trans(self):
        return self.y_trans
        
    def get_x_inter(self):
        return self.x_inter
        
    def get_y_inter(self):
        return self.y_inter
        
    def is_checked(self):
        return self.checked
