from center import Center
from pathketten import PathKetten
from levelpath import LevelPath

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
        # for nov, tail in self.branch.chain.items():
        #     tail.generate_2sats()
        tail = self.branch.chain[30]
        tail.generate_2sats()
        x = 1
