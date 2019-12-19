from Features.Feature import *
import igraph

class in_str_w0(Feature):

    def compute(self, g, vertex_id):
        val = g.strength(mode=igraph.IN, weights=None)
        return [val[vertex_id], self.avg(val)]

class in_str_w1(Feature):
    def compute(self, g, vertex_id):
        weights = self.get_weights(g)
        val = g.strength(mode=igraph.IN, weights=weights)
        return [val[vertex_id], self.avg(val)]

class out_str_w0(Feature):
    def compute(self, g, vertex_id):
        val = g.strength(mode=igraph.OUT, weights=None)
        return [val[vertex_id], self.avg(val)]

class out_str_w1(Feature):
    def compute(self, g, vertex_id):
        weights = self.get_weights(g)
        val = g.strength(mode=igraph.OUT, weights=weights)
        return [val[vertex_id], self.avg(val)]

class all_str_w0(Feature):
    def compute(self, g, vertex_id):
        val = g.strength(mode=igraph.ALL, weights=None)
        return [val[vertex_id], self.avg(val)]

class all_str_w1(Feature):
    def compute(self, g, vertex_id):
        weights = self.get_weights(g)
        val = g.strength(mode=igraph.ALL, weights=weights)
        return [val[vertex_id], self.avg(val)]
