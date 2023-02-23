from sat2.clause import Clause
from sat2.lib2 import output_dic, output_clause, expand_wildcard
import os

class Node2Sat:
    # klauses: [(C2, C3), (¬C3, C4), (C2, C4), (¬C1, ¬C2), (¬C3, C1)] =>
    # C3 -> 2:0, ¬C2 -> 1:1
    # [{1:0,2:0}, {2:1, 3:0}, {1:0, 3:0}, {0:1, 1:1}, {2:1, 0:0}]
    
    def __init__(self, parent,  # where this node splitted from. On root: None
                klauses,        # set of 2sat clauses ({<name>:{1:0, 3:1},..})
                sats={}):       # for root {}
                # sats can be 
                # 1. None: split-sat conflict itself: this node is a stopper
                # 2. sat resulted from split
        self.bitdic = {}  # {bit: set(name1, name2,..)}        
        self.parent = parent
        # child node first clone sat from parent
        if parent:
            self.sats = parent.sats.copy() 
            self.solution_sats = parent.solution_sats.copy()
        else:
            self.solution_sats = []
            self.sats = {}
        if parent:
            # add the given sats to the sat cloned from parent.
            # this may have conflict: results in False, causing stop = True
            self.conflict = sats == None or (not self.add_sats(sats))
            if self.conflict:
                self.solution_sats = None
                return
        if len(klauses) == 0:
            self.done = True
            if not self.conflict:
                self.solution_sats.append(self.fill_wbits(self.sats))
            return
        if len(klauses) == 1:
            name, dic = tuple(klauses.items())[0]  # klauses has only 1 (name,dic)
            cl = Clause(name, dic)
            slst = cl.sats()
            for s in slst:
                sat = self.sats.copy()
                sat.update(s)
                self.solution_sats.append(self.fill_wbits(sat))
            self.bitdic = {bit: [name] for bit in cl.bits}
            self.done = True
            return
        self.done = False
        self.clauses = {}
        
        for name, dic in klauses.items():
            for bit in dic:
                self.bitdic.setdefault(bit,set()).add(name)
            self.clauses[name] = Clause(name, dic)
        x = 1
    
    def fill_wbits(self, sat):
        # any bit b in self.bitdic not in sat, sat['wbs'].append(b)
        wbits = set(self.bitdic) - set(sat)
        if len(wbits) > 0:
            sat.update({'wbs': wbits})
        return sat
            
    def add_sats(self, sats):
        # if sats has a conflict with self.sats (same bit, diff bit-value)
        # return False; otherwise fill sats into self.sats, return True
        # --------------------------------------------------------------
        for bit, bv in sats.items():
            if bit in self.sats:
                if bv != self.sats[bit]:
                    return False
            else:
                self.sats[bit] = bv
        return True

    def remove_clause(self, cl):
        self.clauses.pop(cl.kname)
        for b in cl.bits:
            self.bitdic[b].remove(cl.kname)

    def add_clause(self, k2): # add a 2-sat clause (sat2.clause/Clause)
        obits = set(self.sats).intersection(k2.bits)
        len_obits = len(obits)
        if len_obits == 2:
            self.conflict = not k2.verify(self.sats)
            # if at lest one b in vk.bits: 
            #    self.sats[b] != vk.dic[b]
            # this vk can be omitted. - do not add it
        elif len_obits == 1:
            b = obits.pop()
            ob = k2.other_bit(b)
            if k2.dic[b] == self.sats[b]:
                return self.add_sats({ob: k2.dic[ob]})
            # if k2.dic[b] != self.sats[b], k2 not added
        else: # k2 has no bit in self.sats
            obits = set(self.bitdic).intersection(k2.bits)
            len_obits = len(obits)
            if len_obits < 2:
                for b in obits:
                    self.bitdic.setdefault(b,[]).append(k2.kname)
            else: # len_obits == 2
                for b in obits:
                    for kn in self.bitdic[b]:
                        if self.clauses[kn].bits == k2.bits:
                            res = self.clauses[kn].evaluate_overlap(k2)
                            if type(res) == type({}): # 
                                self.remove_clause(self.clauses[kn])
                                if not self.add_sats(res):
                                    self.conflict = True
                            elif res == 1: # k2 to be added
                                for b in obits:
                                    self.bitdic.setdefault(b,[]).append(k2.kname)
                            else:          # k2 not added
                                pass




        

    def maxpopular_bit(self):
        ''' find the bit where most vks sitting on '''
        bit = -1
        siz = 0
        for b, names in self.bitdic.items():
            leng = len(names)
            if  leng > siz:
                bit = b
                siz = leng
        return bit

    def include_wildbits(self):
        '''
        for every missing bit in sat: bit(s) = (bits in map) - (sat-bits), 
        set  sat[bit] = 2
        '''
        allbits = set(self.bitdic)
        leng = len(allbits)
        solsats = []
        for sat in self.solution_sats:
            if len(sat) == leng:
                solsats.append(sat)
            else:
                bits = allbits - set(sat)
                s = sat.copy()
                for b in bits:
                    s[b] = 2
                solsats.append(s)
        self.solution_sats = solsats

    def split_me(self):
        if self.done:
            return
        sbit = self.maxpopular_bit()  # bit with the most number of clauses
        pn0_clauses = {}
        pn0_sats = {sbit:0}
        pn1_clauses = {}
        pn1_sats = {sbit:1}
        for kn, k in self.clauses.items():
            if sbit in k.bits:
                obit = k.other_bit(sbit)
                obv = int(not k.dic[obit])
                if k.dic[sbit] == 0:
                    if pn0_sats:
                        if obit in pn0_sats:
                            if obv != pn0_sats[obit]:
                                pn0_sats = None
                        else:
                            pn0_sats[obit] = obv
                else:
                    if pn1_sats:
                        if obit in pn1_sats:
                            if obv != pn1_sats[obit]:
                                pn1_sats = None
                        else:
                            pn1_sats[obit] = obv
            else:
                # klause not touched, put it into pn0 and pn1
                pn0_clauses[kn] = k.dic.copy()
                pn1_clauses[kn] = k.dic.copy()
        child0 = Node2Sat(self, pn0_clauses, pn0_sats)
        child1 = Node2Sat(self, pn1_clauses, pn1_sats)
        self.conflict = child0.conflict and child1.conflict
        if self.conflict: return
        
        self.children = (child0, child1)
        for ch in self.children:
            if ch.conflict or ch.done:
                continue
            ch.split_me()

    def verify(self):
        if len(self.solution_sats) == 0: 
            print("There exists no sat")
            return
        expanded_sats = expand_wildcard(self.solution_sats)
        for i in range(len(expanded_sats)):
            sat = expanded_sats[i]
            print(f"\nVerifying sat{i}: {output_dic(sat)}")

            for cl in self.clauses.values():
                res = cl.verify(sat)
                if not res:
                    print(f" {output_clause(cl)} - not verified.")
                else:
                    print(f" {output_clause(cl)} - verified.")
