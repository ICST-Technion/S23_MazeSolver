import math

def get_rotation_direction(current_direction, next_direction):
    # Calculate the arctangent of current and next direction
    current_angle = math.atan2(current_direction[1], current_direction[0])
    next_angle = math.atan2(next_direction[1], next_direction[0])

    # Calculate the angle difference
    angle_difference = next_angle - current_angle

    # Normalize the angle difference to be between -180 and 180 degrees
    angle_difference = math.atan2(math.sin(angle_difference), math.cos(angle_difference))

    # Determine the rotation direction
    if angle_difference > 0:
        return abs(180*angle_difference/math.pi) # clockwise
    elif angle_difference < 0:
        return -abs(180*angle_difference/math.pi) # counterclockwise
    else:
        return 0

# Example usage
current_direction = (0, -1)  # Represents the current direction as a vector
next_direction = (-1, 0)   # Represents the next direction as a vector

rotation_direction = get_rotation_direction(current_direction, next_direction)
print("Rotation Direction:", rotation_direction)
