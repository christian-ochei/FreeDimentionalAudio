"""
_HeadExtrinsic(...) Depends on metrics from the spatialparameters/parameters.py file
"""

import numpy as np
from OpenGL.GL import *
from spatialparameters import parameters


class _HeadExtrinsic:
    def __init__(self,face_tracker):
        self._face_tracker = face_tracker
        self._active = True
        self._registered_head_points = None
        self._L_ear_pose = None
        self._R_ear_pose = None
        self._depth_norm_simplices = np.random.randint(0,468-1,(100,2)) # TODO: Must be a seed not rand

    def _pipeline(self):
        _face_tracker = self._face_tracker
        while self._active:
            if _face_tracker._registered_landmarks is not None:
                landmarks:np.ndarray = - _face_tracker._registered_landmarks.copy()
                landmarks[...,:2] -= (_face_tracker._ih/2, _face_tracker._iw/2)
                rand_lines = landmarks[:,self._depth_norm_simplices]
                rand_lines = (rand_lines[:,:,0]-rand_lines[:,:,1])
                norm = 76/np.sqrt((rand_lines**2).sum(-1)).mean()
                landmarks *= norm
                landmarks[...] *= (parameters.distance_between_ears / 0.29997215915)
                landmarks[...,2] += norm*700
                landmarks = landmarks[...,[1,0,2]]/500
                self._registered_head_points = landmarks
                self._L_ear_pose = landmarks[0,454]
                self._R_ear_pose = landmarks[0,234]


    def _glDraw(self,binder):
        if self._registered_head_points is not None:
            head_points = self._registered_head_points
            head_points = binder(self._registered_head_points)
            glBegin(GL_POINTS)
            for vertex in head_points.reshape(-1,3):
                glColor3fv([0,0,0.2+vertex[2]/9])
                glVertex3f(*vertex)
            glEnd()
        ...



