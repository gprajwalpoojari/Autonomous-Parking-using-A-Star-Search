from algorithms_Trailer import *
from global_v import *

def run_AStar_package(grid, world, polygon_list):
    success = Dijkstra(grid, world, polygon_list)
    if success:
        path = trace_path(grid, world)
        draw(grid, world)
        return global_v.COUNT
    else:
        return 0
