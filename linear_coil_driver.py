from UnitConversionBase import *
from numpy import int16
class UnidirectionalCoilDriver(UnitConversion):
    base_unit = 'V'
    derived_units = ['A']
    
    def __init__(self, calibration_parameters=None):
        # These parameters are loaded from a globals.h5 type file automatically
        self.parameters = calibration_parameters
        
        # I[A] = slope * V[V] + shift
        # Saturates at saturation Volts
        self.parameters.setdefault('slope', 1) # A/V
        self.parameters.setdefault('shift', 0) # A
        self.parameters.setdefault('saturation', 10) # V
        
        UnitConversion.__init__(self,self.parameters)
        # We should probably also store some hardware limits here, and use them accordingly 
        # (or maybe load them from a globals file, or specify them in the connection table?)

    def A_to_base(self,amps):
        #here is the calibration code that may use self.parameters
        volts = (amps - self.parameters['shift']) / self.parameters['slope']
        return volts * int16(amps>0)
    def A_from_base(self,volts):
        volts = min(volts, self.parameters['saturation'])
        amps = self.parameters['slope'] * volts + self.parameters['shift']
        return amps * int16(amps>0)
