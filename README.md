<br>

# FreeDimentionalAudio



 I present FreeDimentionalAudio A framework that enables novel 3D binaural audio synthesis. This work showcases my new RayTracing approach to spatial audio and my love for music.

#

<br>

### Installation / Dependency

In order to use this framework you have to first install its dependencies
And doing that is as simple as running this in your command line

```
pip install requirements.txt
```

And all dependencies will get installed.
Make sure you are running the latest version of Python

#

<br>

### Experience Spatial Realism at a glance

Once all dependencies are installed. Get a pair of earphones, not headphones.
This part depends on face tracking in order to give the 3D effect. Make sure you are comfortable with that before proceeding to the next step.

Onces you are prepared just run this in the command line

```python
python demo.py 
```
and enjoy …


#

<br>


## This Pipeline in a Nutshell

### 1. A Small introduction video to the pipeline. 

```Main Thread```

Demo stems and stemsparser.py is included in the stems directory

I made the parser.py to automatically localize sound sources and animate them for a 
more amazing experience.

Just make sure the filename of each stems suffix is one of ```Vocals, Drums, Snares, Ambient, Mono, Hats, Crashes```

An Example will be 
```
entrance_downsweepCrashes.wav
```

### 2. A Highly efficient and Differentiable Spatial Audio Propagation Module 

```Thread 1```

I quickly Discovered direct ray tracing is not the most suitable solution to spatial audio propagation. This is due to rays not being able to account for directional waves and acoustic impedance. Instead of casting rays as lines. I decided to cast triangulated planes from which local sound intensity and total attenuation can be determined by a cubic interpolation of nearest areas. Read my paper for more information.

After computing a sound propagation template PropagationShere( … ) will be truncated. This holds information about how each sound source should change with respect to a sphere around the head.


### 3. Spherical Head Related Transfer function. 

```Thread 2```

Because the source sound differs from ear angles, the propagation sphere has to be attenuated with respect to the HRTF sphere.

```python
SpatialDescriptor( … ) = PropagationShere( … ) - HRTFSphere( … )
```

A Personalized Head Related Transfer function is very important for realistic spatial audio. Make sure you run the headcallibration.py file to get everything set up. Read more in the headcalibration folder


### 4. Realtime Audio Player 

```Thread 3```

This is one of the most crucial parts of this pipeline. It has to be fast, Robust to lags, It has to have almost zero latency, Thus it is the fastest thread.


### 5. Real Time Face Tracker  

```Thread 4```

For a truly immersive experience. FreeDimentionalAudio Requires known facial intrinsic and extrinsic parameters computed in real time. The easiest and least expensive method I could think of was a face tracker. To realize such idea, I took advantage of MediaPipe Face tracker which is crucial to this pipeline
	
Make sure to ```pip install mediapipe```


### Realtime - Visualizer  

```Main Thread```

I also built a small visualizer to display how sound and your face moves in real time

#
<br>

### Contributing to FreeDimentionalAudio

I am highly in need of contributors. please send a PR.
…
#
<br>
