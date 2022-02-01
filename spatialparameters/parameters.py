"""
All distance metrics must be in form of M (Meters in view coordinates)

speed_of_sound : seconds per meter
"""
from . conversions import *

distance_between_ears  = mm_to_M(147.3)
inverse_speed_of_sound = 1 / m_to_M(343)
