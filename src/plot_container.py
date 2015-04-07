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
# File: plot_container.py
#
# Author: Gina Sprint
#
#############################################################################
# Summary: Wrapper class for Chaco Plot objects.
#
#############################################################################

from enthought.traits.api import HasTraits, Instance           
from enthought.chaco.api import Plot, ArrayPlotData
from enthought.chaco.tools.api import PanTool, ZoomTool, LegendHighlighter, DragZoom

#*************************************MyLegendHighlighter************************************* 
class MyLegendHighlighter(LegendHighlighter):
    '''
    
    Adapted from a Chaco example.
    '''  
    #*************************************is_draggable()************************************* 
    def is_draggable(self, x, y):
        '''
        Returns whether the (x,y) position is in a region that is OK to
        drag.

        Overrides DragTool.
        '''
        if self.component:
            legend = self.component
            #print x, y
            #print legend.x, legend.x2 ,legend.y, legend.y2
            return (x >= legend.x and x <= legend.x2 and \
                    y >= legend.y and y <= legend.y2)
        else:
            return False    
        
    #*************************************drag_start()************************************* 
    def drag_start(self, event):
        '''
        Called when the drag operation starts.
        Implements DragTool.
        
        Args: 
        Returns:
        Raises:
        '''  
        if self.component:
            self.original_padding = self.component.padding
            event.window.set_mouse_owner(self, event.net_transform())
            event.handled = True
        return

    #*************************************dragging()************************************* 
    def dragging(self, event):
        '''
        This method is called for every mouse_move event that the tool
        receives while the user is dragging the mouse.
        Implements DragTool. Moves the legend by aligning it to a corner of its
        overlay component.
        
        Args: 
        Returns:
        Raises:
        '''  
        # To properly move a legend (which aligns itself to a corner of its overlay
        # component), we need to modify the padding amounts as opposed to modifying
        # the position directly.
        if self.component:
            legend = self.component
            valign, halign = legend.align
            left, right, top, bottom = self.original_padding

            dy = int(event.y - self.mouse_down_position[1])
            if valign == "u":
                # we subtract dy because if the mouse moves downwards, dy is
                # negative but the top padding has increased
                legend.padding_top = top - dy
            else:
                legend.padding_bottom = bottom + dy

            dx = int(event.x - self.mouse_down_position[0])
            if halign == "r":
                legend.padding_right = right - dx
            else:
                legend.padding_left = left + dx

            event.handled = True
            legend.request_redraw()
        return

    #*************************************drag_end()************************************* 
    def drag_end(self, event):
        '''
        Called when a mouse event causes the drag operation to end.
        Implements DragTool.
        
        Args: 
        Returns:
        Raises:
        '''  
        # Make sure we have both a legend and that the legend is overlaying
        # a component
        if self.auto_align and self.component and self.component.component:
            # Determine which boundaries of the legend's overlaid component are
            # closest to the center of the legend
            legend = self.component
            component = legend.component

            left = int(legend.x - component.x)
            right = int(component.x2 - legend.x2)
            #print "legend.x %d component.x %d legend.x2 %d component.x2 %d" %(legend.x, legend.x2, component.x, component.x2)
            if left < right:
                halign = "l"
                legend.padding_left = left
            else:
                halign = "r"
                legend.padding_right = right

            bottom = int(legend.y - component.y)
            top = int(component.y2 - legend.y2)
            if bottom < top:
                valign = "l"
                legend.padding_bottom = bottom
            else:
                valign = "u"
                legend.padding_top = top

            legend.align = valign + halign
            if event.window.mouse_owner == self:
                event.window.set_mouse_owner(None)
            event.handled = True
            legend.request_redraw()
        return

#*************************************PlotContainer*************************************     
class PlotContainer(HasTraits):
    '''
    
    PlotContainer class
    '''
    plot_data = Instance(ArrayPlotData)
    plot_conactory = Instance(Plot)
    
    #*************************************__init__()*************************************     
    def __init__(self, name, model, time_src):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        self.name = name
        self.metrics = []
        self.model = model
        self.plot_data = ArrayPlotData(index = time_src)
        self.plot_conactory = Plot(self.plot_data)#spacing=20, padding = 20, border_visible=False)
        self.plot_conactory.padding_bg_color = "white" 
        self.plot_conactory.bgcolor = "white" 
        self.plot_conactory.padding_left = 50
        self.plot_conactory.padding_bottom = 17
        self.plot_conactory.padding_right = 20
        self.plot_conactory.padding_top = 2

        self.saved_index_range = self.plot_conactory.index_range
        self.plot_conactory.legend.visible = True
        self.plot_conactory.legend.align = "ll"
        self.x_axis = self.plot_conactory.x_axis
        self.y_axis = self.plot_conactory.y_axis
        self.plot_conactory.legend.tools.append(MyLegendHighlighter(self.plot_conactory.legend, drag_button="left", 
            modifier="shift"))

        self.pan_tool = PanTool(self.plot_conactory, constrain=True,
                                        constrain_direction="x")
        self.plot_conactory.tools.append(self.pan_tool)
        self.zoom_tool = ZoomTool(self.plot_conactory, drag_button="right",
                                              always_on=True,
                                              always_on_modifier="shift",
                                              tool_mode="range",
                                              axis="index",
                                              max_zoom_out_factor=1.0,
                                             )
        self.plot_conactory.tools.append(self.zoom_tool)
        self.drag_zoom_tool = DragZoom(self.plot_conactory, drag_button="right")
        self.plot_conactory.tools.append(self.drag_zoom_tool)



        