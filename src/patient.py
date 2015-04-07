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
# File: patient.py
#
# Author: Gina Sprint
#
#############################################################################
# Summary: Represents the patient information.
#
#############################################################################

import qtall as qt4

#*************************************Patient*************************************
class Patient(qt4.QObject):
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
        
        # Attributes of patient
        self.id = None
        self.sex = None
        self.height = None
        self.weight = None
        self.fim = None
        self.mini_cog = None
        
        self.date_admitted = None
        self.discharge_date = None
        
        self.injuries = None
        self.rehab = None
        self.sessions_per_week = None
        self.mins_per_session = None
        self.community_modules_used = None
        self.community_sessions_per_week = None
        self.community_mins_per_session = None
        self.history = None
        
        self.lower_leg_length = None
        self.upper_leg_length = None
        self.torso_length = None
    
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
       