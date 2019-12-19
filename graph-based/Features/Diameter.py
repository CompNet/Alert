from Features.Feature import *
      
class diameter_d0_w0(Feature):
    def compute(self, g, vertex_id):
        val = g.diameter(directed=False, weights=None)
        return val

class diameter_d0_w1(Feature):
    def compute(self, g, vertex_id):
        weights = self.get_weights(g)
        val = g.diameter(directed=False, weights=weights)
        return val

class diameter_d1_w0(Feature):
    def compute(self, g, vertex_id):
        val = g.diameter(directed=True, weights=None)
        return val

class diameter_d1_w1(Feature):
    def compute(self, g, vertex_id):
        weights = self.get_weights(g)
        val = g.diameter(directed=True, weights=weights)
        return val