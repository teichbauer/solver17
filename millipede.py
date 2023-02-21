from cvnode2 import PathNode

class Path(PathNode):
    def __init__(self, name, sat, bitdic, clauses):
        self.name = [name]
        super().__init__(sat, bitdic.copy(), clauses.copy())

    def clone(self):
        p = super().clone()
        p.name = self.name
        return p

class Millipede:
    def __init__(self, stail):  # starting-tail - nov:21
        self.tails = [stail]
        self.paths = {}
        for cv in stail.cvks_dic:
            # if not stail.cvn2s[cv].done:
            name = (stail.nov, cv)
            n2 = stail.cvn2s[cv]
            self.paths[name] = Path(
                name, 
                stail.bgrid.cv_sats[cv],
                n2.bitdic, 
                n2.clauses)

    def grow(self, tail):
        npath = {}
        while len(self.paths) > 0:
            k, pth = self.paths.popitem()
            for cv in tail.cvks_dic:
                path = pth.clone()
                path.name.append((tail.nov, cv))
                n2 = tail.cvn2s[cv]
                path.add_sat(n2.sat)
                for kn, cl in n2.clauses.items():
                    path.add_k2(kn, cl.dic)
                npath[path.name] = path
        self.paths = npath




