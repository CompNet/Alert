from Features.Feature import *
import igraph
      
class cluster_strong(Feature):
    def compute(self, g, vertex_id):
        val = g.clusters(mode=igraph.STRONG).cluster_graph()
        return len(val.vs)

class cluster_weak(Feature):
    def compute(self, g, vertex_id):
        val = g.clusters(mode=igraph.WEAK).cluster_graph()
        return len(val.vs)