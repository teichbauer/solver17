from clause import Clause
from lib2 import output_dic, output_clause, expand_wildcard
import os

class PathNode:
    # klauses: [(C2, C3), (¬C3, C4), (C2, C4), (¬C1, ¬C2), (¬C3, C1)] =>
    # C3 -> 2:0, ¬C2 -> 1:1
    # [{1:0,2:0}, {2:1, 3:0}, {1:0, 3:0}, {0:1, 1:1}, {2:1, 0:0}]
    solution_sats = []
    def __init__(self, parent,  # where this node splitted from. On root: None
                klauses,        # set of 2sat clauses ({<name>:{1:0, 3:1},..})
                sats={}):       # for root {}
                # sats can be 
                # 1. None: split-sat conflict itself: this node is a stopper
                # 2. sat resulted from split
        self.parent = parent
        # child node first clone sat from parent
        self.sats = parent.sats.copy() if parent else {}
        if parent:
            # add the given sats to the sat cloned from parent.
            # this may have conflict: results in False, causing stop = True
            self.stop = sats == None or (not self.add_sats(sats))
            if self.stop:
                return
        if len(klauses) == 0:
            self.done = True
            if not self.stop:
                self.solution_sats.append(self.sats)
            return
        self.done = False
        self.clauses = {}
        self.bitkdic = {}  # {bit: set(name1, name2,..)}

        for name, dic in klauses.items():
            for bit in dic:
                self.bitkdic.setdefault(bit,set()).add(name)
            self.clauses[name] = Clause(name, dic)
        x = 1
    
    def output_clauses(self):
        print(f"Clauses:")
        for cl in self.clauses.values():
            print(output_clause(cl))
            
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

    def maxpopular_bit(self):
        bit = -1
        siz = 0
        for b, names in self.bitkdic.items():
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
        allbits = set(self.bitkdic)
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
        child0 = PathNode(self, pn0_clauses, pn0_sats)
        child1 = PathNode(self, pn1_clauses, pn1_sats)
        
        self.children = (child0, child1)
        for ch in self.children:
            if ch.stop or ch.done:
                continue
            ch.split_me()
