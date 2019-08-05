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
    return x1, y1, x2, y2

def circle_line_intersection(line_start, line_end, circle_centre, radius):
    pass


def get_distance(vec_1, vec_2):
    """
    Computes the euclidean distance between two vectors (tuples)
    through the use of pythagoras' theorem.
    """
    delta_x = vec_2[0] - vec_1[0]
    delta_y = vec_2[1] - vec_1[1]
    return m.sqrt((delta_x**2) + (delta_y**2))
    