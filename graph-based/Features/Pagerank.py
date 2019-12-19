from Features.Feature import *

class pr_c_w0_d0(Feature):
    def compute(self, g, vertex_id):
        val = g.pagerank(directed=False)
        return [val[vertex_id], self.avg(val)]

class pr_c_w0_d1(Feature):
    def compute(self, g, vertex_id):
        val = g.pagerank(directed=True)
        return [val[vertex_id], self.avg(val)]


class pr_c_w1_d0(Feature):
    def compute(self, g, vertex_id):
        weights = self.get_weights(g)
        val = g.pagerank(weights=weights, directed=False)
        return [val[vertex_id], self.avg(val)]


class pr_c_w1_d1(Feature):
    def compute(self, g, vertex_id):
        weights = self.get_weights(g)
        val = g.pagerank(weights=weights, directed=False)
        return [val[vertex_id], self.avg(val)]
