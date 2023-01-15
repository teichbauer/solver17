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
        self.find_candidates(layer24)
        x = 1


    def find_candidates(self, layer):
        sats_dic = layer.cvsats(2)
        sbits = set(sats_dic)
        while True:
            nov = layer.tail.nov + 3
            if nov == Center.maxnov:
                break
            ntail = self.branch.chain[nov]
            overbits = sbits.intersection(ntail.bdic)
            if len(overbits)> 0:
                x = 9
        x = 0
        # for cv in layer.cv_2sats:
        #     sats_dic = layer.cvsats(cv)


