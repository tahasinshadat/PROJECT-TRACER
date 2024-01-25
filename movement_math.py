def convert_range(value, original_min, original_max, new_min, new_max):
    original_range = original_max - original_min
    new_range = new_max - new_min

    percentage = (value - original_min) / original_range

    return new_min + (percentage * new_range)

def get_DC_from_angle(angle):
    """Used for servos, pos is clockwise, 0 is vertical
       angle: value from -90 to 90"""
    return convert_range(90 + angle, 0, 180, 5, 10)