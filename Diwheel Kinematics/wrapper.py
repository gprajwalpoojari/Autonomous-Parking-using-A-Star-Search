from algorithms_Diwheel import *
from global_v import *

def run_AStar_package(grid, world, polygon_list):
    success = AStar(grid, world, polygon_list)
    if success:
        trace_path(grid, world)
        draw(grid, world)
