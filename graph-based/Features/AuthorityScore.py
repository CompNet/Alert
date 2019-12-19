from Features.Feature import *

class as_w0(Feature):
    def compute(self, g, vertex_id):
        val = g.authority_score(weights=None)
        return [val[vertex_id], self.avg(val)]

class as_w1(Feature):
    def compute(self, g, vertex_id):
        weights = self.get_weights(g)
        val = g.authority_score(weights=weights)
        return [val[vertex_id], self.avg(val)]