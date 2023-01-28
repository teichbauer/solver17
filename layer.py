from sat2.node2sat import Node2Sat

class Layer:
    def __init__(self, tail):
        self.tail = tail
        self.base_bits = tail.bgrid.bitset
        self.cv_sats = {
            v:tail.bgrid.grid_sat(v) for v in tail.bgrid.chvset
        }
        # self.cv_cldict = self.set_cv_2sat(tail)
        self.set_node2s(tail)

    def set_cv_2sat(self, tail):
        chv_cldict = {}  # cls keyed by chv
        key_cldict = {}  # cl keyed by key(tail.cvks_dic)

        for chv in self.cv_sats:
            if len(tail.cvks_dic[chv]) == 0:
                chv_cldict[chv] = None
                continue
            key = tuple(sorted(tail.cvks_dic[chv]))
            if key in key_cldict:
                chv_cldict[chv] = key_cldict[key]
            else:
                clause_dic = {}
                for kn in tail.cvks_dic[chv]:
                    clause_dic[kn] = tail.vk2dic[kn].dic.copy()
                pn = Node2Sat(None, clause_dic)
                # pn.split_me()
                key_cldict[key] = pn
                chv_cldict[chv] = key_cldict[key]
        return chv_cldict
        
    def set_node2s(self, tail):
        self.node2s = {}    # {<cv>:<node2>}
        key_n2s = {}        # key is tuple(kns) for a cv. some vs have the same
        for cv in self.cv_sats:
            if len(tail.cvks_dic[cv]) == 0:
                self.node2s[cv] = None
                continue
            key = tuple(sorted(tail.cvks_dic[cv]))
            if key in key_n2s:
                self.node2s[cv] = key_n2s[key]
            else:
                clause_dic = {}
                for kn in tail.cvks_dic[cv]:
                    clause_dic[kn] = tail.vk2dic[kn].dic.copy()
                pn = Node2Sat(None, clause_dic)
                key_n2s[key] = pn
                self.node2s[cv] = pn

    def sat_and_bits(self, cv):
        # get sat and bits.
        # sat: cv-grid-sat + node2(cv).sat
        # bits: sat-bit + node2.bidic-bits
        sat = self.cv_sats[cv].copy()
        if self.node2s[cv]:
            sat.update(self.node2s[cv].sats)
        bits = set(sat)
        # bits.update(self.node2s[cv].bitdic)
        return sat, bits

    def cvsats(self, cv):
        sat = self.cv_sats[cv].copy()
        if self.cv_cldict[cv]:
            ss = self.cv_cldict[cv].solution_sats[0]
            sat.update(ss)
        return sat



