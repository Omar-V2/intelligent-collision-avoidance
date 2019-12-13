import math as m

# This implementation of the liang-barsky algorithm is courtesy of the PySDL2 library
# All credit is to rightful authors:
# https://pysdl2.readthedocs.io/en/rel_0_9_4/modules/sdl2ext_algorithms.html

def liangbarsky(x_min, y_max, x_max, y_min, x1, y1, x2, y2):
    """Clips a line to a rectangular area.

    This implements the Liang-Barsky line clipping algorithm.  x_min,
    y_max, x_max and y_min denote the clipping area, into which the line
    defined by x1, y1 (start point) and x2, y2 (end point) will be
    clipped.

    If the line does not intersect with the rectangular clipping area,
    four None values will be returned as tuple. Otherwise a tuple of the
    clipped line points will be returned in the form (cx1, cy1, cx2, cy2).
    """
    dx = x2 - x1 * 1.0
    dy = y2 - y1 * 1.0
    dt0, dt1 = 0.0, 1.0
    xx1 = x1
    yy1 = y1

    checks = ((-dx, x1 - x_min),
              (dx, x_max - x1),
              (-dy, y1 - y_min),
              (dy, y_max - y1))
    for p, q in checks:
        if p == 0 and q < 0:
            return None
        if p != 0:
            dt = q / (p * 1.0)
            if p < 0:
                if dt > dt1:
                    return None
                dt0 = max(dt0, dt)
            else:
                if dt < dt0:
                    return None
                dt1 = min(dt1, dt)
    if dt0 > 0:
        x1 += dt0 * dx
        y1 += dt0 * dy
    if dt1 < 1:
        x2 = xx1 + dt1 * dx
        y2 = yy1 + dt1 * dy
    return x1, y1

def circle_line_intersection(line_start, line_end, circle_centre, radius):
    """
    Computes the intersection points, if any between a line segment
    and a circle.
    """
    delta_x = line_end[0] - line_start[0]
    delta_y = line_end[1] - line_start[1]
    circ_x = line_start[0] - circle_centre[0]
    circ_y = line_start[1] - circle_centre[1]
    # a, b and c are coefficients of quadratic equation
    a = delta_x**2 + delta_y**2
    b = (2 * delta_x * circ_x) + (2 * delta_y * circ_y)
    c = (circ_x**2) + (circ_y**2) - radius**2
    discriminant = b*b - (4*a*c)
    if discriminant < 0: # no intersection
        return None
    else:
        # only interested in t_1
        t_1 = (-b - (discriminant**0.5)) / (2*a)
        if 0 <= t_1 <= 1:
            x_1 = line_start[0] + (t_1 * delta_x)
            y_1 = line_start[1] + (t_1 * delta_y)
            return x_1, y_1


def get_distance(vec_1, vec_2):
    """
    Computes the euclidean distance between two vectors (tuples)
    through the use of pythagoras' theorem.
    """
    delta_x = vec_2[0] - vec_1[0]
    delta_y = vec_2[1] - vec_1[1]
    return m.sqrt((delta_x**2) + (delta_y**2))

def get_angle(pt_1, pt_2):
    """
    Computes the angle between the vector going from pt_1 to pt_2 and the x axis.
    """
    delta_x = pt_1[0] - pt_2[0]
    delta_y = pt_2[1] - pt_1[1]
    # negative because we have taken clockwise to be positive direction
    radians = -m.atan2(delta_y, delta_x)
    return m.degrees(radians)
