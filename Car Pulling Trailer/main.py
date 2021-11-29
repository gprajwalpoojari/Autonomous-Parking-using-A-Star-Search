from world import *
from math_lib import *
from algorithms_Trailer import *
from global_v import *
from wrapper import *

def main(world, SIZE):
    grid = []
    position = 4, 7
    heading = 0
    polygon_list = draw_world(world, grid, position, heading)
    iterations = run_AStar_package(grid, world, polygon_list)
    run = True
    while run:
        draw(grid, world)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

main(world, SIZE)
