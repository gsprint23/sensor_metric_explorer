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


@author: Adapted from: https://github.com/enthought/chaco/blob/master/examples/demo/zoomed_plot/zoom_overlay.py
'''

#############################################################################
# Project: sensor_metric_explorer
#
# File: zoom_overlay.py
#
# Author: Adapted from: https://github.com/enthought/chaco/blob/master/examples/demo/zoomed_plot/zoom_overlay.py
#
#############################################################################
# Summary: The polygon overlay mapping timeline to bottom plot axis
#
#############################################################################

from __future__ import with_statement

from numpy import array, amax, amin

from enthought.enable.api import ColorTrait, Component
from enthought.traits.api import Float, Instance, Int
from enthought.chaco.api import AbstractOverlay, BaseXYPlot
from enthought.traits.ui.api import Item, View, Group

#*************************************ZoomOverlay*************************************  
class ZoomOverlay(AbstractOverlay):
    '''
    
    Adapted from a Chaco example.
    '''  
    
    source = Instance(BaseXYPlot)
    destination = Instance(Component)
    
    border_color = ColorTrait((0, 0, 0.7, 1))
    border_width = Int(1)
    fill_color = ColorTrait("lightblue")
    alpha = Float(0.3)
    
    traits_view = View(
    Group(Item('fill_color', label="Color", style="simple"),
        Item('border_width', label="Border Width", style="custom"),
        Item('border_color', label="Border Color"),
        orientation = "vertical"),
            width=500, height=300, resizable=True,
            title="Configure Settings",
            buttons = ['OK', 'Cancel']
            )
    
    #*************************************calculate_points()*************************************  
    def calculate_points(self, component):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        # find selection range on source plot
        x_start, x_end = self._get_selection_screencoords()
        if x_start > x_end:
            x_start, x_end = x_end, x_start
        
        y_end = self.source.y
        y_start = self.source.y2
        
        left_top = array([x_start, y_end])
        left_mid = array([x_start, y_start])
        right_top = array([x_end, y_end])
        right_mid = array([x_end, y_start])
        
        # Offset y because we want to avoid overlapping the trapezoid with the topmost
        # pixels of the destination plot.
        #y = self.destination.y + 1
        y = 100
        
        left_end = array([self.destination.x, y])
        right_end = array([self.source.x2, y])

        polygon = array((left_top, left_mid, left_end, 
                         right_end,right_mid, right_top))
        left_line = array((left_top, left_mid, left_end))
        right_line = array((right_end,right_mid, right_top))
        
        return left_line, right_line, polygon
    
    #*************************************overlay()*************************************  
    def overlay(self, component, gc, view_bounds=None, mode="normal"):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  

        tmp = self._get_selection_screencoords()
        if tmp is None:
            return
        
        left_line, right_line, polygon = self.calculate_points(component)
       
        with gc:
            gc.translate_ctm(*component.position)
            gc.set_alpha(self.alpha)
            gc.set_fill_color(self.fill_color_)
            gc.set_line_width(self.border_width)
            gc.set_stroke_color(self.border_color_)
            gc.begin_path()
            gc.lines(polygon)
            gc.fill_path()
            
            gc.begin_path()
            gc.lines(left_line)
            gc.lines(right_line)
            gc.stroke_path()

        return
    
    #*************************************_get_selection_screencords()*************************************  
    def _get_selection_screencoords(self):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        selection = self.source.index.metadata["selections"]
        if selection is not None and len(selection) == 2:
            mapper = self.source.index_mapper
            return mapper.map_screen(array(selection))
        else:
            return None
    
    #*************************************_source_changed()*************************************  
    def _source_changed(self, old, new):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        if old is not None and old.controller is not None:
            old.controller.on_trait_change(self._selection_update_handler, "selection",
                                           remove=True)
        if new is not None and new.controller is not None:
            new.controller.on_trait_change(self._selection_update_handler, "selection")
        return
    
    #*************************************_selection_update_handler()*************************************  
    def _selection_update_handler(self, value):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        if value is not None and self.destination is not None:
            r = self.destination.index_mapper.range
            start, end = amin(value), amax(value)
            r.low = start
            r.high = end
        
        self.source.request_redraw()
        self.destination.request_redraw()
        return
