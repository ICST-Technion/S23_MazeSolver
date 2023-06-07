import math
import numpy as np

def distance_from_line(line_point1, line_point2, point):
    # Calculate the direction vector of the line
    line_direction = (line_point2[0] - line_point1[0], line_point2[1] - line_point1[1])

    # Calculate the vector from the line point to the given point
    line_to_point_vector = (point[0] - line_point1[0], point[1] - line_point1[1])

    # Calculate the magnitude of the line direction vector
    line_direction_magnitude = math.sqrt(line_direction[0] ** 2 + line_direction[1] ** 2)

    # Calculate the projection of the line-to-point vector onto the line direction vector
    projection = (
            (line_to_point_vector[0] * line_direction[0] + line_to_point_vector[1] * line_direction[1])
            / line_direction_magnitude
    )

    # Calculate the projection vector
    projection_vector = (projection * line_direction[0] / line_direction_magnitude,
                         projection * line_direction[1] / line_direction_magnitude)

    # Calculate the distance vector from the line to the point
    distance_vector = (line_to_point_vector[0] - projection_vector[0],
                       line_to_point_vector[1] - projection_vector[1])

    # Calculate the distance from the line to the point
    distance = math.sqrt(distance_vector[0] ** 2 + distance_vector[1] ** 2)

    # Check which side of the line the point is on
    side = (line_to_point_vector[0] * line_direction[1] -
            line_to_point_vector[1] * line_direction[0])

    if side > 0:
        distance *= -1  # One side is considered negative

    return distance

def calculate_cos_theta(point1, point2):
    angle_1 = np.arctan2(point1[0], point1[1])
    angle_2 = np.arctan2(point2[0], point2[1])
    return angle_1 - angle_2

a = np.array((400, 600))
b = np.array((300, 600))
p = np.array((50, -50))
v1 = [100, 0]
v2 = [25, -25]

print(180*calculate_cos_theta(v1, v2)/np.pi)
print(distance_from_line(a, b, p))
