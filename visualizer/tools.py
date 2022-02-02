import numpy as np
from OpenGL.GL import *

def _glVertexPointer(vertices):
    glVertexPointer(3, GL_FLOAT, 0, vertices)

def _glColorPointer(features):
    glColorPointer(3, GL_FLOAT, 0, features)

def _array(array):
    return np.array(array,dtype=np.float32)