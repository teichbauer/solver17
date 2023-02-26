from center import Center
from millipede import Millipede

class PathFinder:
    def __init__(self, branch):
        self.branch = branch
        self.sumbdic = branch.sumbdic
        self.sat = branch.sat
        end_tail = branch.chain[Center.minnov]  # end-tail
        self.millipede = Millipede(end_tail)
        self.downward_blocker()

    def downward_blocker(self):
        for nov in self.branch.novs:
            tail = self.branch.chain[nov]
            for cvn2 in tail.node2s.values():
                nv = nov -3
                while nv >= Center.minnov:
                    t = self.branch.chain[nv]
                    head = t.bgrid.bitset
                    for b, v in cvn2.sat.items():
                        if b in head:
                            cvs = t.bgrid.bv2cvs(b,int(not v))
                            for cv in cvs:
                                cvn2.lower_blocks.add((t.nov, cv))
                    # heads of lower tail.cvn2s piercing into cvn2.bitdic
                    xbits = head.intersection(cvn2.bitdic)
                    if xbits:
                        for tcv, tcvn2 in t.cvn2s.items():
                            xcvn2 = cvn2.clone()
                            sat = t.bgrid.grid_sat(tcv).copy()
                            if not xcvn2.add_sat(sat):
                                x = 0
                            else:
                                x = 0
                            if xcvn2.add_cvn2(tcvn2):
                                x = 8
                            else:
                                x = 0
                        x = 9
                    nv = nv - 3

                x = 0
            x = 9
        x = 9

    def find_solutions(self):
        # for cvn2 in self.etail.node2s.values():
        #     self.find_path(self.etail, cvn2)
        nov = self.millipede.etail.nov
        while True:
            tail = self.branch.chain[nov+3]
            self.millipede.grow(tail)
            if tail.nov == Center.maxnov: 
                return
            nov = tail.nov
        x = 1
