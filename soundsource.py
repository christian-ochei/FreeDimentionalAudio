import numpy as np
import keyboard
_array = lambda pylist: np.array(pylist,dtype=np.float32)


class _3DSpatialSpeaker:
    def __init__(self,location=(0,0,0)):
        self.location = _array(location)
        self._speed = 0.01
        ...

    def render(self,accumulated):
        ...

    def __call__(self, *args, **kwargs):
        if keyboard.is_pressed('8'):self.location[...,1] += self._speed
        if keyboard.is_pressed('5'):self.location[...,1] -= self._speed

        if keyboard.is_pressed('4'):self.location[...,0] -= self._speed
        if keyboard.is_pressed('6'):self.location[...,0] += self._speed

        if keyboard.is_pressed('7'):self.location[...,2] += self._speed
        if keyboard.is_pressed('9'):self.location[...,2] -= self._speed
