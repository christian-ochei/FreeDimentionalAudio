import soundsource
import propagation
import densepropagation
import spatialparameters
import playback

import threading

class _SpatialPipeline:
    def __init__(self,room,head_extrinsic,rays_per_speaker=20,stemsdir='stems'):
        self._spatial_parameters = spatialparameters._SpatialParameters(
        )
        self._rays_per_speaker = rays_per_speaker
        self._stemsdir = stemsdir
        self._propergator = propagation._AudioPropagation(room=room,rays_per_speaker=rays_per_speaker)
        self._3d_sounds   = [soundsource._3DSpatialSpeaker()]
        self._active = True
        self._head_extrinsic = head_extrinsic
        self._player = playback.RealtimeSpatialPlayer()
        self._r_spherical_coefficients = None

    def _assign_binder(self,binder):
        self._propergator._binder = binder

    def _playback_thread(self):
        while True:
            if self._r_spherical_coefficients is not None:
               self._player(self._r_spherical_coefficients)

    def _pipeline(self):
        playback_thread = threading.Thread(target=self._playback_thread,args=())
        playback_thread.start()

        while self._active:
            for spatialsound in self._3d_sounds:
                spatialsound()
                # density:densepropagation._DensePropagation = self._propergator._propagate(spatialsound,self._head_extrinsic)
                # spherical_map = density._spherical_map(self._spatial_parameters)
                # spherical_coefficients = spherical_map._apply_hrtf(self._spatial_parameters._hrtf)
                # self._r_spherical_coefficients = spherical_coefficients
                # spherical_harmonics = density._spherical_harmonics(self._head_extrinsic)

    def _glDraw(self,binder):
        for sound in self._3d_sounds:
            ...
            # self._propergator._glDraw(sound,binder)