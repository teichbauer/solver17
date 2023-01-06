from vk2pkg import Vk2Package

class PathKetten:
    def __init__(self, path_pool, start_tail):
        self.path_pool = path_pool
        self.curr_nv = start_tail.nov
        self.curr_cv = path_pool[self.curr_nv].pop(0)
        self.path = [(self.curr_nv, self.curr_cv)]
        # pkg = Vk2Package(self)
        # self.pkg_dic = {self.path[-1]: pkg}  
        # for kn in start_tail.cvks_dic[self.curr_cv]:
        #     vk = start_tail.vk2dic[kn]
        #     pkg.vkdic[kn] = vk
        #     for b, v in vk.dic.items():
        #         pkg.bdic.setdefault(b, set([])).add(kn)

    def walkup(self, nxtail):
        return True

    def grow(self, nxt_tail): # current tail grow to next_tail
        nxt_nv = nxt_tail.nov
        nxt_cv = self.path_pool[nxt_nv].pop(0)
        new_pkg = Vk2Package(self, self.pkg_dic[self.path[-1]])
        for bit, d in nxt_tail.blbmgr.block_bv_dic.items():
            for bv, cvs in d.items():
                if nxt_cv in cvs:
                    new_pkg.add_block(bit, bv)
        blocks = self.blocks_from_cbdic(nxt_cv, nxt_tail.blbmgr.cbdic)
        for bl_bit, bl_va in blocks:
            if not new_pkg.add_block(bl_bit, bl_va):
                return False
        for kn in nxt_tail.cvks_dic[nxt_cv]:
            vk = nxt_tail.vk2dic[kn]
            if not new_pkg.add_vk(vk):
                return False
        if new_pkg.finalize():
            x = 0
        p = (nxt_nv, nxt_cv)
        self.path.append(p)
        self.pkg_dic[p] = new_pkg  # ?? self.pkg_dic[self.path] = new_pkg ??
        return self.path

    def blocks_from_cbdic(self, nxt_cv, tail_cbdic):
        blcks = []
        for pnode in self.path:
            pnode_nv, pnode_cv = pnode
            if pnode_nv in tail_cbdic:
                for kn, tp in tail_cbdic[pnode_nv].items():
                    # tp:[(nv-cvs),(nxt-cv),(blck-bit, blck-val)]
                    if pnode_cv in tp[0] and nxt_cv in tp[1]:
                        blck_bit, blck_val = tp[2]
                        blcks.append((blck_bit, blck_val))
        return blcks


