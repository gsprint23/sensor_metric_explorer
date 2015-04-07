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
# File: signal.py
#
# Author: Gina Sprint
#
#############################################################################
# Summary: Represents the signal for each axis of the sensors.
#
#############################################################################

import qtall as qt4
import pandas as pd
import datetime
import csv


#*************************************Signal*************************************
class Signal(qt4.QObject):
    '''
    
    '''


    #*************************************__init__()*************************************
    def __init__(self, model, fname=None):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        qt4.QObject.__init__(self)
        
        # Using a dictionary for time series lookup
        self.data_dict = {}
        self.features = {}
    
        # model member set when this dataset is set in model
        self.model = model


    #*************************************description()*************************************
    def description(self):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return ""
    
    #*************************************set_features()*************************************
    def set_features(self, results):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        self.features = results
        