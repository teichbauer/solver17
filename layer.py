from sat2.node2sat import Node2Sat

class Layer:
    def __init__(self, tail):
        self.tail = tail
        self.cv_sats = {
            v:tail.bgrid.grid_sat(v) for v in tail.bgrid.chvset
        }
        self.tail_chvclauses(tail)

    def tail_chvclauses(self, tail):
        chv_cldict = {}  # cls keyed by chv
        key_cldict = {}  # cl keyed by key(tail.cvks_dic)

        for chv in tail.bgrid.chvset:
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
        self.chvclauses = chv_cldict    