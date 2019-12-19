from Features.Feature import *
import igraph

class in_clo_w0(Feature):
    def compute(self, g, vertex_id):
        val = g.closeness(mode=igraph.IN, weights=None)
        return [val[vertex_id], self.avg(val)]

class in_clo_w1(Feature):
    def compute(self, g, vertex_id):
        weights = self.get_weights(g)
        val = g.closeness(mode=igraph.IN, weights=weights)
        return [val[vertex_id], self.avg(val)]

class out_clo_w0(Feature):
    def compute(self, g, vertex_id):
        val = g.closeness(mode=igraph.OUT, weights=None)
        return [val[vertex_id], self.avg(val)]

class out_clo_w1(Feature):
    def compute(self, g, vertex_id):
        weights = self.get_weights(g)
        val = g.closeness(mode=igraph.OUT, weights=weights)
        return [val[vertex_id], self.avg(val)]

class all_clo_w0(Feature):
    def compute(self, g, vertex_id):
        val = g.closeness(mode=igraph.ALL, weights=None)
        return [val[vertex_id], self.avg(val)]

class all_clo_w1(Feature):
    def compute(self, g, vertex_id):
        weights = self.get_weights(g)
        val = g.closeness(mode=igraph.ALL, weights=weights)
        return [val[vertex_id], self.avg(val)]
