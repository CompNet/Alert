from Features.Feature import *
import igraph
      
class clique_number(Feature):
    def compute(self, g, vertex_id):
        if not g.is_directed:
            val = g.clique_number()
        else:
            gr = g.as_undirected()
            val = gr.clique_number()
        return val