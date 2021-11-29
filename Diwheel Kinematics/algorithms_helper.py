from global_v import *
from math_lib import *
from world import *
import matplotlib.pyplot as plt

def cross_product(line, point):
    x1 = line[1][0] - line[0][0]
    y1 = line[1][1] - line[0][1]
    x2 = point[0] - line[0][0]
    y2 = point[1] - line[0][1]
    cross = x1 * y2 - x2 * y1
    return cross

def collision_algorithm(robot_polygon, obstacles_polygon):
    COLLISION = False
    for i in range(len(obstacles_polygon)):
        for j in range(len(robot_polygon.lines)):
            for k in range(len(obstacles_polygon[i].lines)):
                probability = [False, False]
                exception = [False, False]
                line = [0, 0]
                line[0] = robot_polygon.lines[j]
                line[1] = obstacles_polygon[i].lines[k]

                #for each line l in [l0, l1]
                for l in range(2):
                    m = 1 if l == 0 else 0

                    #for each point p in the other line
                    cross = [0,0]
                    for n in range(2):
                        cross[n] = cross_product(line[l],line[m][n])

                    #If the two cross products have opposite sign, or one of them is zero
                    if (cross[0] * cross[1] <= 0):
                        if (cross[0] != 0 or cross[1] != 0):
                            probability[l] = True
                        #store true value if only one of them is zero
                        if (cross[0] == 0 or cross[1] == 0):
                            exception[l] = True
                        else:
                            exception[l] = False
                    else:
                        probability[l] = False

                #If both cross product checks above indicated opposite signs,
                if (probability[0] and probability[1] == True):
                    #check for atleast one zero cross product in both cases
                    if (not(exception[0] and exception[1])):
                          COLLISION = True
                          break

        #check for complete overlap
        if (COLLISION == False):
            collision = [False, False]
            polygon = [robot_polygon, obstacles_polygon[i]]
            #for each polygon
            for j in range(2):
                k = 1 if j == 0 else 0
                cross = [0, 0, 0, 0]
                #for each line in polygon[j]
                for l in range(len(polygon[j].lines)):
                    cross[l] = cross_product(polygon[j].lines[l], polygon[k].lines[0][1])
                for m in range(len(polygon[j].lines)):
                    if (cross[m] > 0):
                        collision[j] = False
                        break
                else:
                    collision[j] = True

            if (collision[0] and collision[1]):
                COLLISION = True
                break

    if (COLLISION == True):
        return True
    else:
        return False

def trace_path(grid, world):
    end = global_v.final
    result = []
    last = end[0]
    first = start[0]
    while (last != first):
        result.append(end)
        end = PREVIOUS[last]
        position = round(end[1]), round(end[2])
        heading = end[3]
        last = end[0]
    result.append(start)
    result.reverse()
    # vehicle = []
    # position = []
    # heading = []
    x_plt = []
    y_plt = []
    for state in result:
        x_plt.append(state[1])
        y_plt.append(-1 * state[2])
        temp = []
        position = round(state[1]), round(state[2])
        heading = state[3] * 180 / math.pi
        temp_lines, vehicle = make_robot(grid, position, heading)
        # place_robot(grid, vehicle)
        grid[round(position[0])][round(position[1])].color = BLUE
        draw(grid, world)
        # clear_vehicle(grid, vehicle)
    plt.plot(x_plt, y_plt)
    plt.show()
    temp, vehicle = make_robot(grid, position, heading)
    # place_robot(grid, vehicle)
    draw(grid, world)
    print("Done.")
