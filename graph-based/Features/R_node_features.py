from Features.Feature import *
import igraph
import os,sys
import subprocess as sp
      
def extract_R_node_features(g):
    tmp_features = {}
    graphfile = 'tmp/tmp_graph.graphml'
    g.save(graphfile)

    if len(g.vs) <= 1:
        if g.is_directed:
            fn = ["Alpha_Unweighted", "Alpha_Weighted", "Articulation_Point", "Burt_Cstrt_Unweighted", "Burt_Cstrt_Weighted", "Bonacich_Power", "Subgraph_Ctr", "P", "z", "I_int", "I_ext", "H", "D", "P_in", "P_out", "z_in", "z_out", "I_intd_in", "I_intd_out", "I_extd_in", "I_extd_out", "H_in", "H_out", "D_in", "D_out"]
            fnames = [fname for fname in fn]
        else:
            fn = ["Alpha_Unweighted", "Alpha_Weighted", "Articulation_Point", "Burt_Cstrt_Unweighted", "Burt_Cstrt_Weighted", "Bonacich_Power", "Subgraph_Ctr", "P", "z", "I_int", "I_ext", "H", "D"]
            fnames = [fname for fname in fn]
        fnames_a = [fn + "_avg" for fn in fnames]
        for fn in fnames:
            fn = fn.replace('"', '')
            tmp_features[fn] = 0.0
        for fn in fnames_a:
            fn = fn.replace('"', '')
            tmp_features[fn] = 0.0

    try:
        res = sp.check_output(
            ["./Features/node_features.R", graphfile], stderr=sp.STDOUT)
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
        fa = average_col(res, col)
        fn = fn.strip()
        fn = fn.replace('"', '')
        fn = fn.replace('^', 'd_')
        tmp_features[fn] = f
        tmp_features[fn + "_avg"] = fa
    return tmp_features

def average_col(res_array, j):
    values = []
    for i in range(len(res_array)):
        try:
            f = float(res_array[i].split()[j])
        except:
            f = complex(res_array[i].split()[j].replace("i", "j")).real
        values.append(f)
    return sum(values) / len(values)

def compute_feature(g, vertex_id):
    features = extract_R_node_features(g)
    return features

class Alpha_Unweighted(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class Alpha_Unweighted_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class Alpha_Weighted(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class Alpha_Weighted_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class Articulation_Point(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class Articulation_Point_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class Articulation_Point_Nbr(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class Burt_Cstrt_Unweighted(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class Burt_Cstrt_Unweighted_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class Burt_Cstrt_Weighted(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class Burt_Cstrt_Weighted_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class Bonacich_Power(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class Bonacich_Power_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class Subgraph_Ctr(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class Subgraph_Ctr_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class P(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class P_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class z(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class z_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class I_int(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class I_int_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class I_ext(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class I_ext_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class H(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class H_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class D(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class D_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class P_in(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class P_in_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class P_out(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class P_out_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class z_in(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class z_in_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class z_out(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class z_out_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class H_out(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class H_out_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class H_in(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class H_in_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class D_out(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class D_out_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class D_in(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class D_in_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class I_intd_in(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class I_intd_in_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class I_intd_out(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class I_intd_out_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class I_extd_in(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class I_extd_in_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class I_extd_out(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)

class I_extd_out_avg(Feature):
    def compute(self, g, vertex_id):
        return compute_feature(g, vertex_id)