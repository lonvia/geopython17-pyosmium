import osmium as o
import sys
import shapely.wkb as wkblib

wkbfab = o.geom.WKBFactory()

class AreaHandler(o.SimpleHandler):

    def area(self, a):
        if a.tags.get('building') != 'church':
            return

        outer_rings, inner_rings = a.num_rings()

        centroids = []
        for r in a.outer_rings():
            x, y = map(sum, zip(*[(n.lon, n.lat) for n in r]))
            centroids.append((x/len(r), y/len(r)))

        x, y = map(sum, zip(*centroids))
        x /= outer_rings
        y /= outer_rings

        print('W' if a.from_way() else 'R', a.orig_id(), x, y)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python list_churches.py <osmfile>")
        sys.exit(-1)

    AreaHandler().apply_file(sys.argv[1])

