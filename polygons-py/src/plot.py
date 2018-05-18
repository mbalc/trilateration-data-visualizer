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

    anchor_coords = read_anchors()[1]
    anchors = [make_point(elem, radius=0.055) for elem in anchor_coords]
    a = PatchCollection(anchors, alpha=0.8)
    ax.add_collection(a)

    objs = [make_point(elem, full=False) for elem in get_objects()[0][1]]
    circs = [make_point(elem, full=False, radius=r) for elem, r in
             zip(anchor_coords, readings[1][5])]

    a.set_color('black')

    p = PatchCollection(polygons, alpha=0.6)
    o = PatchCollection(objs, alpha=1.0)
    c = PatchCollection(circs, alpha=0.8)

    c.set_visible(False)

    # colors = 100 * np.random.rand(len(polygons))
    p.set_facecolors(plt.get_cmap('Pastel1')(np.arange(.10, 1.99, .24)))
    p.set_edgecolor('black')
    # o.set_array((10 * np.ones(len(objs))))
    # c.set_array((10 * np.ones(len(objs))))
    # print(np.array(colors), 10 * np.ones(len(objs)))

    ax.add_collection(p)
    ax.add_collection(o)
    ax.add_collection(c)
    plt.axis([-2, 2, -2, 2])

    def hover(event):
        if event.inaxes == ax:
            if a.contains(event)[0]:
                c.set_visible(True)

            else:
                c.set_visible(False)

            fig.canvas.draw_idle()


    fig.canvas.mpl_connect("motion_notify_event", hover)
    plt.show()


draw()
