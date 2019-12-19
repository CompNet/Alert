from Features.Feature import *

class hub_w0(Feature):
    def compute(self, g, vertex_id):
        val = g.hub_score(weights = None)
        return [val[vertex_id], self.avg(val)]


class hub_w1(Feature):
    def compute(self, g, vertex_id):
        weights = self.get_weights(g)
        val = g.hub_score(weights = weights)
        return [val[vertex_id], self.avg(val)]
