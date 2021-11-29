from global_v import *
from math_lib import *
import copy
import pygame
import math
import random
import global_v

world = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption('Path Planner')

class Polygon:
    def __init__(self, position, heading, lines):
        self.position = position
        self.heading = heading
        self.lines = lines

class Block:
    def __init__(self, row, col, color, size):
        self.row = row
        self.col = col
        self.size = size
        self.x = row * size
        self.y = col * size
        self.color = color

    def draw_block(self, world):
        pygame.draw.rect(world, self.color, (self.x, self.y, self.size, self.size))

def initialize_world(grid):
    block_size = SIZE // ROWS
    for i in range(ROWS):
        grid.append([])
        for j in range(ROWS):
            block = Block(i, j, WHITE, block_size)
            grid[i].append(block)
            VERTICES.append(block)
            EDGE_LIST.append([])
            DISTANCE.append(math.inf)
            PREVIOUS.append([])

def draw_grid_borders(world):
    block_size = SIZE // ROWS
    for i in range(ROWS):
        pygame.draw.line(world, BLACK, (0, i * block_size), (SIZE, i * block_size))
        for j in range(ROWS):
            pygame.draw.line(world, BLACK, (j * block_size, 0), (j * block_size, SIZE))

def make_vehicle_points():
    points = []
    x, y = 0, 0
    a, b = x + 8, y + 3
    temp = a, b
    points.append(temp)
    b = y - 2
    temp = a, b
    points.append(temp)
    a = x - 1
    temp = a, b
    points.append(temp)
    b = y + 3
    temp = a, b
    points.append(temp)

    return points

def transform_coordinates(points, position, heading):
    for i in range(len(points)):
        a, b = points[i]
        new_a = a * math.cos(math.pi/180 * heading) - b * math.sin(math.pi/180 * heading)
        new_b = a * math.sin(math.pi/180 * heading) + b * math.cos(math.pi/180 * heading)
        new_a = new_a + position[0]
        new_b = new_b + position[1]
        if round(new_a) < 0 or round(new_b) < 0 or round(new_a) > 127 or round(new_b) > 127:
            return False
        else:
            temp = round(new_a), round(new_b)
            points[i] = temp
    return points

def make_end_point_pairs(points):
    lines = []
    for j in range(len(points)):
        line = []
        line.append(points[j])
        if (j == len(points) - 1):
            line.append(points[0])
        else:
            line.append(points[j + 1])
        lines.append(line)
    return lines

def make_bresenham_lines(lines):
    rasterized_line = []
    for i in lines:
        x, y = i[0]
        x2, y2 = i[1]
        line = []
        line.append(i[0])
        dx = abs(x2 - x)
        dy = -abs(y2 - y)
        sx = 1 if x < x2 else -1
        sy = 1 if y < y2 else -1
        err = dx + dy;
        while (x != x2 or y != y2):
            e2 = 2*err
            if (e2 >= dy):
                err += dy
                x += sx
            if (e2 <= dx):
                err += dx
                y+=sy
            temp = x, y
            line.append(temp)
        temp = x2, y2
        line.append(i[1])
        rasterized_line.append(line)
    return rasterized_line

def make_filled_polygon(rasterized_lines, color):
    block_size = SIZE // ROWS
    vehicle = []
    x0 = []
    x1 = []
    for t in range(ROWS):
        x0.append(-1)
        x1.append(-1)
    for rasterized_line in rasterized_lines:
        for element in rasterized_line:
            x, y = element
            if (x0[y] == -1):
                x0[y] = x
                x1[y] = x
            else:
                x0[y] = min(x0[y], x)
                x1[y] = max(x1[y], x)
    n=0
    for y in range(ROWS):
        if (x0[y]!= -1):
            vehicle.append([])
            for x in range(x0[y], x1[y]):
                    block = Block(x, y, color, block_size)
                    vehicle[n].append(block)
            n = n+1
    x0.clear()
    x1.clear()
    return vehicle

def make_obstacle_points():
    points = []
    x, y = 0, 0
    a, b = x + 16, y + 16
    temp = a, b
    points.append(temp)
    b = y - 15
    temp = a, b
    points.append(temp)
    a = x - 15
    temp = a, b
    points.append(temp)
    b = y + 16
    temp = a, b
    points.append(temp)
    return points

def make_robot(grid, position, heading):
    block_size = SIZE // ROWS
    points_vehicle = make_vehicle_points()
    points_trailer = make_vehicle_points()
    points_vehicle = transform_coordinates(points_vehicle, position[0], heading[0])
    points_trailer = transform_coordinates(points_trailer, position[1], heading[1])
    if points_vehicle == False or points_trailer == False:
        return False, False, False, False
    lines_vehicle = make_end_point_pairs(points_vehicle)
    lines_trailer = make_end_point_pairs(points_trailer)
    rasterized_lines_vehicle = make_bresenham_lines(lines_vehicle)
    rasterized_lines_trailer = make_bresenham_lines(lines_trailer)

    robot = make_filled_polygon(rasterized_lines_vehicle, GREEN)
    trailer = make_filled_polygon(rasterized_lines_trailer, GREEN)
    return lines_vehicle, lines_trailer, robot, trailer

def place_robot(grid, vehicle, trailer):
    for i in range(len(vehicle)):
        for j in range(len(vehicle[i])):
            grid[vehicle[i][j].row][vehicle[i][j].col].color = vehicle[i][j].color
    for i in range(len(trailer)):
        for j in range(len(trailer[i])):
            grid[trailer[i][j].row][trailer[i][j].col].color = trailer[i][j].color

def make_vehicle(grid, position, heading):
    block_size = SIZE // ROWS
    vehicle = []
    points = make_vehicle_points()
    points = transform_coordinates(points, position, heading)
    if points == False:
        return False
    lines = make_end_point_pairs(points)
    rasterized_lines = make_bresenham_lines(lines)
    vehicle = make_filled_polygon(rasterized_lines, RED)

    for i in range(len(vehicle)):
        for j in range(len(vehicle[i])):
            grid[vehicle[i][j].row][vehicle[i][j].col].color = vehicle[i][j].color
    return lines

def make_obstacle(grid, position, heading):
    block_size = SIZE // ROWS
    vehicle = []
    points = make_obstacle_points()
    points = transform_coordinates(points, position, heading)
    if points == False:
        return False
    lines = make_end_point_pairs(points)
    rasterized_lines = make_bresenham_lines(lines)
    vehicle = make_filled_polygon(rasterized_lines, BLACK)


    for i in range(len(vehicle)):
        for j in range(len(vehicle[i])):
            grid[vehicle[i][j].row][vehicle[i][j].col].color = vehicle[i][j].color
    return lines


def clear_vehicle(grid, robot, trailer):
    for i in range(len(robot)):
        for j in range(len(robot[i])):
            grid[robot[i][j].row][robot[i][j].col].color = WHITE
    for i in range(len(trailer)):
        for j in range(len(trailer[i])):
            grid[trailer[i][j].row][trailer[i][j].col].color = WHITE

def place_obstacle(grid):
    position1 = 6, 122
    # position2 = 61, 120
    heading1 = 0
    vehicle1 = make_vehicle(grid, position1, heading1)
    vehicle1_polygon = Polygon(position1, heading1, vehicle1)
    # vehicle2 = make_vehicle(grid, position2, heading1)
    # vehicle2_polygon = Polygon(position2, heading1, vehicle2)
    position2 = 64, 64
    obstacle = make_obstacle(grid, position2, heading1)
    obstacle_polygon = Polygon(position2, heading1, obstacle)
    position_robot = 19, 6
    position_trailer = 4, 6
    position = [position_robot, position_trailer]
    heading_robot = 0
    heading_trailer = 0
    heading = [heading_robot, heading_trailer]
    vehicle = []
    robot_lines, trailer_lines, robot, trailer = make_robot(grid, position, heading)
    # place_robot(grid, robot, trailer)
    robot_polygon = Polygon(position[0], heading[0], robot_lines)
    trailer_polygon = Polygon(position[1], heading[1], trailer_lines)
    polygons = []
    polygons.append(robot_polygon)
    polygons.append(trailer_polygon)
    polygons.append(vehicle1_polygon)
    # polygons.append(obstacle_polygon)
    return polygons


def draw(grid, world):
    for row in grid:
        for block in row:
            block.draw_block(world)
    draw_grid_borders(world)
    pygame.display.update()

def draw_world(world, grid, position, heading):
    initialize_world(grid)
    cells = len(VERTICES)
    obs_cells = global_v.DENSITY * cells
    count = 4
    obstacle_list = place_obstacle(grid)
    draw(grid, world)
    return obstacle_list
