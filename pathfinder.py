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
        candis = {}
        while True:
            nov = layer.tail.nov + 3
            if nov == Center.maxnov:
                break
            ntail = self.branch.chain[nov]
            cv = 2
            sat = layer.cvsats(cv)
            sat_bits = set(sat)
            obits = sat_bits.intersection(ntail.bdic)
            if len(obits) > 0:
                olayer = Layer(ntail)
                if olayer:
                    for ocv in ntail.bgrid.chvset:
                        osats = olayer.cvsats(ocv)
                        obs = obits.intersection(osats)
                        if len(obs) > 0:
                            res = self.sat_conflict(obs, sat, osats)
                            x = 1
                x = 9
        x = 0

    def sat_conflict(self, obits, sat1, sat2):
        for b in obits:
            if b in sat1 and b in sat2:
                if sat1[b] != sat2[b]:
                    return False
        return True