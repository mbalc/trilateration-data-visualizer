from math import sqrt

import numpy as np

from src import config, utilities, read


# predeclarations were needed for typing operator arguments
class Point:
    pass


class Vector:
    pass


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other: Vector):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point):
        return Vector(self.x - other.x, self.y - other.y)


class Vector(Point):
    def __sum__(self, other: Vector):
        return Vector(other.x + self.x, other.y + self.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, scale):
        return Vector(self.x * scale, self.y * scale)

    def __pow__(self, arg):
        return self.x ** arg + self.y ** arg

    def rotate(self):
        """Rotate vector direction 90 degrees counter-clockwise"""
        return Vector(-self.y, self.x)


class Circle:
    def __init__(self, center: Point, radius):
        self.c = center
        self.r = radius


def intersect(o1: Circle, o2: Circle):
    """Return a list of points of intersection for given circles if they intersect,
    or of a midpoint of a distance between circles (between those points belonging to circles that
    are closest to each other)"""
    if o1.r < o2.r:
        return intersect(o2, o1)
    (c1, r1), (c2, r2) = (o1.c, o1.r), (o2.c, o2.r)

    center_dist_sq = (c2 - c1) ** 2
    center_dist = sqrt(center_dist_sq)
    if (r1 + r2) ** 2 <= center_dist_sq:  # circles too distant from each other
        mid_length = (center_dist - r1 - r2)
        return [c1 + ((c2 - c1) * ((r1 + mid_length / 2) / center_dist))]

    if (r1 - r2) ** 2 >= center_dist_sq:  # circles are self-contained
        mid_length = (r1 - center_dist - r2)
        return [c1 + ((c2 - c1) * ((center_dist + r2 + (mid_length / 2)) / center_dist))]

    else:  # circles have exactly two points of intersect:
        assert (center_dist > 0.)  # if these are equal, we should have handled it in cases above
        # i1, i2    - points of intersection,
        # mid       - orthographic projection of i1 onto p1p2 line
        # a = vector c1 -> mid, b = vector mid -> c2 (|b| may turn up negative when c2 is inside o1)
        # d = |a| + |b| = center_dist
        # r1^2 - |a|^2 = |mid  -> i1|^2 = r2^2 - |b|^2  (2x Pythagorean theorem
        # d(|a| - |b|) = r1^2 - r2^2   (we know d > 0)
        # |a| = |b| + ((r1^2 - r2^2)/d)
        p1_to_mid_length = (((r1 ** 2 - r2 ** 2) / center_dist) + center_dist) / 2
        mid = c1 + ((c2 - c1) * (p1_to_mid_length / center_dist))
        mid_to_i1_length = sqrt(r1 ** 2 - p1_to_mid_length ** 2)
        v1 = ((c2 - c1) * (mid_to_i1_length / center_dist)).rotate()
        i1 = mid + v1
        i2 = mid + (-v1)
        return [i1, i2]


def median(iterable):
    length = len(iterable)
    if length == 0:
        return 0
    out = iterable[int(length / 2)]
    if length % 2 == 0:
        point = iterable[int((length - 1) / 2)]
        out = tuple(a + b / 2 for a, b in zip(out, point))  # mean of two middle elements
    return out


@utilities.once
def intersections():
    tag_ids, readings = read.readings()
    _, anchors = read.anchors()

    assert (len(anchors.shape) == 2 and anchors.shape[1] == 2)
    assert (anchors.shape[0] == readings.shape[1])

    anchor_count = anchors.shape[0]

    circles = [(tag, [Circle(Point(*anchors[i]), elem[i]) for i in range(anchor_count)]) for
               tag, elem in zip(tag_ids, readings)]

    output = []

    for tag_id, reads in circles:
        inters = []
        for i1 in range(len(reads)):
            for i2 in range(i1 + 1, len(reads)):
                out = intersect(reads[i1], reads[i2])
                inters.extend(out)

        points = [(elem.x, elem.y) for elem in inters]

        # indepedent x and y median point
        med = (median(sorted(points, key=lambda elem: elem[0]))[0],
               median(sorted(points, key=lambda elem: elem[1]))[1])

        output.append((tag_id, list(
            filter(lambda elem: (med[0] - elem[0]) ** 2 + (med[1] - elem[1]) ** 2 < config.EPSILON,
                   points))))  # filter out those that are too distant from median

    return output


@utilities.once
def point_data():
    anchor_coords = read.anchors()[1]

    inters = intersections()
    readings = read.readings()
    points = []
    circs = []
    for inter_set, circ_set in zip(inters, readings[1]):
        points.append([sum(y) / len(y) for y in zip(*inter_set[1])])  # mean of all points
        circs.append(zip(anchor_coords, circ_set))

    return points, circs, inters


def index_by_mask(mask):
    return np.ma.array(range(len(mask)), mask=mask).compressed()


@utilities.once
def containment_data():
    tag_ids = read.readings()[0]
    pt_data = point_data()
    polys = read.polygons()

    cont_data = np.logical_not([poly.contains_points(pt_data[0]) for poly in polys])

    # special case for poly no. 1 - as stated in task description
    cont_data[1] = np.logical_or(cont_data[1], np.logical_not(cont_data[2]))

    pt_id_cont = [index_by_mask(cont) for cont in cont_data]
    # TODO check if tag_ids are not wrong
    tag_id_cont = [sorted(set([tag_ids[pt_id] for pt_id in poly_cont])) for poly_cont in pt_id_cont]

    not_in_any = index_by_mask(np.any(np.logical_not(cont_data), axis=0))

    return not_in_any, pt_id_cont, tag_id_cont
