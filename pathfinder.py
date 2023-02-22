from center import Center
from millipede import Millipede

class PathFinder:
    def __init__(self, branch):
        self.branch = branch
        self.sumbdic = branch.sumbdic
        self.sat = branch.sat
        end_tail = branch.chain[Center.minnov]  # end-tail
        self.millipede = Millipede(end_tail)


    def find_solutions(self):
        # for cvn2 in self.etail.node2s.values():
        #     self.find_path(self.etail, cvn2)
        tail = self.millipede.etail
        while True:
            nv = tail.nov + 3
            if nv > Center.maxnov: 
                return
            nxt_tail = self.branch.chain[nv]
            self.millipede.grow(nxt_tail)
            tail = nxt_tail
        x = 1
