from world import *
from math_lib import *
from algorithms_Akerman import *
from global_v import *
from wrapper import *

def main(world, SIZE):
    grid = []
    polygon_list = draw_world(world, grid)
    run_AStar_package(grid, world, polygon_list)
    run = True
    while run:
        draw(grid, world)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

main(world, SIZE)
