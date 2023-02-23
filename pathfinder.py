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
                for b, v in cvn2.sat.items():
                    nv = nov -3
                    while nv >= Center.minnov:
                        if b in Center.headbits[nv]:
                            t = self.branch.chain[nv]
                            cvs = t.bgrid.bv2cvs(b,v)
                            for cv in cvs:
                                cvn2.lower_blocks.add((t.nov, cv))
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
