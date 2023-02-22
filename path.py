from pathnode import PathNode

class Path(PathNode):
    def __init__(self, name, sat, bitdic, clauses):
        self.name = name
        # from super/PathNode:
        #   .sat
        #   .bitdic
        #   .clauses
        # -------------------------
        super().__init__(sat.copy(), bitdic.copy(), clauses.copy())

    # def get_leg(self, name):
    #     return self.sat, self.bitdic, self.clauses

    def clone(self):
        p = Path(self.name.copy(), self.sat, self.bitdic, self.clauses)
        return p

    def add_n2(self, n2, n2cv):
        sat = n2.sat_dic(n2cv)
        if not self.add_sat(sat):
            return False
        else:
            for kn, cl in n2.clauses.items():
                if not self.add_k2(kn, cl.dic):
                    return False
            return True
