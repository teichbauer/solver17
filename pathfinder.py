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

    def collect_ocvs(self, bits, tail):
        '''
        return a list of cvs, each of it contains some bit from bits
        '''
        cvs_vks = {}
        for bit in bits:
            for kn in tail.bdic[bit]:
                vk = tail.vk2dic[kn]
                for cv in vk.cvs:
                    cvs_vks.setdefault(cv,[]).append(vk)
        return cvs_vks


    def find_candidates(self, layer):
        for cv in layer.cv_sats:
            sat, bits = layer.sat_and_bits(cv)
            while True:
                nov = layer.tail.nov + 3
                if nov == Center.maxnov:
                    break
                ntail = self.branch.chain[nov]
                obits = bits.intersection(ntail.bdic)
                if len(obits) > 0:
                    ocvs_vks = self.collect_ocvs(obits, ntail)
                    x = 9
        x = 0

    def sat_conflict(self, obits, sat1, sat2):
        for b in obits:
            if b in sat1 and b in sat2:
                if sat1[b] != sat2[b]:
                    return False
        return True