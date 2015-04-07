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


# Chaco imports
from enthought.chaco.api import ArrayDataSource, DataRange1D, BarPlot, ScatterPlot, LinePlot, LinearMapper, VPlotContainer
from enthought.chaco.tools.api import RangeSelection, RangeSelectionOverlay
from enthought.chaco.scales_tick_generator import ScalesTickGenerator
#from enthought.chaco.scales_axis import PlotAxis
from enthought.chaco.api import LabelAxis
from enthought.enable.component_editor import ComponentEditor
from enthought.traits.ui.api import Item, View
from enthought.traits.api import HasTraits, Instance
                                 
# Relative imports
from zoom_overlay import ZoomOverlay
from plot_container import PlotContainer


        
#*************************************Plots*************************************      
class Plots(HasTraits):
    '''
    
    Main work horse. Model of the data.
    '''  

    container = Instance(VPlotContainer)
    
    container_view = View(Item('container', editor=ComponentEditor(), show_label=False, width = 1000, height = 400), 
                   width = 1000, height = 400, resizable=True)
    
    #*************************************__init__()************************************* 
    def __init__(self, model, ui, extension, parent):
        '''
        Constructor
        '''
        self.model = model
        self.ui = ui
        self.extension = extension
        self.parent = parent
        
        self.plots = {}
        self.renderers = {}
        
        self.hidden = False
        self.time_src = ArrayDataSource([])
        self.container = VPlotContainer(bgcolor = "white",
            fill_padding=True,
            border_visible=False,
            stack_order = 'top_to_bottom')  
        self.setup_plots()
        self.pc = self.edit_traits(view='container_view', parent=parent, kind='subpanel').control
        parent.layout.addWidget(self.pc)
        self.pc.setParent(parent)
    
    #*************************************update_plots()************************************* 
    def update_plots(self, pc):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        ann = pc.data_dict["annotations"]
        t0 = ann.get_value("START")
        t1 = ann.get_value("STOP")
        tug = ann.get_value("TURN_AROUND")
        delta = t1 - t0
        total = delta.seconds + delta.microseconds * 10**(-6)
        self.time_src.set_data([0, total])

        t2 = tug-t0
        t2 = t2.seconds + t2.microseconds * 10**(-6)


        self.x_axis.labels = ["START", "TURN_AROUND", "5s", "STOP"]
        self.x_axis.positions = [0,
                                 t2,
                                 5,
                                 total]
        
        for name, plot in self.plots.items():
            plot_conactory = plot.plot_conactory
          
            res = pc.results[name[:-3]] # to remove the extension
            print res
            data_src = plot_conactory.datasources.get("index")
            data_src.set_data(res[0])
              
            data_src = plot_conactory.datasources.get(name)
            data_src.set_data(res[1])
            
    #*************************************create_plot()************************************* 
    def create_plot(self, name, ylabel="", color="blue"):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        p = PlotContainer(name, self, self.time_src)
        p.plot_conactory.y_axis.title = ylabel
        self.plots[name] = p
        
        p.plot_data.set_data(name, [])
        renderer, = p.plot_conactory.plot(("index", name), name=name, color=color, line_width=1.5)
        self.renderers[name] = renderer
        
        self.container.add(p.plot_conactory)

    #*************************************setup_plots()************************************* 
    def setup_plots(self):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        ext = self.extension
        
        if ext == "S2":
            color = "green"
        else:
            color = "blue"

        self.create_plot("AAE " + ext, ylabel="[ ]", color=color)
        self.create_plot("ARE " + ext, ylabel="[ ]", color=color)
        self.create_plot("Jerk " + ext, ylabel="[m/s2/s]", color=color)
        self.create_plot("SI " + ext, ylabel="[ ]", color=color)
        self.create_plot("VI " + ext, ylabel="[ ]", color=color)
        
        p = self.plots["VI " + ext]
        
        null_ds = ArrayDataSource([])
        self.time_plot = LinePlot(index = self.time_src, value = null_ds,
                        index_mapper = LinearMapper(range=DataRange1D(self.time_src)),
                        value_mapper = LinearMapper(range=DataRange1D(null_ds)),  
                        color = "black",
                        border_visible = True,
                        bgcolor = "white",
                        height = 10,
                        resizable = "h",
                        padding_top=50,
                        padding_bottom=40,
                        padding_left=50,
                        padding_right=20)
        self.ticker = ScalesTickGenerator()  
        self.x_axis = LabelAxis(self.time_plot, orientation="bottom", title="Time [sec]", label_rotation=0)
        #self.x_axis = PlotAxis(self.time_plot, orientation="bottom", tick_generator = self.ticker, title="Time [sec]")
        self.time_plot.underlays.append(self.x_axis)
        self.container.add(self.time_plot)
        
        # Add a range overlay to the miniplot that is hooked up to the range
        # of the main price_plot
        range_tool = RangeSelection(self.time_plot)
        self.time_plot.tools.append(range_tool)
        range_overlay = RangeSelectionOverlay(self.time_plot, metadata_name="selections")
        self.time_plot.overlays.append(range_overlay)
        range_tool.on_trait_change(self._range_selection_handler, "selection")
        self.range_tool = range_tool

        p.plot_conactory.index_range.on_trait_change(self._plot_range_handler, "updated")
        self.zoom_overlay = ZoomOverlay(source=self.time_plot, destination=p.plot_conactory)
        self.container.overlays.append(self.zoom_overlay)
          
    #*************************************set_inde_range()************************************* 
    def set_index_range(self, low, high):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        iterator = iter(self.renderers.values())
        while True:
            try:
                curr = iterator.next()
                curr.index_range.low = low
                curr.index_range.high = high
            except StopIteration:
                break 
            
    #*************************************set_bounds()************************************* 
    def set_bounds(self, low, high):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        iterator = iter(self.renderers.values())
        while True:
            try:
                curr = iterator.next()
                curr.index_range.set_bounds(low, high)
            except StopIteration:
                break 
       
    #*************************************_range_selection_handler()************************************* 
    def _range_selection_handler(self, event):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        # The event obj should be a tuple (low, high) in data space
        if event is not None:
            low, high = event
            self.set_index_range(low, high)
        else:
            self.set_bounds("auto", "auto")
        
    #*************************************_plot_range_handler()************************************* 
    def _plot_range_handler(self, event):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        if event is not None:
            low, high = event
            if "auto" not in (low, high):
                pass
                '''if low < self.df["Time"][0]:
                    low = self.df["Time"][0]
                if high > self.df["Time"][self.counter-1]:
                    high = self.df["Time"][self.counter-1]
                self.range_tool.selection = (low, high)'''
          
          
    #*************************************change_view()************************************* 
    def change_view(self, plots_to_show):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        temp = list(self.container.components) # to get a copy
        for plot in temp:
            #if type(plot).__name__ == 'Plot':
            self.container.remove(plot)
            
        plots_to_show.sort()
        for plot in plots_to_show:    
            self.container.add(self.plots[plot + " " + self.extension].plot_conactory)
        self.container.add(self.time_plot) # add the time_plot back last so it is on the bottom
        self.container.request_redraw()
                
    #*************************************hide()************************************* 
    def hide(self):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        self.hidden = True
        self.pc.hide()
        
    #*************************************unhide()************************************* 
    def unhide(self):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        self.hidden = False
        self.pc.show()