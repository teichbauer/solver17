from sat2.node2sat import Node2Sat

class Layer:
    def __init__(self, tail):
        self.tail = tail
        self.base_bits = tail.bgrid.bitset
        self.cv_sats = {
            v:tail.bgrid.grid_sat(v) for v in tail.bgrid.chvset
        }
        self.cv_cldict = self.set_cv_2sat(tail)

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
                pn.split_me()
                key_cldict[key] = pn
                chv_cldict[chv] = key_cldict[key]
        return chv_cldict
        

    def cvsats(self, cv):
        sat = self.cv_sats[cv].copy()
        if self.cv_cldict[cv]:
            ss = self.cv_cldict[cv].solution_sats[0]
            sat.update(ss)
        return sat



