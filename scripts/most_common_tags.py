import osmium
from collections import Counter

class TagStats(osmium.SimpleHandler):

    def __init__(self):
        super(TagStats, self).__init__()
        self.names = Counter()

    def way(self, w):
        if 'highway' in w.tags:
            self.names[w.tags.get('name', '<unknown>')] += 1


h = TagStats()
h.apply_file("../../data/switzerland-latest.osm.pbf")

for n,c in h.names.most_common(20):
    print(c,n)
