from global_v import *
from world import *
from math_lib import *
from algorithms_helper import *
import heapq


def AStar(grid, world, polygon_list):
    robot_polygon = polygon_list[0]
    obstacles_polygon = []
    for obstacle in range(3):
        obstacles_polygon.append(polygon_list[obstacle+1])
    q = []
    DISTANCE[START] = 0
    current_heading = robot_polygon.heading
    x = robot_polygon.position[0]
    y = robot_polygon.position[1]
    values = x, y, current_heading
    start = x, y, current_heading
    end = 32, 120, 0
    heapq.heappush(q, (DISTANCE[START] + calc_dist(start, end), values))
    delta_t = 1
    us_values = [-1.5, 0, 1.5]
    u_phi_values = [-math.pi/9, 0, math.pi/9]
    L = 2.8
    while (len(q) != 0):
        priority, u = heapq.heappop(q)
        x = u[0]
        y = u[1]
        current_heading = u[2]
        possible_states = []
        count = 0
        for us in (us_values):
            for u_phi in (u_phi_values):
                theta_next = us * math.tan(u_phi) / L * delta_t + current_heading
                x_next = us * math.cos(theta_next) * delta_t + x
                y_next = us * math.sin(theta_next) * delta_t + y
                position = round(x_next), round(y_next)
                heading = theta_next * 180 / math.pi
                vehicle = []
                robot_lines, robot = make_robot(grid, position, heading)
                next_config = Polygon(position, heading, robot_lines)

                if robot_lines == False:
                    continue
                else:
                    if not(collision_algorithm(next_config, obstacles_polygon)):
                        values = round(x_next, 2),round(y_next, 2), round(theta_next, 2), u_phi
                        print(values)
                        if (round(x_next) == round(x) and round(y_next) == round(y)):
                            continue
                        else:
                            possible_states.append(values)
        node = ROWS * round(y) + round(x)
        for v in possible_states:
            new_node = ROWS * round(v[1]) + round(v[0])
            if ((DISTANCE[new_node] > DISTANCE[node] + calc_dist(u, v))):
                dist = calc_dist(u, v)
                DISTANCE[new_node] = DISTANCE[node] + dist
                obs = 64, 64
                car1 = 4, 20
                car2 = 61, 120
                heapq.heappush(q, (DISTANCE[new_node] + (calc_dist(v, end))*(1 + (9/math.pi*abs(v[3]))) + (1000 / calc_dist(obs, v)) + (10 / calc_dist(car1, v)) + (10 / calc_dist(car2, v)) , v))
                PREVIOUS[new_node] = node, v[0], v[1], v[2]
        if (node == END and abs(current_heading * 180 /math.pi) < 5):
            global_v.final = END, round(x), round(y), current_heading
            print("A-Star Search complete. Tracing path....")
            return (True)
        if (len(q) == 0):
            print("ERROR - A-Star: The given obstacle field does not have a path to destination.")
            return (False)
    return True
