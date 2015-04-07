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
# File: ui.py
#
# Author: Gina Sprint
#
#############################################################################
# Summary: User interface. Contains the MaindWindow.
#
#############################################################################

# Qt4 bindings for core Qt functionalities (non-GUI)
# Python Qt4 bindings for GUI objects
import qtall as qt4
from plot_widget import PlotWidget
from data_table_model import DataTableModel
  


class DataTableView(qt4.QTableView):  
    '''
    
    '''  
    #*************************************__init__()*************************************
    def __init__(self, parent = None):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        super(DataTableView, self).__init__(parent)

        self.setHorizontalScrollBarPolicy(qt4.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(qt4.Qt.ScrollBarAlwaysOn)

        # To force the width to use sizeHint().width()
        self.setSizePolicy(qt4.QSizePolicy.Fixed, qt4.QSizePolicy.Preferred)

        # To readjust the size automatically...
        # ... when columns are added or resized
        self.horizontalHeader().geometriesChanged \
             .connect(self.updateGeometryAsync)
        self.horizontalHeader().sectionResized \
             .connect(self.updateGeometryAsync)        

    #*************************************setModel()*************************************
    def setModel(self, model):   
        '''
        
        Args: 
        Returns:
        Raises:
        '''     
        super(DataTableView, self).setModel(model)
        # ... when a row header label changes and makes the
        # width of the vertical header change too
        self.model().headerDataChanged.connect(self.updateGeometryAsync)
        
    #*************************************updateGeomteryAsync()*************************************
    def updateGeometryAsync(self):   
        '''
        
        Args: 
        Returns:
        Raises:
        '''     
        #self.resizeColumnsToContents()
        qt4.QTimer.singleShot(0, self.updateGeometry)

    #*************************************sizeHint()*************************************
    def sizeHint(self):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        height = super(DataTableView, self).sizeHint().height()

        # length() includes the width of all its sections
        width = self.horizontalHeader().length() 

        # you add the actual size of the vertical header and scrollbar
        # (not the sizeHint which would only be the preferred size)                  
        width += self.verticalHeader().width()        
        width += self.verticalScrollBar().width()       

        # and the margins which include the frameWidth and the extra 
        # margins that would be set via a stylesheet or something else
        margins = self.contentsMargins()
        width += margins.left() + margins.right()
        
        # TODO: Fix this hack, what is up!
        width -= 125

        return qt4.QSize(width, height)

#*************************************MainWindow*************************************     
class MainWindow(qt4.QMainWindow): 
    '''
    
    '''  
    controller = None
    model = None
    
    #*************************************__init__()*************************************
    def __init__(self, model): 
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        # initialize the super class
        super(MainWindow, self).__init__()
        
        self.model = model
        
        self.setWindowTitle("St. Luke's Circuit")
        self.setObjectName("MainWindow")
        self.setWindowIcon(qt4.QIcon(r"resources\bar_icon.png"))
        
        self.menuBar = self.menuBar()
        self.fileMenu = self.menuBar.addMenu("&File")
        self.editMenu = self.menuBar.addMenu("&Edit")
        self.viewMenu = self.menuBar.addMenu("&View")
        self.helpMenu = self.menuBar.addMenu("&Help")
        self.controlToolBar = self.addToolBar("Control")
        self.controlToolBar.setObjectName("ControlToolBar")
        self.statusBar = self.statusBar()
        self.statusBar.showMessage("Ready", 5000) #shown for 5 seconds
        
        self.splitter = qt4.QSplitter(qt4.Qt.Horizontal, self)
        #self.summaryTabLayout.setStretchFactor(self.splitter, 1)    
        
        self.tableView = DataTableView()
        self.tableModel = DataTableModel(self, self.model)
        self.tableView.setModel(self.tableModel)
        self.splitter.addWidget(self.tableView)

        self.plotSplitter = qt4.QSplitter(qt4.Qt.Vertical, self.splitter)
        self.splitter.addWidget(self.plotSplitter)
        
        self.mplS1 = PlotWidget(self.plotSplitter)
        self.mplS1.setObjectName("mplS1")
        self.plotSplitter.addWidget(self.mplS1)
        
        self.mplS2 = PlotWidget(self.plotSplitter)
        self.mplS2.setObjectName("mplS2")
        self.plotSplitter.addWidget(self.mplS2)
        
        self.setCentralWidget(self.splitter)
        
        self.open1Action = self.action_factory(r"resources\fileopen1.png", 
                                                   "&Open", "Open session 1 circuit profile",
                                                   self.open_circuit_profile1_slot,
                                                   self.fileMenu,
                                                   self.controlToolBar)
        
        self.open2Action = self.action_factory(r"resources\fileopen2.png", 
                                                   "&Open", "Open session 2 circuit profile",
                                                   self.open_circuit_profile2_slot,
                                                   self.fileMenu,
                                                   self.controlToolBar)
        
        self.openGoalAction = self.action_factory(r"resources\fileopengoal.png", 
                                                   "&Open", "Open goal circuit profile",
                                                   self.open_goal_slot,
                                                   self.fileMenu,
                                                   self.controlToolBar)
        
        self.saveAction = self.action_factory(r"resources\filesave.png", 
                                                   "&Save", "Save current circuit profile",
                                                   self.save_circuit_profile_slot,
                                                   self.fileMenu,
                                                   self.controlToolBar)
        
        self.saveAsAction = self.action_factory(r"resources\filesaveas.png", 
                                                   "&SaveAs", "SaveAs current circuit profile",
                                                   self.saveas_circuit_profile_slot,
                                                   self.fileMenu,
                                                   self.controlToolBar)
        
        self.patientViewAction = self.action_factory(r"resources\viewmag-.png", 
                                                   "&Patient", "Change view to patient perspective",
                                                   self.patient_view_slot,
                                                   self.viewMenu,
                                                   self.controlToolBar,
                                                   True,
                                                   False)
                
        self.therapistViewAction = self.action_factory(r"resources\viewmag.png", 
                                                   "&Therapist", "Change view to therapist perspective",
                                                   self.therapist_view_slot,
                                                   self.viewMenu,
                                                   self.controlToolBar,
                                                   True,
                                                   False)
        
        self.researcherViewAction = self.action_factory(r"resources\viewmag+.png", 
                                                   "&Researcher", "Change view to researcher perspective",
                                                   self.researcher_view_slot,
                                                   self.viewMenu,
                                                   self.controlToolBar,
                                                   True,
                                                   True)
                
        self.helpAction = self.action_factory(r"resources\help.png", 
                                                   "&Help", "View the help guide",
                                                   self.help_slot,
                                                   self.fileMenu,
                                                   self.controlToolBar)
        
        self.exitAction = self.action_factory(r"resources\exit.png", 
                                                   "&Exit", "Exit the application",
                                                   self.close,
                                                   self.fileMenu,
                                                   self.controlToolBar)

    #*************************************open_helper()************************************* 
    def open_helper(self, identifier):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        fd = qt4.QFileDialog(self, "Browse data file")
        fd.setDirectory(r"C:\Users\Gina\workspace\StLukesCircuit\data")
        fname = fd.getOpenFileName()

        if len(fname) > 0:
            self.model.load_circuit_profile(identifier, fname)
        
    #*************************************open_circuit_profile1_slot()************************************* 
    def open_circuit_profile1_slot(self):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        self.open_helper("S1")
        
    #*************************************open_circuit_profile2_slot()************************************* 
    def open_circuit_profile2_slot(self):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        self.open_helper("S2")
        
    #*************************************open_goal_slot()************************************* 
    def open_goal_slot(self):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        self.open_helper("Goal")
        
    #*************************************save_circuit_profile_slot()************************************* 
    def save_circuit_profile_slot(self):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        pass
    

    #*************************************saveas_circuit_profile_slot()************************************* 
    def saveas_circuit_profile_slot(self):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        pass
        
    #*************************************help_slot()************************************* 
    def help_slot(self):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        pass
       
       
    #*************************************uncheck_views()************************************* 
    def uncheck_views(self):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        self.therapistViewAction.setChecked(False)
        self.patientViewAction.setChecked(False)
        self.researcherViewAction.setChecked(False)
         
    #*************************************therapist_view_slot()************************************* 
    def therapist_view_slot(self):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        self.uncheck_views()
        self.therapistViewAction.setChecked(True)
        self.model.change_view("T")
    
    #*************************************patient_view_slot()************************************* 
    def patient_view_slot(self):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        self.uncheck_views()
        self.patientViewAction.setChecked(True)
        self.model.change_view("P")
    
    #*************************************researcher_view_slot()************************************* 
    def researcher_view_slot(self):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        self.uncheck_views()
        self.researcherViewAction.setChecked(True)
        self.model.change_view("R")

    #*************************************closeEvent()************************************* 
    def closeEvent(self, event):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        quit_msg = "Are you sure you want to exit the program?"
        reply = qt4.QMessageBox.question(self, "Exit", 
                         quit_msg, qt4.QMessageBox.Yes, qt4.QMessageBox.No)
    
        if reply == qt4.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            

    #*************************************action_factory()************************************* 
    def action_factory(self, icon, name, tooltip, slot, menu, toolbar, checkable=False, checked=False):
        '''
        
        Args: 
        Returns:
        Raises:
        '''  
        action = qt4.QAction(qt4.QIcon(icon), name, self)
        action.setToolTip(tooltip)
        action.setStatusTip(tooltip)
        action.setCheckable(checkable)
        action.setChecked(checked)
        qt4.QObject.connect(action, qt4.SIGNAL("triggered()"), slot)
        menu.addAction(action)
        toolbar.addAction(action)
        return action

        
    
            