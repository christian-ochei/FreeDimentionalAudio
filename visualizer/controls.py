import keyboard
import numpy as np
import math as m
import win32api



class _RotationMatrix:
    def __init__(self):
        ...

    @staticmethod
    def matrix(theta):
        return (_RotationMatrix.rx(theta[0]) *
                _RotationMatrix.ry(theta[1]) *
                _RotationMatrix.rz(theta[2]))

    @staticmethod
    def rotate(vertices,theta):
        R = _RotationMatrix.matrix(theta)
        return R @ vertices

    @staticmethod
    def rx(theta):
        return np.matrix([[1, 0, 0],
                      [0, m.cos(theta), -m.sin(theta)],
                      [0, m.sin(theta), m.cos(theta)]])
    @staticmethod
    def ry(theta):
        return np.matrix([[m.cos(theta), 0, m.sin(theta)],
                          [0, 1, 0],
                          [-m.sin(theta), 0, m.cos(theta)]])
    @staticmethod
    def rz(theta):
        return np.matrix([[m.cos(theta), -m.sin(theta), 0],
                          [m.sin(theta), m.cos(theta), 0],
                          [0, 0, 1]])

def _array(x):
    return np.array(x,dtype=np.float32)

class _ViewController:
    def __init__(self):
        super(_ViewController, self).__init__()
        self._camera_T     = np.array((0,0,0),dtype=np.float32)
        self._camera_theta = np.array((0,0,0),dtype=np.float32)

        self._bf_camera_theta = np.array((0,0,0),dtype=np.float32)
        self._initial_pose = _array(win32api.GetCursorPos())
        self._initial_camera_theta = self._bf_camera_theta
        self._initial_key_press = False

        self._refresh  = False
        self._speed    = 0.2
        self._r_speed  = 0.2

    def __call__(self, *args, **kwargs):
        # Translations
        if keyboard.is_pressed('w'):self._camera_T[...,1] += self._speed
        if keyboard.is_pressed('s'):self._camera_T[...,1] -= self._speed

        if keyboard.is_pressed('a'):self._camera_T[...,0] -= self._speed
        if keyboard.is_pressed('d'):self._camera_T[...,0] += self._speed

        if keyboard.is_pressed('q'):self._camera_T[...,2] += self._speed
        if keyboard.is_pressed('e'):self._camera_T[...,2] -= self._speed

        # Rotations
        if keyboard.is_pressed('j'):self._camera_theta[...,1] += self._r_speed
        if keyboard.is_pressed('l'):self._camera_theta[...,1] -= self._r_speed

        if keyboard.is_pressed('i'):self._camera_theta[...,0] -= self._r_speed
        if keyboard.is_pressed('k'):self._camera_theta[...,0] += self._r_speed

        if keyboard.is_pressed('u'):self._camera_theta[...,2] += self._r_speed
        if keyboard.is_pressed('o'):self._camera_theta[...,2] -= self._r_speed

        left_key_state = win32api.GetKeyState(0x01)
        if left_key_state < 0:
            if not self._initial_key_press:
                self._initial_pose = _array(win32api.GetCursorPos())
                self._initial_camera_theta = self._camera_theta.copy()
            self._initial_key_press = True
            displacement = self._initial_pose - _array(win32api.GetCursorPos())
            self._bf_camera_theta = displacement/100
            self._camera_theta[...,[1,0]] = self._bf_camera_theta + \
                                            self._initial_camera_theta[...,[1,0]]
        else:
            # self._camera_theta[:] += self._bf_camera_theta
            self._bf_camera_theta[:] = 0
            self._initial_key_press = False

    def _control_bind(self,array):
        """
        :param array: np.array [...,3:point]
        :return:
        """
        array = np.copy(array)
        array -= self._camera_T
        array = np.array((np.matmul(_RotationMatrix.matrix(self._camera_theta),
                                    array.reshape(-1,3).T)).T).reshape(array.shape)
        return array
