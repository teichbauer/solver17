from center import Center
from layer import Layer
from sat2.node2sat import Node2Sat

class PathFinder:
    def __init__(self, branch):
        self.branch = branch
        self.sumbdic = branch.sumbdic
        self.etail = branch.chain[branch.novs[-1]]
        self.sat = branch.sat
        self.path_pool = {}  # {<nov>: [<children-vals>]}
        for nv in branch.novs:
            self.path_pool[nv] = sorted(branch.chain[nv].bgrid.chvset)


    def find2sat_solutions(self):
        nov = 24
        tail = self.branch.chain[nov]
        layer24 = Layer(tail)  # self.tail_chvclauses(tail)
        sats_dic = self.get_cvs_sats(tail)
        x = 1


    def tail_chvclauses(self, tail):
        chv_cldict = {}  # cls keyed by chv
        key_cldict = {}  # cl keyed by key(tail.cvks_dic)

        for chv in tail.bgrid.chvset:
            if len(tail.cvks_dic[chv]) == 0:
                chv_cldict[chv] = None
                continue
            key = tuple(sorted(tail.cvks_dic[chv]))
            if key in key_cldict:
                chv_cldict[chv] = key_cldict[key]
            else:
                clause_dic = {}
                for kn in tail.cvks_dic[chv]:
                    clause_dic[kn] = tail.vk2dic[kn].dic.copy()
                pn = Node2Sat(None, clause_dic)
                pn.split_me()
                key_cldict[key] = pn
                chv_cldict[chv] = key_cldict[key]
        self.chvclauses = chv_cldict

    def get_cvs_sats(self, layer):
        sats_dic = {}
        for chv in layer.chvclauses:
            pass
        #     sat_dic = tail.bgrid.grid_sat(chv)
        #     cl = self.chvclauses[chv]
        #     if cl == None:
        #         sats_dic[chv] = sat_dic
        #         continue            
        #     # cl.split_me()
        #     sats = sats_dic.setdefault(chv,[])
        #     for sat in cl.solution_sats:
        #         ss = sat.copy()
        #         ss.update(sat_dic)
        #         sats.append(ss)
        # return sats_dic


