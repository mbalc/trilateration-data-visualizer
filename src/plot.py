from random import randrange

import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import matplotlib
import numpy as np
from matplotlib.patches import Circle, Wedge

from src import read, analyze
from src.analyze import get_intersections


def make_circ(elem, *args, full=True, radius=0.04):
    def getter(el): return Wedge([*el], radius, 0, 360, width=0.004)

    if full:
        def getter(el): return Circle([*el], radius=radius)

    return getter(elem)


def init_polygons(ax):
    polygons = read.polygons()
    poly_coll = PatchCollection(polygons, alpha=0.6)
    poly_coll.set_facecolors(plt.get_cmap('Pastel1')(np.arange(.10, 1.99, .24)))
    poly_coll.set_edgecolor('black')
    ax.add_collection(poly_coll)


def init_anchors(ax):
    anchor_coords = read.anchors()[1]
    anchors = [make_circ(elem, radius=0.055) for elem in anchor_coords]
    anch_coll = PatchCollection(anchors, alpha=0.8)
    anch_coll.set_color('black')
    ax.add_collection(anch_coll)

    return anchor_coords


def create_inters(inter_set):
    inters = [make_circ(elem, full=False) for elem in inter_set[1]]
    i = PatchCollection(inters, alpha=1.0)
    i.set_visible(False)
    i.set_color('black')
    return i


def create_circs(circ_set):
    circs = [make_circ(elem, full=False, radius=r) for elem, r in circ_set]
    c = PatchCollection(circs, alpha=0.8)
    c.set_visible(False)
    return c


def init_points(ax, points):
    pt_coll = PatchCollection(points, alpha=0.6)
    colors = ['limegreen'] * len(points)
    pt_coll.set_facecolors(colors)
    pt_coll.set_edgecolor('black')
    ax.add_collection(pt_coll)
    return pt_coll, colors


def setup_plots(fig, ax, pt_coll, circ_colls, inter_colls, colors):
    plt.axis('equal', emit=True)
    plt.gca().set_ylim(-1.5, 1.5)
    plt.gca().set_xlim(-1.7, 1.7)

    active = -1

    def deactivate():
        circ_colls[active].set_visible(False)
        inter_colls[active].set_visible(False)
        colors[active] = 'limegreen'

    def hover(event):
        nonlocal active
        if event.inaxes == ax:
            ct, indexes = pt_coll.contains(event)
            ind = indexes['ind']
            if ct:
                if active not in ind:
                    deactivate()
                    active = ind[randrange(len(ind))]  # don't be arbitrary in ambiguous situations
                circ_colls[active].set_visible(True)
                inter_colls[active].set_visible(True)
                colors[active] = 'crimson'

            else:
                deactivate()

            pt_coll.set_facecolors(colors)
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)


def draw():
    matplotlib.pyplot.style.use('seaborn')
    fig, ax = plt.subplots()

    init_polygons(ax)
    anchor_coords = init_anchors(ax)

    inter_colls = []
    circ_colls = []
    points = []

    interesting_intersections = get_intersections()
    readings = read.readings()

    for point, circs, inters in analyze.get_point_data():
        points.append(make_circ(point, radius=0.03, full=True))
        circ_colls.append(create_circs(circs))
        inter_colls.append(create_inters(inters))

    pt_coll, colors = init_points(ax, points)

    for i, c in zip(inter_colls, circ_colls):
        ax.add_collection(i)
        ax.add_collection(c)

    setup_plots(fig, ax, pt_coll, circ_colls, inter_colls, colors)

    plt.show()


draw()
