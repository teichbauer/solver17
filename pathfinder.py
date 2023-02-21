from center import Center
from layer import Layer
from millipede import Millipede

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
        # for cvn2 in self.etail.node2s.values():
        #     self.find_path(self.etail, cvn2)
        tail = self.etail
        mil = Millipede(self.etail)
        while True:
            nv = tail.nov + 3
            if nv > Center.maxnov: return
            ntail = self.branch.chain[nv]
            mil.grow(ntail)
            tail = ntail
        x = 1

    def find_path(self, 
                  ctail,  # current/starting-tail
                  cvn2):  # cvnode2 looping thru ctail.node2s
        nv = ctail.nov + 3
        if nv > Center.maxnov: return
        ntail = self.branch.chain[nv]
        allbits = set(ntail.bdic)
        for cv in cvn2.cvs:
            cvsat = cvn2.sat_dic(cv)
            bs = allbits.intersection(cvsat)
            if len(bs) == 0:
                continue
            for b in bs:
                x = 0
        x = 0

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