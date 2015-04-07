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
# File: datatable.py
#
# Author: Gina Sprint
#
#############################################################################
# Summary: Data object of the app. Stores the data and associated operations.
#
#############################################################################

import qtall as qt4

#*************************************DataTableModel*************************************  
class DataTableModel(qt4.QAbstractTableModel):
    '''

    '''    

    #*************************************__init__()*************************************  
    def __init__(self, parent, mod):
        '''

        Args:
        Returns: 
        Raises:
        '''    
        qt4.QAbstractTableModel.__init__(self, parent)

        self.model = mod
        self.connect(self.model, qt4.SIGNAL('sigModified'), self.slotModelModified)

    #*************************************rowCount()*************************************  
    def rowCount(self, parent):
        '''

        Args:
        Returns: 
        Raises:
        '''    
        try:
            ds = self.model.get_horiz_headers()
            ds = len(ds)
        except (KeyError, AttributeError):
            return 0
        return ds
        
    #*************************************slotModelModified()*************************************  
    def slotModelModified(self):
        '''

        Args:
        Returns: 
        Raises:
        '''    
        self.emit(qt4.SIGNAL('layoutChanged()'))

    #*************************************columnCount()*************************************  
    def columnCount(self, parent):
        '''

        Args:
        Returns: 
        Raises:
        '''    
        try:
            ds = self.model.get_vert_headers()
            ds = len(ds)
        except KeyError:
            return 0
        return ds

    #*************************************data()*************************************  
    def data(self, index, role):
        '''

        Args:
        Returns: 
        Raises:
        '''    
        # get dataset
        ds = self.model.get_result_at(index.row(), index.column())
        if ds is not None and role == qt4.Qt.DisplayRole:
            try:
                # convert data to QVariant
                return qt4.QVariant(float(ds))
            except IndexError:
                return qt4.QVariant()

        if role == qt4.Qt.ToolTipRole:
            tooltip = self.model.get_description_at(index.row(), index.column())
            return qt4.QVariant(tooltip)
        # empty entry
        return qt4.QVariant()
    
    #*************************************headerData()*************************************  
    def headerData(self, section, orientation, role):
        '''

        Args:
        Returns: 
        Raises:
        '''    

        try:
            cols = self.model.get_vert_headers()
            rows = self.model.get_horiz_headers()
        except KeyError:
            return qt4.QVariant()

        #self.emit(qt4.SIGNAL('header'))
        if role == qt4.Qt.DisplayRole:
            if orientation == qt4.Qt.Horizontal:
                # column names
                if len(cols) > 0:
                    return qt4.QVariant(cols[section])
            else:
                # return row numbers
                if len(rows) > 0:
                    return qt4.QVariant(rows[section])

        return qt4.QVariant()
        
    #*************************************flags()*************************************  
    def flags(self, index):
        '''

        Args:
        Returns: 
        Raises:
        '''    
        
        if not index.isValid():
            return qt4.Qt.ItemIsEnabled
        else:
            return qt4.QAbstractTableModel.flags(self, index)# | qt4.Qt.ItemIsEditable

    #*************************************removeRows()*************************************  
    def removeRows(self, row, count):
        '''

        Args:
        Returns: 
        Raises:
        '''    
        return False

    #*************************************insertRows()*************************************  
    def insertRows(self, row, count):
        '''

        Args:
        Returns: 
        Raises:
        '''    
        return False

    #*************************************setData()*************************************  
    def setData(self, index, value, role):
        '''

        Args:
        Returns: 
        Raises:
        '''    

        return False
 

            