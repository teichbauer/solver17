from path import Path

class Millipede:
    def __init__(self, end_tail):
        self.etail = end_tail
        self.paths = {}
        self.setup()

    def setup(self):
        for cv in self.etail.cvks_dic:
            # if not stail.cvn2s[cv].done:
            name = (self.etail.nov, cv)
            n2 = self.etail.cvn2s[cv]
            self.paths[name] = Path(
                name,
                n2.sat_dic(cv),
                n2.bitdic, 
                n2.clauses)
            x = 0
        x = 1

    def grow(self, tail):
        npath = {}
        for pth in self.paths.values():
            sat, bdic, cls = pth.sat, pth.bitdic, pth.clauses
            for xn2 in tail.node2s.values():
                for cv in xn2.cvs:
                    p = Path((pth.name,(tail.nov, cv)), sat, bdic, cls)
                    res = p.add_n2(xn2, cv)
                    if not res:
                        continue
                    npath[p.name] = p
        self.paths = npath




