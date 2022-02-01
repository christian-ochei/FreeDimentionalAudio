"""
0.2999721592202008M == 0.1473m : My actual distance_between_ears
0.2999721592202008  /  0.1473 = 2.03647087
"""

m_to_M  = lambda v: v * 2.03647087
mm_to_m = lambda v: v * 0.001
mm_to_M = lambda v: m_to_M(mm_to_m(v))

