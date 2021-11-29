import math
from global_v import *

def serialize(i, j):
    temp = j * ROWS + i
    return temp

def calc_dist(u, v):
    dist = ((u[1] - v[1])**2 + (u[0] - v[0])**2)**0.5
    return dist
