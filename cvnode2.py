from sat2.clause import Clause

class CVNode2:
    def __init__(self, tail, cv):
        self.tail = tail
        self.cvs = set([cv])
        self.sat = {}
        self.bitdic = {}   # {<bit>:[kname,...],..}
        self.clauses = {}  # {<kname>: k2-clause,...}
        self.done = False  # False, True, "conflict"

    def add_k2(self, kname, k2dic):
        dic = k2dic.copy()
        cl = Clause(kname, dic)
        for bit in dic:
            if bit in self.bitdic:
                for kn in self.bitdic[bit]:
                    clx = self.clauses[kn]
                    if clx.bits == cl.bits:
                        ev = cl.evaluate_overlap
                        if ev == 0:  # k2dic douplicates - don't add
                            return   # just return
                        self.sat.update(ev)
                        return
            self.bitdic.setdefault(bit, set()).add(kname)
        self.clauses[kname] = cl

    def add_sat(self, sat):
        '''
        a sat bit:value pair like {5:1} means: the value on bit 5 must be 1,
        othewise this will make F=()^()^.. fail. So, if a k2 has bit 5,
        and: a): bv is 1 -> this ke can eliminate bit-5, k2 becomes sat-bit;
        b), bv is 0 -> this k2 can be eliminated, the 5:1 makes it so.
        '''
        while len(sat) > 0:
            sbit, sval = sat.popitem()
            if sbit in self.sat:
                if self.sat[sbit] == sval:
                    continue
                else:
                    self.done = "conflict"
                    return 
            else:
                self.sat[sbit] = sval
            new_sat = {}
            if sbit in self.bitdic:
                while len(self.bitdic[sbit]) > 0:
                    kn = self.bitdic[sbit].pop()
                    cl = self.clauses.pop(kn)  # cl is no more in self.clauses
                    obit = cl.other_bit(sbit)

                    # clear cl's obit from bitdic
                    self.bitdic[obit].pop(kn)
                    if len(self.bitdic[obit]) == 0:
                        del self.bitdic[obit]

                    if cl.dic[sbit] == sval:
                        new_sat[obit] = int(not cl.dic[obit])
                    else:
                        pass

                del self.bitdic[sbit]
            self.add_sat(new_sat)



