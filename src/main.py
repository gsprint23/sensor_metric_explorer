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
# File: main.py
#
# Author: Gina Sprint
#
#############################################################################
# Summary: The main entry point to the application. Initializes the model.
#
#############################################################################

import os
#os.environ['QT_API'] = 'pyqt'
os.environ['ETS_TOOLKIT'] = 'qt4'

# relative imports
from model import Model

__version__ = "1.0.0"

#*************************************main()*************************************
if __name__ == '__main__':
    '''
    
    Args: 
    Returns:
    Raises:
    '''  
    
    # initialize the MODEL
    model = Model()

    