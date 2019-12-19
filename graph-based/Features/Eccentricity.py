from Features.Feature import *
import igraph

class in_ecc(Feature):
    def compute(self, g, vertex_id):
        val = g.eccentricity(mode=igraph.IN)
        return [val[vertex_id], self.avg(val)]


class out_ecc(Feature):
    def compute(self, g, vertex_id):
        val = g.eccentricity(mode=igraph.OUT)
        return [val[vertex_id], self.avg(val)]

class all_ecc(Feature):
    def compute(self, g, vertex_id):
        val = g.eccentricity(mode=igraph.ALL)
        return [val[vertex_id], self.avg(val)]
