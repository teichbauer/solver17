from path import Path
stops = set([
    ((21,4),(24,0),(27,1),(30,3)),
    ((21,4),(24,0),(27,1),(30,5)),
    ((21,4),(24,0),(27,1),(30,7)),
    ((21,4),(24,0),(27,2),(30,3)),
    ((21,4),(24,0),(27,2),(30,5)),
    ((21,4),(24,0),(27,2),(30,7)),
    ((21,4),(24,0),(27,3),(30,3)),
    ((21,4),(24,0),(27,3),(30,5)),
    ((21,4),(24,0),(27,3),(30,7)),
    ((21,4),(24,0),(27,4),(30,3)),
    ((21,4),(24,0),(27,4),(30,5)),
    ((21,4),(24,0),(27,4),(30,7)),
    ((21,4),(24,0),(27,5),(30,3)),
    ((21,4),(24,0),(27,5),(30,5)),
    ((21,4),(24,0),(27,5),(30,7)),
])


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

    def grow(self, higher_tail):
        npath = {}
        for pth in self.paths.values():
            sat, bdic, cls = pth.sat, pth.bitdic, pth.clauses
            for kcv, xn2 in higher_tail.node2s.items():
                for cv in xn2.cvs:
                    if type(pth.name[0]) == tuple:
                        name = pth.name + ((higher_tail.nov, cv),)
                    else:
                        name = (pth.name,(higher_tail.nov, cv))
                    leng = len(name)
                    if leng == 4:
                        if name in stops:
                            x = 100
                    p = Path(name, sat, bdic, cls)
                    res = p.add_n2(xn2, cv)
                    if not res:
                        continue
                    npath[p.name] = p
        self.paths = npath




