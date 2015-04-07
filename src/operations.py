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
# File: operations.py
#
# Author: Gina Sprint & Vladimir Borisov
#
#############################################################################
# Summary: Dataset operations to be applied to the circuit profiles.
#
#############################################################################


#*************************************get_subclasses()*************************************
def get_subclasses(c):
    '''
    
    Args: 
    Returns:
    Raises:
    ''' 
    subclasses = c.__subclasses__()
    for d in list(subclasses):
        subclasses.extend(get_subclasses(d))
    return subclasses
    
#*************************************get_first_two_on()*************************************
def get_first_on(ms):
    '''
    
    Args: 
    Returns:
    Raises:
    ''' 
    for dt, val in ms.iterkv():
        if val == "ON":
            return dt
    return None
    
#*************************************Operations*************************************
class Operations(object):
    '''
    
    ''' 
    name = ""
    description = ""
    unit = ""
    display = "table"
    
    #*************************************__init__()*************************************
    def __init__(self, model):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        super(Operations, self).__init__()
        self.ops = {}
        self.model = model
        op_classes = get_subclasses(OperationBase)
        
        # initialize all the operation objects
        for op in op_classes:
            temp = op(self.model)
            self.ops[temp.name] = temp
        
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        results = {}
        for op in self.ops.values():
            results[op.name] = op.compute(cp)
        return results
    
    #*************************************get_ops()*************************************
    def get_ops(self, fliter=None):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        # fliter used to avoid key word filter
        if fliter == None:
            return self.ops
        
        ops = {}
        for name, op in self.ops.items():
            if op.display == fliter:
                ops[name] = op
        return ops
    
    #*************************************get_description()*************************************
    def get_description(self, opname):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return self.ops[opname].description

#*************************************OperationBase*************************************
class OperationBase(object):
    '''
    
    ''' 
    name = ""
    description = ""
    unit = ""
    display = "table"
    therapist = False
    patient = False
    
    #*************************************__init__()*************************************
    def __init__(self, model):
        '''
        data will be a pointer, no copying
        
        Args: 
        Returns:
        Raises:
        ''' 
        self.model = model
        
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0

#*************************************AveragedAccelerationEnergy*************************************
class AverageAccelerationEnergy(OperationBase):
    '''
    
    ''' 
    name = "AAE"
    description = ""
    unit = "%"
    display = "plot"
    patient = True
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return ([0,2,4,6,8,10],[1,2,1,2,1,2])
    
#*************************************AveragedRotationEnergy*************************************
class AverageRotationEnergy(OperationBase):
    '''
    
    ''' 
    name = "ARE"
    description = ""
    unit = "%"
    display = "plot"
    therapist = True
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return ([0,2,4,6,8,10],[1,2,1,2,1,2])
    
#*************************************AverageSittoStandVelocity*************************************
class AverageSittoStandVelocity(OperationBase):
    '''
    
    ''' 
    name = "Average sit-to-stand velocity"
    description = ""
    unit = "deg/sec"
    patient = True
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0
    
#*************************************Cadence*************************************
class Cadence(OperationBase):
    '''
    
    ''' 
    name = "Cadence"
    description = ""
    unit = "strides/min"
    therapist = True
    
  
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0
 
    
#*************************************DoubleSupportDuration*************************************
class DoubleSupportDuration(OperationBase):
    '''
    
    ''' 
    name = "Double support duration"
    description = ""
    unit = "%"
    therapist = True
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0

#*************************************Duration*************************************
class Duration(OperationBase):
    '''
    
    ''' 
    name = "Duration"
    description = ""
    unit = "%"
  
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0
    
#*************************************Eccentricity*************************************
class Eccentricity(OperationBase):
    '''
    
    ''' 
    name = "Eccentricity"
    description = ""
    unit = "%"
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0
       
#*************************************FootSymmetry*************************************
class FootSymmetry(OperationBase):
    '''
    
    ''' 
    name = "Foot symmetry"
    description = ""
    unit = "%"
    patient = True
  
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0

#*************************************IAAtot*************************************
class IAAtot(OperationBase):
    '''
    
    ''' 
    name = "IAAtot"
    description = ""
    unit = "%"
  
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0
    
#*************************************Jerk*************************************
class Jerk(OperationBase):
    '''
    
    ''' 
    name = "Jerk"
    description = ""
    unit = "m/s2/s"
    display = "plot"
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return ([0,2,4,6,8,10],[1,2,1,2,1,2])

#*************************************Kurtosis*************************************
class Kurtosis(OperationBase):
    '''
    
    ''' 
    name = "Kurtosis"
    description = ""
    unit = "%"
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0
    
#*************************************LinearVelocity*************************************
class LinearVelocity(OperationBase):
    '''
    
    ''' 
    name = "Linear velocity"
    description = "The velocity computed using the motion sensors.\
    Computed for 12 feet from the edge of the shag rug to the EXIT sign, where the question is asked"
    unit = "ft/s"
    patient = True
  
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        Using Aaron's specifications:
        The TUG sensors at Kyoto are M054 to M060.
        They all reside in the first floor hallway, and they are ordered low to high, starting from the front door.
        M054 is inside the front door.  It is 18" from the door, and 12" from the wall on your right (towards the kitchen).
        M055 is 24" from M054 and 12" from the wall.
        M056 to M060 follow this pattern, ending just before you enter the living room.
        
        Args: 
        Returns:
        Raises:
        '''
        SENSOR_SPACING_FT = 2
        num_sensors_out = 4
        num_sensors_back = 4
    
        ann = cp.data_dict["annotations"]
        t0 = ann.get_value("START")
        t1 = ann.get_value("STOP")
        ta = ann.get_value("TURN_AROUND")
    
        m56 = cp.data_dict["M056"]
        m56 = m56[t0:ta]
        
        m59 = cp.data_dict["M059"]
        m59 = m59[t0:ta]
        
        m58 = cp.data_dict["M058"]
        m58 = m58[ta:t1]
        
        m55 = cp.data_dict["M055"]
        m55 = m55[ta:t1]

        t0_out = get_first_on(m56)
        t1_out = get_first_on(m59)
        t0_back = get_first_on(m58)
        t1_back = get_first_on(m55)
        
        # Compute time
        delta_t_out = t1_out - t0_out
        delta_t_back = t1_back - t0_back
    
        # Compute distance
        dist_out = SENSOR_SPACING_FT * num_sensors_out
        dist_back = SENSOR_SPACING_FT * num_sensors_back
    
        # Compute velocity = distance / time
        velocity_out = dist_out / (delta_t_out.seconds + delta_t_out.microseconds * 10**(-6))
        velocity_back = dist_back / (delta_t_back.seconds + delta_t_back.microseconds * 10**(-6))
    
        avg = (velocity_out + velocity_back) / 2.0
        return float("%.3f" %avg)
    
    
#*************************************MeanSwayVelocity*************************************
class MeanSwayVelocity(OperationBase):
    '''
    
    ''' 
    name = "Mean sway velocity"
    description = ""
    unit = "%"
    therapist = True
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0

#*************************************MovementIntensityVariation*************************************
class MovementIntensityVariation(OperationBase):
    '''
    
    ''' 
    name = "VI"
    description = ""
    unit = "%"
    display = "plot"
    patient = True
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return ([0,2,4,6,8,10],[1,2,1,2,1,2])
    
#*************************************NormalizedStrideSpeed*************************************
class NormalizedStrideSpeed(OperationBase):
    '''
    
    ''' 
    name = "Normalized stride speed"
    description = ""
    unit = "%"
    patient = True
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0

#*************************************PeakSittoStandVelocity*************************************
class PeakSittoStandVelocity(OperationBase):
    '''
    
    ''' 
    name = "Peak sit-to-stand velocity"
    description = ""
    unit = "deg/sec"
    therapist = True
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0
    
#*************************************RangeOfMotion*************************************
class RangeOfMotion(OperationBase):
    '''
    
    ''' 
    name = "Range of motion"
    description = ""
    unit = "deg"
    patient = True
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0
    
#*************************************RootSumSquares*************************************
class RootSumSquares(OperationBase):
    '''
    
    ''' 
    name = "Root sum of squares"
    description = ""
    unit = "%"
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0
      
#*************************************SingleSupportDuration*************************************
class SingleSupportDuration(OperationBase):
    '''
    
    ''' 
    name = "Single support duration"
    description = ""
    unit = "%"
    therapist = True
  
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0

#*************************************Skewness*************************************
class Skewness(OperationBase):
    '''
    
    ''' 
    name = "Skewness"
    description = ""
    unit = "%"
  
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0
    
#*************************************SmoothnessIntensity*************************************
class SmoothnessIntensity(OperationBase):
    '''
    
    ''' 
    name = "SI"
    description = ""
    unit = "%"
    display = "plot"
    therapist = True
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return ([0,2,4,6,8,10],[1,2,1,2,1,2])

     
#*************************************StanceDuration*************************************
class StanceDuration(OperationBase):
    '''
    
    ''' 
    name = "Stance duration"
    description = ""
    unit = "%"
    therapist = True
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0
    
#*************************************StepDuration*************************************
class StepDuration(OperationBase):
    '''
    
    ''' 
    name = "Step duration"
    description = ""
    unit = "s"
    patient = True
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0
       
#*************************************StepLength*************************************
class StepLength(OperationBase):
    '''
    
    ''' 
    name = "Step length"
    description = ""
    unit = "m"
    patient = True
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0

    
#*************************************StrideDuration*************************************
class StrideDuration(OperationBase):
    '''
    
    ''' 
    name = "Stride duration"
    description = ""
    unit = "%"
    patient = True
  
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0
      
#*************************************StrideLength*************************************
class StrideLength(OperationBase):
    '''
    
    ''' 
    name = "Stride length"
    description = ""
    unit = "m"
    patient = True
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0
    
#*************************************StrideLengthHeight*************************************
class StrideLengthHeight(OperationBase):
    '''
    
    ''' 
    name = "Stride length/height"
    description = ""
    unit = "%"
    therapist = True
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0

#*************************************StrideSpeed*************************************
class StrideSpeed(OperationBase):
    '''
    
    ''' 
    name = "Stride speed"
    description = ""
    unit = "%"
    patient = True
  
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0
    
#*************************************SwayAccelerationAmplitude*************************************
class SwayAccelerationAmplitude(OperationBase):
    '''
    
    ''' 
    name = "Sway Acceleration Amplitude"
    description = ""
    unit = "%"
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0
    
#*************************************SwayFrequency*************************************
class SwayFrequency(OperationBase):
    '''
    
    ''' 
    name = "Sway frequency"
    description = ""
    unit = "%"
    therapist = True
    
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0
    
#*************************************SwayJerk*************************************
class SwayJerk(OperationBase):
    '''
    
    ''' 
    name = "Sway jerk"
    description = ""
    unit = "%"
  
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0

#*************************************SwayJerkNormalized*************************************
class SwayJerkNormalized(OperationBase):
    '''
    
    ''' 
    name = "Sway jerk normalized"
    description = ""
    unit = "%"
    therapist = True
  
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0
     
#*************************************SwingDuration*************************************
class SwingDuration(OperationBase):
    '''
    
    ''' 
    name = "Swing duration"
    description = ""
    unit = "%"
    therapist = True
  
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0

#*************************************TUGDuration*************************************
class TUGDuration(OperationBase):
    '''
    
    ''' 
    name = "TUG duration"
    description = ""
    unit = "s"
    patient = True
  
    #*************************************compute()*************************************
    def compute(self, cp):
        '''
        
        Args: 
        Returns:
        Raises:
        ''' 
        return 0.0
