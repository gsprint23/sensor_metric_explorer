sensor_metric_explorer
==========================

sensor_data_preprocessing is a code base used to orient and filter Shimmer sensors  &lt;http://www.shimmersensing.com/>. The code also trims the data files down to the sections of interest. This code is highly specific to 

sensor_metric_explorer 1.0.0
------------
https://github.com/gsprint23

sensor_metric_explorer is Copyright (C) 2015 Gina L. Sprint
Email: Gina Sprint <gsprint@eecs.wsu.edu>

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

This code is a prototype for a user interface to explore metrics derived from 
inertial sensors. This code can be tricky to run based on the compatibility
between PyQt4 and Enthought Chaco (plotting library). I recommend using
Python 2.6 (EPD 6.3-2) and PyQt4.9.

Dependencies
-PyQt4
-Enthought Chaco
-Pandas
-Numpy/Scipy
