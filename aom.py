from UnitConversionBase import *
from numpy import *

class SineAom(UnitConversion):
    """
    AOM calibration P(A) is very close to a sine for dipole trap AOM!
    """
    base_unit = "Arb"
    derived_units = ["Power", "fraction"]

    def __init__(self, calibration_parameters=None):
        # These parameters are loaded from a globals.h5 type file automatically
        self.parameters = calibration_parameters
        
        # P(x) = A * cos(2*pi*f * x + phase) + c
        # Saturates at saturation Volts
        self.parameters.setdefault('A', 1.969)
        self.parameters.setdefault('f', 0.527)
        self.parameters.setdefault('phase', 3.262)
        self.parameters.setdefault('c', 1.901)
        
        UnitConversion.__init__(self,self.parameters)

    def Power_to_base(self, power):
        A = self.parameters["A"]
        f = self.parameters["f"]
        phase = self.parameters["phase"]
        c = self.parameters["c"]
        phi = arccos((power - c) / A) - phase
        if phi <0:
            phi += 2*pi
        elif phi > 2*pi:
            phi -= 2*pi
        return phi / (2*pi*f)
    
    def Power_from_base(self, amp):
        A = self.parameters["A"]
        f = self.parameters["f"]
        phase = self.parameters["phase"]
        c = self.parameters["c"]

        return A * cos(2*pi*f*amp + phase) + c        

    def fraction_to_base(self, fraction):
        Pmax = self.parameters["A"] + self.parameters["c"]
        Pmin = max(self.parameters["c"] - self.parameters["A"], 0)
        P = (Pmax - Pmin) * fraction + Pmin
        Amp = self.Power_to_base(P)
        print "AOM amplitude", Amp
        return Amp
    
    def fraction_from_base(self, amp):
        P = self.Power_from_base(amp)
        Pmax = self.parameters["A"] + self.parameters["c"]
        Pmin = max(self.parameters["c"] - self.parameters["A"], 0)
        fraction = (P - Pmin) / (Pmax - Pmin)
        return fraction

