'''
Copyright (C) 2015 Gina L. Sprint
Email: Gina Sprint <gsprint@eecs.wsu.edu>

This file is part of sensor_metric_explorer.

sensor_sensor_metric_explorer is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

sensor_sensor_metric_explorer is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with sensor_data_preprocessing.  If not, see <http://www.gnu.org/licenses/>.

Created on Apr 2, 2015

This code is a prototype for a user interface to explore metrics derived from 
inertial sensors. This code can be tricky to run based on the compatibility
between PyQt4 and Enthought Chaco (plotting library). I recommend using
Python 2.6 (EPD 6.3-2) and PyQt4.9.


@author: Gina Sprint
'''

#############################################################################
# Project: sensor_metric_explorer
#
# File: model.py
#
# Author: Gina Sprint
#
#############################################################################
# Summary: Holds the data and updates the GUI
#
#############################################################################

import sys
                                 
# Relative imports
from ui import MainWindow

from plots import Plots
from circuit_profile import CircuitProfile
from operations import Operations
import qtall as qt4

        
#*************************************Model*************************************      
class Model(qt4.QObject):
    '''
    
    Main work horse. Model of the data.
    '''  
    
    #*************************************__init__()************************************* 
    def __init__(self):
        '''
        Constructor
        '''
        qt4.QObject.__init__( self )
                
        self.view_mode = "R"        
        
        self.cp1 = CircuitProfile(None)
        self.cp2 = CircuitProfile(None)
        self.cpgoal = CircuitProfile(None)
        
        self.ops = {}
        self.results = {"S1": {}, "S2": {}, "Change": {}, "Goal": {}}
        
        self.load_operations()
        # create the GUI app
        self.app = qt4.QApplication.instance()
        self.app.processEvents()
        # instantiate the main window
        self.ui = MainWindow(self)
        self.plots_S1 = Plots(self, self.ui, "S1", self.ui.mplS1)
        self.plots_S2 = Plots(self, self.ui, "S2", self.ui.mplS2)
        self.plots_S2.hide()
        # full screen
        self.ui.showMaximized()
        # start the Qt main loop execution, exiting from this script
        # with the same return code of Qt application
        sys.exit(self.app.exec_())
        
        self.log_file = open("log_file.txt", "w")

    #*************************************load_circuit_profile()************************************* 
    def load_circuit_profile(self, identifier, fname):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        if identifier == "S1":
            cp = self.cp1
        elif identifier == "S2":
            cp = self.cp2
            self.plots_S2.unhide()
            if len(cp.results) == 0:
                self.plots_S1.hide()
        elif identifier == "Goal":
            cp = self.cpgoal
        else:
            print "Unknown circuit profile identifier"
            sys.exit()
        
        cp.open_file(fname)
        results = self.compute_operations(cp)
        cp.set_results(results)
        self.results[identifier] = results
        
        if identifier == "S1":
            self.plots_S1.update_plots(cp)
        elif identifier == "S2":
            self.plots_S2.update_plots(cp)
                    
        self.check_change()
        self.emit(qt4.SIGNAL("sigModified"))
        
        
    #***************************check_change()***************************
    def check_change(self):
        '''
        
        Args: 
        Returns:
        Raises:
        '''
        rS1 = self.results["S1"]
        rS2 = self.results["S2"]
        
        if len(rS1) > 0 and len(rS2) > 0:
            self.results["Change"] = self.cp2 - self.cp1
            self.plots_S1.unhide()
            self.plots_S2.unhide()
        
    #***************************load_operations()***************************
    def load_operations(self):
        '''
        
        Args: 
        Returns:
        Raises:
        '''
        self.ops = Operations(self)
        self.vert_headers = ["S1", "S2", "Change", "Goal"]
        self.horiz_headers = self.ops.get_ops("table").keys()
        self.horiz_headers.sort()
        
    #***************************compute_operations()***************************
    def compute_operations(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        return self.ops.compute(cp)
    
    #***************************change_view()***************************
    def change_view(self, view):
        '''
        
        Args: 
        Returns:
        Raises:
        '''
        self.view_mode = view
        
        temp = []
        temp_plots = []

        if self.view_mode == "R":
            temp = self.ops.get_ops("table").keys()
            temp_plots = self.ops.get_ops("plot").keys()
        
        if self.view_mode == "T":
            for opname, op in self.ops.get_ops("table").items():
                if op.therapist is True or op.patient is True:
                    temp.append(opname)
            
            for opname, op in self.ops.get_ops("plot").items():
                if op.therapist is True or op.patient is True:
                    temp_plots.append(opname)
        
        if self.view_mode == "P":
            for opname, op in self.ops.get_ops("table").items():
                if op.patient is True:
                    temp.append(opname)
                    
            for opname, op in self.ops.get_ops("plot").items():
                if op.patient is True:
                    temp_plots.append(opname)
                    
        self.plots_S1.change_view(temp_plots)
        self.plots_S2.change_view(temp_plots)
        
        temp.sort()
        self.horiz_headers = temp
            
        self.emit(qt4.SIGNAL("sigModified"))
        
    #***************************get_result_at()***************************
    def get_result_at(self, row, col):
        '''
        
        Args: 
        Returns:
        Raises:
        '''
        cpname = self.vert_headers[col]
        cp_results = self.results[cpname]
        
        if len(cp_results) == 0:
            return None
        
        opname = self.horiz_headers[row]
        
        if self.view_mode == "R":
            return cp_results[opname]
        
        if self.view_mode == "T":
            op = self.ops.ops[opname]
            if op.therapist is True or op.patient is True:
                return cp_results[opname]
        
        if self.view_mode == "P":
            op = self.ops.ops[opname]
            if op.patient is True:
                return cp_results[opname]
            
    #***************************get_description_at()***************************
    def get_description_at(self, row, col):
        '''
        
        Args: 
        Returns:
        Raises:
        '''
        cpname = self.vert_headers[col]
        opname = self.horiz_headers[row]
        
        return self.ops.get_description(opname)

    #***************************get_vert_headers()***************************
    def get_vert_headers(self):
        '''
        
        Args: 
        Returns:
        Raises:
        '''
        return self.vert_headers
        
    #***************************get_horiz_headers()***************************
    def get_horiz_headers(self):
        '''
        
        Args: 
        Returns:
        Raises:
        '''
        return self.horiz_headers
        