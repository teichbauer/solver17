from sat2.clause import Clause

class PathNode:
    def __init__(self, sat=None, bitdic=None, clauses= None):
        self.sat = sat if sat else {}
        self.bitdic = bitdic if bitdic else {}     # {<bit>:set{kname,...},..}
        self.clauses = clauses if clauses else {}  # {<kname>: k2-clause,...}

    def clone(self):
        p = PathNode()
        p.bitdic = self.bitdic.copy()
        p.clauses = self.clauses.copy()
        p.sat = self.sat.copy()
        return p

    def add_k2(self, vk):  # vk can be clause, or vklause
        dic = vk.dic.copy()
        dicbits = set(dic)
        touch = dicbits.intersection(self.sat)
        if len(touch) > 0:
            b = touch.pop()
            if dic[b] == self.sat[b]:
                dic.pop(b)
                sbit, sval = dic.popitem()
                return self.add_sat({sbit: int(not sval)})
            else:
                return True
        touch = dicbits.intersection(self.bitdic)
        cl = Clause(vk.kname, dic)
        if len(touch) == 0:
            for bit in dicbits:
                self.bitdic.setdefault(bit, set()).add(vk.kname)
        else:
            for bit in dicbits:
                if bit in self.bitdic:
                    kns = self.bitdic[bit].copy()
                    for kn in kns:
                        clx = self.clauses[kn]
                        if clx.bits == cl.bits:
                            ev = cl.evaluate_overlap(clx)
                            if ev == 0:  # k2dic douplicates - don't add
                                return   # just return
                            if ev != 1:  # ev is a new sat
                                b, v = ev.popitem()
                                if not self.add_sat({b: int(not v)}):
                                    return False
                            self.sat.update(ev)
                            return True
                self.bitdic.setdefault(bit, set()).add(vk.kname)
        self.clauses[vk.kname] = cl
        return True

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
                    return False # self.done = "conflict"
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
            res = self.add_sat(new_sat)
            if not res:
                return False
        return True
