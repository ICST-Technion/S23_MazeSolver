import math


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


a = (400, 600)
b = (300, 600)
p = (350, 580)

print(distance_from_line(a, b, p))
