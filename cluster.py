from center import Center
from pathnode import PathNode

class Cluster(PathNode):
    cluster_dic = {}
    groups = {}

    def __init__(self, name, n2node):
        self.name = name
        self.n2 = n2node
        self.nov = n2node.tail.nov
        bdic = {b:s.copy() for b, s in n2node.bitdic.items()}
        super().__init__(n2node.sat.copy(), bdic, n2node.clauses.copy())
        self.add_sat(n2node.sat_dic(name[1]))
        x = 0

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
        sat = n2.sat_dic(n2cv)
        if not self.add_sat(sat):
            return None
        for cl in n2.clauses.values():
            if cl.kname == 'C0102':
                x = 9
            if not self.add_k2(cl):
                return None
        name = tuple(self.name)
        self.set_bsatbits(n2)
        Cluster.cluster_dic[name] = self
        Cluster.groups.setdefault(self.nov, []).append((name,self))
        return self

    def delta_sat(self):
        bits = set(self.sat) - self.bsatbits
        dset = {b: self.sat[b] for b in bits}
        return bits, dset

    def set_bsatbits(self, lower_n2):
        self.bsatbits = self.n2.tail.bgrid.bitset
        self.bsatbits.update(lower_n2.tail.bgrid.bitset)

    def grow(self, lower_tail):
        for cv, cvn2 in lower_tail.cvn2s.items():
            clu = self.clone()
            res = clu.add_n2(cvn2, cv)
        x = 0    

