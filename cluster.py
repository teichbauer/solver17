from center import Center
from pathnode import PathNode
from blocker import Blocker

class Cluster(PathNode):
    cluster_dic = {}
    groups = {}

    def __init__(self, name, n2node):
        self.name = name
        if type(n2node) == Cluster:  # n2node is a cluster clone it
            self.n2 = n2node.n2
            self.tail1 = n2node.tail1
            self.tail2 = n2node.tail2
            self.sat = {b: v for b, v in n2node.sat.items()}
            self.bitdic = {b:s.copy() for b, s in n2node.bitdic.items() }
            self.clauses = n2node.clauses.copy()
            self.bsatbits = n2node.bsatbits.copy()
            self.block = n2node.block.clone()
            return # cloning done
        # type(n2node) == CVNode2
        self.n2 = n2node
        self.tail1 = n2node.tail
        self.nov = n2node.tail.nov
        bdic = {b:s.copy() for b, s in n2node.bitdic.items()}
        super().__init__(n2node.sat.copy(), bdic, n2node.clauses.copy())
        self.add_sat(n2node.sat_dic(name[1]))
        self.block = Blocker(self)

    def clone(self):  # only for grown cluster (with 2 tails: tail1, tail2)
        clu = Cluster(self.name.copy(), self)
        return clu
    
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
            # if cl.kname == 'C0102':
            #     x = 9
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
            clu = Cluster(self.name, self.n2.clone())
            if clu.add_sat(self.sat):
                clu.add_n2(cvn2, cv)
        x = 0

    def test_sat(self, tsat):
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
                return True, None
        return False, None

    def merge_cluster(self, cl):
        c = self.clone()
        c.name += cl.name
        if not c.block.update(cl.block):
            return None
        if c.add_sat(cl.sat):
            old_sat = c.sat.copy()
            for clause in cl.clauses.values():
                if not c.add_k2(clause):
                    return None
            lower_nov = cl.nov - 6
            new_bits = set(c.sat) - set(old_sat)
            # in case there are new-sat(bits), see if lower tails' head on them
            if len(new_bits) > 0:
                while lower_nov >= Center.minnov:
                    bgrd = Center.snodes[lower_nov].tail.bgrid
                    bs = new_bits.intersection(bgrd.bitset) # tail bit overlaps
                    for b in bs:
                        v = c.sat[b]
                        blck_cvs = bgrd.chvset.difference(bgrd.bv2cvs(b, v))
                        c.block.add_block((lower_nov, blck_cvs))
                    lower_nov -= 3
            return (c, lower_nov)
        return None
