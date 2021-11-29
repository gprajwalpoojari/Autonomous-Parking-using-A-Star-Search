from global_v import *
from world import *
from math_lib import *
from algorithms_helper import *
import heapq
import time


def Dijkstra(grid, world, polygon_list):
    robot_polygon = polygon_list[0]
    trailer_polygon = polygon_list[1]
    q = []
    DISTANCE[START] = 0
    robot_current_heading = robot_polygon.heading
    trailer_current_heading = trailer_polygon.heading
    x_robot = robot_polygon.position[0]
    y_robot = robot_polygon.position[1]
    x_trailer = trailer_polygon.position[0]
    y_trailer = trailer_polygon.position[1]
    values = x_robot, y_robot, robot_current_heading, x_trailer, y_trailer, trailer_current_heading
    start = x_robot, y_robot, robot_current_heading
    end = 45, 122, 0
    heapq.heappush(q, (DISTANCE[START] + calc_dist(start, end), values))
    delta_t = 1
    us_values = [-1.5, 1.5]
    u_phi_values = [-math.pi/7, 0,math.pi/7]
    L = 3
    width = 1.75
    d1 = 5
    pixel = 0.3
    while (len(q) != 0):
        priority, u = heapq.heappop(q)
        x_robot = u[0] * pixel
        y_robot = u[1] * pixel
        current_heading_robot = u[2]
        x_trailer = u[3] * pixel
        y_trailer = u[4] * pixel
        current_heading_trailer = u[5]
        possible_states = []
        for us in (us_values):
            for u_phi in (u_phi_values):
                theta_next_robot = us * math.tan(u_phi) / L * delta_t + current_heading_robot
                theta_next_trailer = us / d1 * math.sin(theta_next_robot - current_heading_trailer) * delta_t + current_heading_trailer
                x_next_robot = (us * math.cos(theta_next_robot) * delta_t + x_robot) / pixel
                y_next_robot = (us * math.sin(theta_next_robot) * delta_t + y_robot) / pixel
                x_next_trailer = (x_next_robot) - (d1 * math.cos(theta_next_trailer)) / pixel
                y_next_trailer = (y_next_robot) - (d1 * math.sin(theta_next_trailer)) / pixel
                position = [[round(x_next_robot), round(y_next_robot)], [round(x_next_trailer), round(y_next_trailer)]]
                heading = theta_next_robot * 180 / math.pi, theta_next_trailer * 180 / math.pi
                robot_lines, trailer_lines, robot, trailer = make_robot(grid, position, heading)
                next_config = [Polygon(position[0], heading[0], robot_lines), Polygon(position[1], heading[1], trailer_lines)]
                obstacles_robot_polygon = [next_config[1], polygon_list[2]]
                obstacles_trailer_polygon = [next_config[0], polygon_list[2]]
                if (robot != False and trailer != False):
                    if (collision_algorithm(next_config[0], obstacles_robot_polygon) == False and collision_algorithm(next_config[1], obstacles_trailer_polygon) == False):
                        values = x_next_robot,y_next_robot, theta_next_robot, x_next_trailer, y_next_trailer, theta_next_trailer, u_phi
                        possible_states.append(values)
        node = ROWS * round(u[1]) + round(u[0])
        for v in possible_states:
            new_node = ROWS * round(v[1]) + round(v[0])
            trailer_current_pose = u[3], u[4], u[5]
            trailer_new_pose = v[3], v[4], v[5]
            robot_lines, trailer_lines, robot, trailer = make_robot(grid, position, heading)
            if ((DISTANCE[new_node] > DISTANCE[node] + calc_dist(u, v)) and (robot != False and trailer != False)):
                dist = calc_dist(u, v)
                DISTANCE[new_node] = DISTANCE[node] + dist
                obs = 64, 64
                car1 = 4, 20
                cost_orientation = abs(v[2]) + abs(v[5])
                heapq.heappush(q, (DISTANCE[new_node] + calc_dist(v, end), v))
                PREVIOUS[new_node] = node, v[0], v[1], v[2], v[3], v[4], v[5]
        if (node == global_v.END):
            global_v.final = global_v.END, round(u[0]), round(u[1]), current_heading_robot, round(u[3]), round(u[4]), current_heading_trailer
            pose = [[u[0], u[1]], [u[3], u[4]]]
            head = [current_heading_robot, current_heading_trailer]
            line1, line2, rb, tr = make_robot(grid, position, heading)
            if (rb != False and tr != False):
                global_v.final = END, round(u[0]), round(u[1]), current_heading_robot, round(u[3]), round(u[4]), current_heading_trailer
                print("A-Star Search complete. Tracing path....")
                return (True)
        if (len(q) == 0):
            print("ERROR - A-Star: The given obstacle field does not have a path to destination.")
            return (False)
    return True
