from Features.Feature import *
import igraph

class in_core(Feature):
    def compute(self, g, vertex_id):
        val = g.coreness(mode=igraph.IN)
        return [val[vertex_id], self.avg(val)]

class out_core(Feature):
    def compute(self, g, vertex_id):
        val = g.coreness(mode=igraph.OUT)
        return [val[vertex_id], self.avg(val)]

class all_core(Feature):

    def compute(self, g, vertex_id):
        val = g.coreness(mode=igraph.ALL)
        return [val[vertex_id], self.avg(val)]
