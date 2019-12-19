from Features.Feature import *

class ad_d0(Feature):

    def compute(self, g, vertex_id):
        val = g.assortativity_degree(directed=False)
        return val
                
class ad_d1(Feature):

    def compute(self, g, vertex_id):
        val = g.assortativity_degree(directed=True)
        return val
