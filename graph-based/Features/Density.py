from Features.Feature import *

class density(Feature):
    def compute(self, g, vertex_id):
        val = g.density()
        return val 