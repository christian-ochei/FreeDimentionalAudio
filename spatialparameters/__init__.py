from . import parameters
import numpy as np

# TODO: Incomplete

class _SpatialParameters:
    def __init__(self,speed_of_sound=parameters.inverse_speed_of_sound):
        ...
    def _meters_to_M(self):
        """
        :return: M is equivalent to meters in view coordinates
        """
        ...

    def _delay_time_for(self,distance):
        return distance * parameters.inverse_speed_of_sound


    # Attenuation and transfer functions
    def _atmospheric_attenuation_for(self,distances):
        return 6 * np.tile(np.sqrt(distances)[...,None],(1,200))

    def _wall_attenuation_for(self,order):
        return np.zeros(200)


