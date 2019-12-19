from Features.Feature import *

class nE(Feature):
    def compute(self, g, vertex_id):
        val = len(g.es)
        return val
                
