import numpy as np
import spatialparameters
from typing import List


class _SphericalTV:
    def __init__(self,directions,delay,dampness,quality=50):
        ...
        # self._discretized_volume = np.zeros()


def _to_line(ray_locations,ear_location):
    line = np.empty([ray_locations.shape[0],2,3])
    line[:,0] = ear_location
    line[:,1] = ray_locations
    return line

def _distance(x,y=0):
    return np.sqrt(np.square(x-y).sum(-1))

def _normalize(V):
    return V/_distance(V)[...,None]

class _DiscretizedSphericalTV:
    def __init__(self, directions,delay,dampness,quality=50):
        ...


class _CastedRay:
    def __init__(self,rays,ear_location):
        self._rays         = rays
        self._ear_location = ear_location
        ...

class _DensePropagation:
    def __init__(self,_propagation_orders,_L_ear_orders,_R_ear_orders,rays_per_speaker):
        super(_DensePropagation, self).__init__()
        self._propagation_orders = _propagation_orders # List[propagation._PropagatedRays]
        self._L_ear_orders:List[_CastedRay] = _L_ear_orders
        self._R_ear_orders:List[_CastedRay] = _R_ear_orders
        self._dampness_initial = np.zeros([rays_per_speaker, 200])

    def _spherical_map(self,parameters):
        for o,(_L_ear_order,_R_ear_order) in enumerate(zip(self._L_ear_orders,self._R_ear_orders)):
            _L_ear = self._map_ear(_L_ear_order,parameters,o)
            _R_ear = self._map_ear(_R_ear_order,parameters,o)
            yield _L_ear,_R_ear

    def _map_ear(self,ear_order,parameters: spatialparameters._SpatialParameters,order):
        """
        computes spherical mapping with respect to
        sphericalparameters._SpatialParameters(...)

        all of order's variables are passed into the spatial
        parameters object except for distance which has already been calculated

        :return _SphericalMep(directions:[N,3],delay[N],dampness[N,F])
        """
        lines      = _to_line(ear_order._rays._locations, ear_order._ear_location)
        distances  = _distance(lines[:,0],lines[:,1]) + ear_order._rays._distances
        directions = _normalize(lines[:,1]-lines[:,0])
        delay = parameters._delay_time_for(distances)
        dampness  = self._dampness_initial.copy()
        # dampness -= triangulated surface area due to reflections and sound focusing
        dampness[:] -= parameters._atmospheric_attenuation_for(distances)
        dampness[:] -= parameters._wall_attenuation_for(order)
        return _SphericalTV(directions,delay,dampness)

