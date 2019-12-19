from Features.Feature import *
import igraph
      
class radius_in(Feature):
    def compute(self, g, vertex_id):
        val = g.radius(mode=igraph.IN)
        return val

class radius_out(Feature):
    def compute(self, g, vertex_id):
        val = g.radius(mode=igraph.OUT)
        return val

class radius_all(Feature):
    def compute(self, g, vertex_id):
        val = g.radius(mode=igraph.ALL)
        return val