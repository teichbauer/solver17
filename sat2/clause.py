from sat2.lib2 import expand_bitcombo

class Clause:
    def __init__(self, name, dic):
        self.name = name
        self.bits = sorted(dic)
        self.dic = dic

    def other_bit(self, b):
        if b in self.bits:
            bits = self.bits[:]
            bits.remove(b)
            return bits[0]
        return None

    def clone(self):  # if bit == -1: make a clone of self
        return Clause(self.bits.copy(), self.dic.copy())

    def evaluate_overlap(self, cl):
        ''' Only for the case of self.bits == cl.bits, if
        1. self.dic == cl.dic - return 0
        2. for 1 bit b self.dic[b] == cl.dic[b]  
            - return a sat{b: self.dic[b]}
        3. self.dic[b0] != cl.dic[b0] and self.dic[b1] != cl/dic[b1]
            - return 1
        '''
        assert(self.bits == cl.bits), f"{self.name} and {cl.name} not overlap."
        b0, b1 = self.bits
        if self.dic[b0] == cl.dic[b0]:
            if self.dic[b1] == cl.dic[b1]:
                return 0
            #  self.dic[b0] == cl.dic[b0] and self.dic[b1] != cl.dic[b1]
            return {b0: self.dic[b0]}
        elif self.dic[b1] == cl.dic[b1]:
            return {b1: self.dic[b1]}
        return 1
        
    
    def sats(self):
        dics = expand_bitcombo(self.bits)
        sats = []
        for d in dics:
            if d != self.dic:
                sats.append(d)
        return sats


    def verify(self, sats):  # sats must not have a single 2 among the values
        if set(self.bits).issubset(set(sats)):
            b0, b1 = self.bits
            if self.dic[b0] == sats[b0] and self.dic[b1] == sats[b1]:
                print(f"{self.name} = hit(False)")
                return False
            return True
        raise Exception(f"{self.name} not in sat")

