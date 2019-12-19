from Features.Feature import *

class nV(Feature):

    def compute(self, g, vertex_id):
        val = len(g.vs)
        return val
                
