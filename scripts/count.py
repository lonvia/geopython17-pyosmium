import osmium

class FileStatsHandler(osmium.SimpleHandler):

    def __init__(self):
        super(FileStatsHandler, self).__init__()
        self.count = [0, 0, 0]

    def node(self, n):
        self.count[0] += 1

    def way(self, w):
        self.count[1] += 1

    def relation(self, r):
        self.count[2] += 1


h = FileStatsHandler()

h.apply_file("../../data/switzerland-latest.osm.pbf")

print("Nodes: %d Ways: %d Relations: %d" % tuple(h.count))

