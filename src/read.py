import re

from matplotlib.patches import Polygon
import numpy as np

from src import config, utilities

FIND_FLOATS = r'[-+]?[0-9]*\.?[0-9]+'


def indexify(a_file, datatype=float):
    """Convert each file line into a tuple of row indexes list (row's first cell) and ndarray of
    values"""

    line_contents = [re.findall(FIND_FLOATS, line) for line in a_file.readlines()]
    return [int(elem[0]) for elem in line_contents], np.array(
        [[datatype(sub) for sub in elem[1:]] for elem in line_contents])


@utilities.once
def polygons():
    """Read contents of files set in config and prepare relevant Polygon patches basing on this
    data"""

    polygon_file = open(config.POLYGON_PATH, 'r')
    vertex_file = open(config.VERTEX_PATH, 'r')

    # the following two lines assume that row indexes match file line numbers in polygon and vertex
    # files
    _, polygon_desc = indexify(polygon_file, int)
    _, vertex_desc = indexify(vertex_file, float)

    shape = vertex_desc.shape
    assert (len(shape) == 2 and shape[1] == 2)

    polygon_verts = [np.array(vertex_desc[elem]) for elem in polygon_desc]

    polygons = [Polygon(elem) for elem in polygon_verts]

    return polygons


@utilities.once
def readings():
    return indexify(open(config.READING_PATH), float)


@utilities.once
def anchors():
    return indexify(open(config.ANCHOR_PATH), float)
