from center import Center
from pathnode import PathNode

class Cluster(PathNode):
    cluster_dic = {}
    groups = {}

    def __init__(self, name, n2node):
        self.name = name
        self.n2 = n2node
        self.tail1 = n2node.tail
        self.nov = n2node.tail.nov
        bdic = {b:s.copy() for b, s in n2node.bitdic.items()}
        super().__init__(n2node.sat.copy(), bdic, n2node.clauses.copy())
        self.add_sat(n2node.sat_dic(name[1]))
        self.blocker_set = set()

    def clone(self):
        c = Cluster(self.name, self.n2.clone())
        if c.add_sat(self.sat):
            return c
        raise Exception("!!")
    
    def add_n2(self, n2, n2cv):
        if type(self.name) == tuple:
            self.name = [self.name, (n2.tail.nov, n2cv)]
        else:
            self.name.append((n2.tail.nov, n2cv))
        self.tail2 = n2.tail
        sat = n2.sat_dic(n2cv)
        if not self.add_sat(sat):
            return None
        for cl in n2.clauses.values():
            if cl.kname == 'C0102':
                x = 9
            if not self.add_k2(cl):
                return None
        name = tuple(self.name)
        self.bsatbits = self.tail1.bgrid.bitset.union(self.tail2.bgrid.bitset)
        Cluster.cluster_dic[name] = self
        Cluster.groups.setdefault(self.nov, []).append((name,self))
        return self

    def delta_sat(self):
        bits = set(self.sat) - self.bsatbits
        dset = {b: self.sat[b] for b in bits}
        return bits, dset

    def grow(self, lower_tail):
        for cv, cvn2 in lower_tail.cvn2s.items():
            clu = self.clone()
            res = clu.add_n2(cvn2, cv)
        x = 0

    def test_sat(self, tsat):
        tail_nov = None
        for b, v in tsat.items():
            assert(b in self.sat), "tsat not qualified"
            if self.sat[b] != v:
                if b in self.bsatbits:
                    if b in self.tail1.bgrid.bits:
                        bgrid = self.tail1.bgrid
                        tail_nov = self.tail1.nov
                    else:
                        bgrid = self.tail2.bgrid
                        tail_nov = self.tail2.nov
                    return True, (tail_nov, bgrid.bv2cvs(b, self.sat[b]))
        return False, None

