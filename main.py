from src import read, analyze, plot


def print_list(arg, desc):
    print('    ' + desc + ' (' + str(len(arg)), 'in total) :')
    print(arg)


def print_results():
    print('\n########    RESULTS    ########\n')

    outside_pt_ids, poly_pt_ids, poly_tag_ids, _ = analyze.containment_data()

    for i in range(len(poly_pt_ids)):
        print('  Polygon no.', i, ':')
        print_list(poly_pt_ids[i], 'Point indices')
        print_list(poly_tag_ids[i], 'Tag-IDs')
        print()

    print('  Outside of all polygons :')
    print_list(outside_pt_ids, 'Point indices')

    ids = read.readings()[0]
    print('Most frequent Tag-ID:', max(set(ids), key=ids.count))

    print('\n########  RESULTS END  ########\n\n')


print('Reading files...')
read.readings()
read.anchors()
read.polygons()

print('Analysing intersections...')
analyze.intersections()
print('Analysing point data...')
analyze.point_data()
print('Analysing containment data...')
analyze.containment_data()

print_results()

print('Initiating plot...')
plot.draw()
