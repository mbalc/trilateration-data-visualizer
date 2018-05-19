import os

DATA_PATH = os.path.normpath(os.path.join(__file__, '..', '..', 'data'))
POLYGON_PATH = os.path.join(DATA_PATH, 'polygons')
VERTEX_PATH = os.path.join(DATA_PATH, 'vertices')
READING_PATH = os.path.join(DATA_PATH, 'readings')
ANCHOR_PATH = os.path.join(DATA_PATH, 'anchors')

"""parameter for filtering out non-relevant intersection points too distant from median point"""
EPSILON = 0.55
