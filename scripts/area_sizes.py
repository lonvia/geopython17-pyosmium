import osmium as o
import sys
import shapely.wkb

wkbfab = o.geom.WKBFactory()

class AreaHandler(o.SimpleHandler):

    def ring_area(self, r):
        total = 0.0
        prev = None
        for n in r:
            if prev is not None:
                total += prev[0] * n.lat - prev[1] * n.lon
            prev = (n.lon, n.lat)

        return (total)/2

    def area(self, a):
        if a.from_way():
            return

        outer_rings, inner_rings = a.num_rings()

        area = 0.0
        for r in a.outer_rings():
            area += self.ring_area(r)

            for i in a.inner_rings(r):
                area += self.ring_area(i)

        # create WKB from area
        wkb = wkbfab.create_multipolygon(a)
        # load into shapely
        poly = shapely.wkb.loads(wkb, hex=True)

        print('W' if a.from_way() else 'R', a.orig_id(), area, poly.area)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python list_churches.py <osmfile>")
        sys.exit(-1)

    AreaHandler().apply_file(sys.argv[1])

