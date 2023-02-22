from pathnode import PathNode

class CVNode2(PathNode):
    def __init__(self, tail, cv):
        super().__init__()
        self.tail = tail
        self.cvs = set([cv])
        self.done = False  # False, True, "conflict"

    def add_sat(self, sat):
        '''
        a sat bit:value pair like {5:1} means: the value on bit 5 must be 1,
        othewise this will make F=()^()^.. fail. So, if a k2 has bit 5,
        and: a): bv is 1 -> this ke can eliminate bit-5, k2 becomes sat-bit;
        b), bv is 0 -> this k2 can be eliminated, the 5:1 makes it so.
        '''
        res = super().add_sat(sat)
        if not res:
            self.done = 'conflict'

    def sat_dic(self, cv):
        sdic = self.sat.copy()
        sdic.update(self.tail.bgrid.cv_sats[cv])
        return sdic


