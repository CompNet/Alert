from Features.Feature import *
import igraph
import os,sys
import subprocess as sp
      
def extract_R_graph_features(g):
    tmp_features = {}
    graphfile = 'tmp/tmp_graph.graphml'
    g.save(graphfile)
        
    if len(g.vs) <= 1:
        tmp_features["Articulation_Point_Nbr"] = 0.0
        tmp_features["Reciprocity"] = 0.0

    try:
        res = sp.check_output(
            ["./Features/graph_features.R", graphfile], stderr=sp.STDOUT)
    except sp.CalledProcessError as exc:
        print("Status : FAIL", exc.returncode, exc.output)
        sys.exit(1)
    res = res.decode("utf-8")
    res = res.split("\n")
    headers = res[0].split()
    res = res[1:-1]
    for fn in headers:
        col = headers.index(fn)
        try:
            f = float(res[0].split()[col])
        except:
            try:
                f = complex(res[0].split()[col].replace("i", "j")).real
            except:
                print ("Vertex Number:", len(g.vs))
                print (res)
                sys.exit(1)
        fn = fn.strip()
        fn = fn.replace('"', '')
        tmp_features[fn] = f
    return tmp_features

def compute_feature(g):
    features = extract_R_graph_features(g)
    return features

class Articulation_Point_Nbr(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g)

class Reciprocity(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g)