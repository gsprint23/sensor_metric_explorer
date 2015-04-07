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
# File: circuit_profile.py
#
# Author: Gina Sprint
#
#############################################################################
# Summary: Data object of the app. Stores the data and associated operations.
#
#############################################################################

import qtall as qt4
import pandas as pd
import datetime
import csv


#*************************************CircuitProfile*************************************
class CircuitProfile(qt4.QObject):
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
        self.results = {}
    
        # model member set when this dataset is set in model
        self.model = model

        if fname is not None:
            self.open_file(fname)

    #*************************************description()*************************************
    def description(self):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return ""
    
    #*************************************set_results()*************************************
    def set_results(self, results):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        self.results = results
        
    #***************************open_file()***************************
    def open_file(self, fname):
        '''
        Opens the file for processing
        '''
        
        # Open, process, close file
        f  = open(fname, "rb")
        reader = csv.reader(f, delimiter=',')
        self.process_file(reader)
        f.close()
        self.fname = fname

    #***************************process_file()***************************
    def process_file(self, handle):
        '''
        Walks through the file and separates the differnt sources
    
        '''
        data = {"annotations": pd.Series(),
                "M054": pd.Series(),
                "M055": pd.Series(),
                "M056": pd.Series(),
                "M057": pd.Series(),
                "M058": pd.Series(),
                "M059": pd.Series(),
                "M060": pd.Series(),
                "x": pd.Series(),
                "y": pd.Series(),        
                "z": pd.Series(),        
                "rx": pd.Series(),
                "ry": pd.Series(),
                "rz": pd.Series()
                }

        for row in handle:
            date = row[0]
            dt = self.get_datetime(date)
            
            src = row[1]
            if src == "system":
                #print "system"
                # annotations is the only one not indexed by datetime!!
                data["annotations"] = data["annotations"].append(pd.Series(dt, index=[row[2]]))
            elif src == "Kyoto":
                #print "Kyoto"
                data["x"] = data["x"].append(pd.Series(row[2], index=[dt]))
                data["y"] = data["y"].append(pd.Series(row[3], index=[dt]))
                data["z"] = data["z"].append(pd.Series(row[4], index=[dt]))
                data["rx"] = data["rx"].append(pd.Series(row[5], index=[dt]))
                data["ry"] = data["ry"].append(pd.Series(row[6], index=[dt]))
                data["rz"] = data["rz"].append(pd.Series(row[7], index=[dt]))
            elif src[:1] == "M":
                #print "Motion"
                data[src] = data[src].append(pd.Series(row[2], index=[dt]))
            else:
                print "Unknown source"
    
        self.data_dict = data

    #***************************get_datetime()***************************
    def get_datetime(self, ts):
        '''
        Returns the datetime given a string formatted such as 2013-03-29 09:58:11.22193
        '''
        
        date = ts.split(' ')
        time = date[1]
        time = time.split(':')
        hour = time[0]
        minute = time[1]
        sec = time[2]
        sec = sec.split('.')
        msec = sec[1]
        sec = sec[0]
        
        date = date[0]
        date = date.split('-')
        year = date[0]
        month = date[1]
        day = date[2]
        
        return datetime.datetime(int(year), int(month),
                               int(day), int(hour), int(minute), int(sec), int(msec))
        
    #*************************************__getitem__()*************************************
    def __getitem__(self, key):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return type(self)(**self._getItemHelper(key))

    #*************************************__len__()*************************************
    def __len__(self):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return len(self.data)
    
    #*************************************__sub__()*************************************
    def __sub__(self,rhs):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        
        # have S2-S1
        results  = {}
        for name,res in self.results.items():
            if type(res) == float:
                results[name] = res - rhs.results[name]
        
        return results

