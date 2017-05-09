import fiona
import osmium as o
import sys

geomfab = o.geom.GeoJSONFactory()

class ShapeConverter(o.SimpleHandler):
    def __init__(self, nodefile, wayfile, areafile):
        o.SimpleHandler.__init__(self)
        self.nodefile = nodefile
        self.wayfile = wayfile
        self.areafile = areafile

    def node(self, n):
        if 'amenity' in n.tags:
            name = n.tags['name'] if 'name' in n.tags else ''
            rec = {
                'geometry' : eval(geomfab.create_point(n)),
                'properties' : {
                    'id' : float(n.id),
                    'name' : name,
                    'kind' : n.tags['amenity']
                }
            }
            self.nodefile.write(rec)

    def way(self, w):
        if 'highway' in w.tags:
            name = w.tags['name'] if 'name' in w.tags else ''
            rec = {
                'geometry' : eval(geomfab.create_linestring(w)),
                'properties' : {
                    'id' : float(w.id),
                    'name' : name,
                    'kind' : w.tags['highway']
                }
            }
            self.wayfile.write(rec)

    def area(self, n):
        if 'boundary' in n.tags:
            name = n.tags['name'] if 'name' in n.tags else ''
            rec = {
                'geometry' : eval(geomfab.create_multipolygon(n)),
                'properties' : {
                    'id' : float(n.id),
                    'name' : name,
                    'kind' : n.tags['boundary']
                }
            }
            self.areafile.write(rec)



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python osm_file_stats.py <osmfile> <shapefile>")
        sys.exit(-1)

    drv = 'ESRI Shapefile'
    crs = {'no_defs': True, 'ellps': 'WGS84', 'datum': 'WGS84', 'proj': 'longlat'}
    scheman = {
        'geometry': 'Point',
        'properties': {'id': 'float', 'name' : 'str', 'kind' : 'str'},
    }
    schemaw = {
        'geometry': 'LineString',
        'properties': {'id': 'float', 'name' : 'str', 'kind' : 'str'},
    }
    schemaa = {
        'geometry': 'MultiPolygon',
        'properties': {'id': 'float', 'name' : 'str', 'kind' : 'str'},
    }
    with fiona.open(sys.argv[2], 'w', layer='node', driver=drv, crs=crs, schema=scheman) as nf:
        with fiona.open(sys.argv[2], 'w', layer='way', driver=drv, crs=crs, schema=schemaw) as wf:
            with fiona.open(sys.argv[2], 'w', layer='area', driver=drv, crs=crs, schema=schemaa) as af:
                h = ShapeConverter(nf, wf, af)

                h.apply_file(sys.argv[1], locations=True)


