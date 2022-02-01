import random
import time

import keyboard
import numpy as np
from OpenGL.GL import *

import densepropagation

def _uniform_points_on_sphere(num_pts):
    indices = np.arange(0, num_pts, dtype=float) + 0.5
    phi = np.arccos(1 - 2 * indices / num_pts)
    theta = np.pi * (1 + 5 ** 0.5) * indices
    x,y,z = np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi)
    return _normalize(np.concatenate([x[...,None],y[...,None],z[...,None]],axis=-1))

def _distance(x,y:np.ndarray=0):
    return np.sqrt(np.square(x-y).sum(-1))

def _batch_index(values,index):
    assert len(values.shape) == 3
    return values.reshape(-1,values.shape[-1]) \
    [index + (np.arange(values.shape[0])*values.shape[1])[...,None]].reshape([*index.shape,values.shape[-1]])


def line_plane_intersection(planeNormal, planePoint, rayPoint,rayDirection, epsilon=1e-6):
    ndotu = _dot(planeNormal,(rayDirection))
    w = rayPoint - planePoint
    si = - _dot(planeNormal,(w)) / ndotu#(np.where(np.abs(ndotu)<0.001,0.001,ndotu))
    Psi = w + \
          si * \
          rayDirection + \
          planePoint
    return Psi

_array = lambda x:np.array(x,dtype=np.float64)

def _dot(x,y):
    return np.sum(x*y,axis=-1)[...,None]

def _normalize(V):
    return V/_distance(V)[...,None]

class _PropagatedRays:
    def __init__(self,locations,directions,distances):
        super(_PropagatedRays, self).__init__()
        self._locations   = locations
        self._directions  = directions
        self._distances   = distances

    def _glDraw(self,binder):
        glBegin(GL_LINES)
        for vertex in binder(self._as_lines().astype(np.float64)).reshape(-1, 3):
            glColor3fv([0.2 + vertex[2] / 9,0.,0.])
            glVertex3f(*vertex)
        glEnd()

    def _as_lines(self):
        as_lines = np.empty([len(self._locations),2,3])
        as_lines[...,0,:] = self._locations
        as_lines[...,1,:] = self._directions + self._locations
        return as_lines

    def __getitem__(self, item):
        return _PropagatedRays(
            self._locations[item],
            self._directions[item],
            self._distances[item],
        )

class _AudioPropagation:
    def __init__(self,room,rays_per_speaker):
        self._room = room
        self._rays_per_speaker = rays_per_speaker
        self._uniform_point_sphere = _uniform_points_on_sphere(rays_per_speaker)
        self._sound_sources = None
        self._intersection = None
        self._reflection_depth = 5
        self._binder = None # assigned from spatial.py
        self._first_order_ray = _PropagatedRays(
            locations=np.zeros([len(self._uniform_point_sphere),3],dtype=np.float64),
            directions=self._uniform_point_sphere,
            distances=np.zeros(len(self._uniform_point_sphere),dtype=np.float64),
        )
        self._propagation_orders = None
        self._ffinal_intersections = [] # TODO: DEBUG
        self._rays_ = []
        ...

    def _specular(self,ray_direction,quad_normals):
        return 2 * quad_normals*_dot(quad_normals,ray_direction) - ray_direction

    def _trace(self,rays):
        """
        :param rays: _PropagatedRays(...)
        :return:     _PropagatedRays(...)
        """
        D_N = 3
        positions    = np.tile(rays._locations[:,None],(1,D_N,1))
        direction    = np.tile(rays._directions[:,None],(1,D_N,1))
        quad_normals = np.tile(self._room._stage_quads_normals[None,:],(len(self._uniform_point_sphere),1,1))
        quad_point   = np.tile(self._room._stage_quads[None,:,2]      ,(len(self._uniform_point_sphere),1,1))

        w = np.concatenate([
            np.where(rays._directions[...,2]>0,0,1)[...,None],
            np.where(rays._directions[...,1]>0,2,3)[...,None],
            np.where(rays._directions[...,0]>0,4,5)[...,None]],axis=-1)

        quad_normals = _batch_index(quad_normals,w)
        quad_point   = _batch_index(quad_point,w)

        intersections = line_plane_intersection(
            quad_normals,quad_point,positions,_normalize(direction))

        distances = _distance(intersections,positions)
        closest = np.argmin(distances,axis=-1)[...,None]

        final_intersections = _batch_index(intersections,closest)[:,0]
        final_distances     = _batch_index(distances[...,None],closest)[...,0,0]
        closest_normal      = _batch_index(quad_normals,closest)[:,0]

        specular = - self._specular(rays._directions,closest_normal)
        final_directions = _normalize(specular)
        if len(self._rays_)<self._reflection_depth:
            self._rays_.append(rays._locations)
            self._ffinal_intersections.append(final_intersections)

        return _PropagatedRays(
            locations=final_intersections,
            directions=final_directions,
            distances=final_distances,
        )

    def _propagate(self,soundsource,ear_extrinsic):
        """
        :param ear_extrinsic._L_ear_pose: shape(3,)
        :param ear_extrinsic._R_ear_pose: shape(3,)
        :param soundsource.location       shape(N,3):
        :param soundsource.location       shape(N,3):
        :return:
        """
        self._first_order_ray._locations[:] = soundsource.location
        _reflection_orders = []
        _L_ear_orders = [densepropagation._CastedRay(self._first_order_ray[:1],ear_extrinsic._L_ear_pose)]
        _R_ear_orders = [densepropagation._CastedRay(self._first_order_ray[:1],ear_extrinsic._R_ear_pose)]
        _propagation_orders = [self._first_order_ray]

        for _ in range(self._reflection_depth):
            rays:_PropagatedRays = self._trace(_propagation_orders[-1])
            rays._distances[:] += _propagation_orders[-1]._distances
            _propagation_orders.append(rays)
            _L_ear_orders.append(densepropagation._CastedRay(rays,ear_extrinsic._L_ear_pose))
            _R_ear_orders.append(densepropagation._CastedRay(rays,ear_extrinsic._R_ear_pose))
        self._propagation_orders = _propagation_orders

        # TODO: DEBUG

        if not random.randint(0,8):
            self._ffinal_intersections = []
            self._rays_ = []

        return densepropagation._DensePropagation(_propagation_orders,_L_ear_orders,_R_ear_orders,
                                                  rays_per_speaker=self._rays_per_speaker)

    def _glDraw(self,sound_source,binder):
        ...
        for _rays_,_ffinal_intersections in zip(self._rays_,self._ffinal_intersections):
            glBegin(GL_LINES)
            for vertex,center in zip(
                    binder(_ffinal_intersections.astype(np.float64)).reshape(-1, 3),
                    binder(_rays_.astype(np.float64)).reshape(-1, 3)
            ):
                glColor3fv([1, 0., 0.])
                glVertex3f(*center)

                glColor3fv([1, 1., 0.])
                glVertex3f(*vertex)
            glEnd()

        # if self._propagation_orders is not None:
        #     for _propagation_order in self._propagation_orders[:1]:
        #         _propagation_order._glDraw(binder)
