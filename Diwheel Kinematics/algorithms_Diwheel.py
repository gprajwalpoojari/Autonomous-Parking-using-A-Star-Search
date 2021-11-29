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
    start = x, y, current_heading
    end = 32, 120, 0
    heapq.heappush(q, (DISTANCE[START] + calc_dist(start, end), start))
    delta_t = 1
    ur_values = [-0.7, 0, 0.7]
    ul_values = [-0.7, 0, 0.7]
    maximum = max(ur_values)
    print(maximum)
    r = 3
    L = 9
    while (len(q) != 0):
        priority, u = heapq.heappop(q)
        x = u[0]
        y = u[1]
        current_heading = u[2]
        possible_states = []
        for ur in (ur_values):
            for ul in (ul_values):
                u_omega = (ul + ur) / 2
                u_phi = ur - ul
                theta_next = r / L * u_phi * delta_t + current_heading
                x_next = r * u_omega * math.cos(theta_next) * delta_t + x
                y_next = r * u_omega * math.sin(theta_next) * delta_t + y
                position = round(x_next), round(y_next)
                heading = theta_next * 180 / math.pi
                robot_lines, robot = make_robot(grid, position, heading)
                next_config = Polygon(position, heading, robot_lines)

                if robot_lines == False:
                    continue
                else:
                    if not(collision_algorithm(next_config, obstacles_polygon)):
                        values = round(x_next, 2),round(y_next, 2), round(theta_next, 2), u_omega, u_phi
                        print(values)
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
                reverse = abs(min(v[3], 0))
                reverse_cost = reverse / maximum
                steering_cost = 5 * abs(v[4])/ maximum * calc_dist(v, end)
                obstacle_cost = (5000 / calc_dist(obstacles_polygon[2].position, v)) + (100 / calc_dist(obstacles_polygon[0].position, v)) + (100 / calc_dist(obstacles_polygon[1].position, v))
                heapq.heappush(q, (DISTANCE[new_node] + calc_dist(v, end) + steering_cost + reverse_cost + obstacle_cost, v))
                PREVIOUS[new_node] = node, v[0], v[1], v[2]
        if (node == END and abs(current_heading * 180 /math.pi) < 5):
            global_v.final = END, round(x), round(y), current_heading
            print("A-Star Search complete. Tracing path....")
            return (True)
        if (len(q) == 0):
            print("ERROR - A-Star: The given obstacle field does not have a path to destination.")
            return (False)
    return True
