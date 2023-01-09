from sat2.lib2 import esxpand_bitcombo

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

    def drop_bit(self, bit=-1):  # if bit == -1: make a clone of self
        if bit not in self.bits:
            return Clause(self.bits.copy(), self.dic.copy())
        bits = self.bits.copy()
        dic = self.dic.copy()
        for b in self.bits:
            if b != bit:
                bits.append(b)
                dic[b] = self.dic[b]
        return Clause(bits, dic)
    
    def sats(self):
        dics = esxpand_bitcombo(self.bits)
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

