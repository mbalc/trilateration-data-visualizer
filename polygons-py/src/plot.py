import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import matplotlib
import numpy as np
from matplotlib.patches import Circle, Wedge

from src.analyze import get_objects
from src.read import read_polygons, read_anchors, read_readings


def make_point(elem, *args, full=True, radius=0.04):
    def getter(el): return Wedge([*el], radius, 0, 360, width=0.004, edgecolor='black')

    if full:
        def getter(el): return Circle([*el], radius=radius, color='black', facecolor='black',
                                      edgecolor='black')
    return getter(elem)


def draw():
    matplotlib.pyplot.style.use('seaborn')
    fig, ax = plt.subplots()

    polygons = read_polygons()
    readings = read_readings()

    poly_coll = PatchCollection(polygons, alpha=0.6)
    poly_coll.set_facecolors(plt.get_cmap('Pastel1')(np.arange(.10, 1.99, .24)))
    poly_coll.set_edgecolor('black')
    ax.add_collection(poly_coll)

    anchor_coords = read_anchors()[1]
    anchors = [make_point(elem, radius=0.055) for elem in anchor_coords]
    anch_coll = PatchCollection(anchors, alpha=0.8)
    anch_coll.set_color('black')
    ax.add_collection(anch_coll)

    inter_colls = []
    circ_colls = []
    points = []

    interesting_intersections = get_objects()
    for inter_set, circ_set in zip(interesting_intersections, readings[1]):
        mean = [sum(y) / len(y) for y in zip(*inter_set[1])]
        points.append(make_point(mean, radius=0.03, full=True))

        inters = [make_point(elem, full=False) for elem in inter_set[1]]
        i = PatchCollection(inters, alpha=1.0)
        i.set_visible(False)
        i.set_color('black')
        inter_colls.append(i)

        circs = [make_point(elem, full=False, radius=r) for elem, r in zip(anchor_coords, circ_set)]
        c = PatchCollection(circs, alpha=0.8)
        c.set_visible(False)
        circ_colls.append(c)

    pt_coll = PatchCollection(points, alpha=0.6)
    colors = ['limegreen'] * len(points)
    pt_coll.set_facecolors(colors)
    pt_coll.set_edgecolor('wheat')
    ax.add_collection(pt_coll)

    for i, c in zip(inter_colls, circ_colls):
        ax.add_collection(i)
        ax.add_collection(c)

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
        # print(active, circ_colls[active], pt_coll.contains(event)[1])
        if event.inaxes == ax:
            ct, ind = pt_coll.contains(event)
            if ct:
                if active not in ind['ind']:
                    deactivate()
                    active = ind['ind'][0]
                circ_colls[active].set_visible(True)
                inter_colls[active].set_visible(True)
                colors[active] = 'red'

            else:
                deactivate()

            pt_coll.set_facecolors(colors)
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)
    plt.show()


draw()
