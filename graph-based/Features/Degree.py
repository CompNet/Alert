from Features.Feature import *
import igraph

class in_deg(Feature):
    def compute(self, g, vertex_id):
        val = g.degree(mode=igraph.IN)
        return [val[vertex_id], self.avg(val)]


class out_deg(Feature):
    def compute(self, g, vertex_id):
        val = g.degree(mode=igraph.OUT)
        return [val[vertex_id], self.avg(val)]


class all_deg(Feature):
    def compute(self, g, vertex_id):
        val = g.degree(mode=igraph.ALL)
        return [val[vertex_id], self.avg(val)]
