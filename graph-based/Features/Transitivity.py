from Features.Feature import *

class trans_loc_d0_w0(Feature):
    def compute(self, g, vertex_id):
        val = g.transitivity_local_undirected(vertices=[vertex_id], weights=None, mode="zero")
        return val[0]
                
class trans_loc_d0_w1(Feature):
    def compute(self, g, vertex_id):
        weights = self.get_weights(g)
        val = g.transitivity_local_undirected(vertices=[vertex_id], weights=weights, mode="zero")
        return val[0]

class trans_avgloc_d0(Feature):
    def compute(self, g, vertex_id):
        val = g.transitivity_avglocal_undirected(mode="zero")
        return val

class trans_d0(Feature):
    def compute(self, g, vertex_id):
        val = g.transitivity_undirected(mode="zero")
        return val