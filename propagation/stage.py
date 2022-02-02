import numpy as np
from OpenGL.GL import *

def _distance(x,y=0):
    return np.sqrt(np.square(x-y).sum(-1))

class _StageHandler:
    def __init__(self):
        self._size = size = 26
        self._div = div = 7

        B = size / div
        Y = -2.1
        YH = 1.8
        LINES = np.zeros([size, 2, 3])
        ARR = (np.arange(size)[..., None] - (size / 2)) * 2
        LINES[:] += [[[-size, Y * div, 0], [size, Y * div, 0]]]
        LINES[:, :, 2] += ARR
        LINES[:] /= div
        LINES_Y = np.zeros([size, 2, 3])
        LINES_Y[:] += [[[0, Y * div, -size], [0, Y * div, size]]]
        LINES_Y[:, :, 0] += ARR
        LINES_Y[:] /= div
        B_D = 2
        W = (640 / 140) / B_D
        H = (480 / 140) / B_D

        self._lines   = LINES
        self._lines_y = LINES_Y

        self._camera_p = np.array([
            [[0, 0, 0], [-W, YH, B]],
            [[0, 0, 0], [W, YH, B]],
            [[0, 0, 0], [-W, Y, B]],
            [[0, 0, 0], [W, Y, B]],
        ], dtype=np.float32)

        self._stage_points = np.array([
            [[-B, Y, -B],
            [B,   Y, -B],
            [B,  YH, -B],
            [-B, YH, -B]],

            [[-B, Y, B],
            [B,   Y, B],
            [B,  YH, B],
            [-B, YH, B]],

            [[-B, Y, -B],
             [-B, Y, B],
             [B, Y, B],
             [B, Y, -B]],

            [[-B, YH, -B],
             [-B, YH, B],
             [B,  YH, B],
             [B,  YH, -B]],

            [[-B, Y, -B],
             [-B, Y, B],
             [-B, YH, B],
             [-B, YH, -B]],

            [[B, Y, -B],
             [B, Y, B],
             [B, YH, B],
             [B, YH, -B]],

        ])

        self._stage_faces = np.array([
            [0,1,2,3],
            [4,5,6,7],
            [0,1,5,4],
            [3,2,7,6],
            [0,3,7,4],
            [1,2,5,6],
        ])

        self._stage_quads = self._stage_points
        U = (self._stage_quads[:, 1] - self._stage_quads[:, 0])[..., None]
        V = (self._stage_quads[:, 3] - self._stage_quads[:, 0])[..., None]

        self._stage_quads_normals =  - np.concatenate([
            U[:, 1] * V[:, 2] - U[:, 2] * V[:, 1],
            U[:, 2] * V[:, 0] - U[:, 0] * V[:, 2],
            U[:, 0] * V[:, 1] - U[:, 1] * V[:, 0]
        ], axis=-1)


        self._stage_quads_normals[[0,2,4]] = -self._stage_quads_normals[[0,2,4]]
        self._stage_quads_normals /= _distance(self._stage_quads_normals)[...,None]

        self._stage_boundaries = np.array([
            [[B, YH, B], [-B, YH, B]],
            [[-B, YH, B], [-B, Y, B]],
            [[-B, Y, B], [B, Y, B]],
            [[B, Y, B], [B, YH, B]],
            [[B, YH, -B], [-B, YH, -B]],
            [[-B, YH, -B], [-B, Y, -B]],
            [[-B, Y, -B], [B, Y, -B]],
            [[B, Y, -B], [B, YH, -B]],
            [[B, Y, B], [B, Y, -B]],
            [[B, YH, B], [B, YH, -B]],
            [[-B, YH, B], [-B, YH, -B]],
            [[B, YH, B], [B, YH, -B]],
        ], dtype=np.float32)


    def _glDraw(self,binder):
        LINES_ = binder(self._lines)
        LINES_Y_ = binder(self._lines_y)
        CAMERA_P_ = binder(self._camera_p)
        STAGE_BOUNDARIES_ = binder(self._stage_boundaries)
        _stage_quads = binder(self._stage_quads)
        glBegin(GL_LINES)
        for vertex in LINES_.reshape(-1, 3):
            glColor3fv([0.2 + vertex[2] / 9] * 3)
            glVertex3f(*vertex)
        for vertex in LINES_Y_.reshape(-1, 3):
            glColor3fv([0.2 + vertex[2] / 9] * 3)
            glVertex3f(*vertex)

        for i,vertex in enumerate(_stage_quads):
            glColor3fv([0, 0, 0.2 + vertex[0,2] / 9])
            glVertex3f(*vertex[0])

            glColor3fv([0, 0, 0.2 + vertex[1,2] / 9])
            glVertex3f(*vertex[1])

            glColor3fv([0, 0, 0.2 + vertex[1,2] / 9])
            glVertex3f(*vertex[1])

            glColor3fv([0, 0, 0.2 + vertex[2,2] / 9])
            glVertex3f(*vertex[2])

            glColor3fv([0, 0, 0.2 + vertex[2,2] / 9])
            glVertex3f(*vertex[2])

            glColor3fv([0, 0, 0.2 + vertex[3,2] / 9])
            glVertex3f(*vertex[3])
        for vertex in STAGE_BOUNDARIES_.reshape(-1, 3):
            glColor3fv([0, 0, 0.2 + vertex[2] / 9])
            glVertex3f(*vertex)
        for vertex in CAMERA_P_.reshape(-1, 3):
            glColor3fv([(0.2 + vertex[2] / 9) / 2] * 3)
            glVertex3f(*vertex)
        glEnd()
        ...