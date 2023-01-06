from blbmgr import BlbManager
from center import Center
from branch import Branch
from blockchecker import BlockChecker


def merge_vkpair(vk2a, vk2b): # vk2a and vk2b must have common-cvs
    #         vk2a         vk2b                 return
    #---------------------------------------------------
    # dic1:{ 11:0, 21:1}, dic2:{11:1, 21:1} -> {(21,1)}
    # dic1:{ 11:0, 21:1}, dic2:{11:0, 21:0} -> {(11,0)}
    # dic1:{ 11:0, 21:1}, dic2:{11:1, 21:0} -> {}
    # -------------------------------------
    # this not possible to gwet to here:
    # dic1:{ 11:0, 21:1}, dic2:{11:0, 21:1} -> {(11,0),(21,1)} 
    s1 = set(tuple(vk2a.dic.items()))
    s2 = set(tuple(vk2b.dic.items()))
    s = s1.intersection(s2)
    if len(s) == 0:
        return None
    if len(s) == 2:
        raise Exception(f'{vk2a.kname} and {vk2b.kname} are duplicates')
    t = s.pop()
    return t

class Tail:
    def __init__(self, bgrid, vk2dic, bitdic, block_bv_dic=None):
        self.bgrid = bgrid
        self.nov = bgrid.nov
        self.vk2dic = vk2dic
        self.split_sats = []
        self.combos = []
        # vk2-bdic : all vk1s will be removed in sort_vks
        self.bdic = self.copy_bdic(bitdic)
        self.bchecker = BlockChecker(self)
        if block_bv_dic != None:  # block_bv_dic==None: for clone
            self.sort_vks(vk2dic)
            self.blbmgr = BlbManager(self, block_bv_dic) 
        tuple_lst = self.proc_pairs()
        if tuple_lst:
            self.pair2blocker(tuple_lst)
        self.eval_combos()
        if Center.root_branch == None:
            Center.root_branch = Branch(None)
        Center.root_branch.add_tail(self.nov, self)

    def sort_vks(self, vk2dic):
        self.cvks_dic = {v: set([]) for v in self.bgrid.chvset }
        # only care about vk2s. All vk1s will become sats
        for kn, vk in vk2dic.items():  
            for cv in vk.cvs:
                self.cvks_dic[cv].add(kn)
        x = 0

    def remove_vk2(self, kn):
        # vk2.cvs became empty, remove it from vk2dic, and bdic
        vk = self.vk2dic.pop(kn, None)
        for b in vk.bits:
            if kn in self.bdic[b]:
                self.bdic[b].remove(kn)
                if len(self.bdic[b]) == 0:
                    del self.bdic[b]
        return vk
            
    def clone(self, split_sat_tpl):
        ntail = Tail(
            self.bgrid, 
            self.vk2dic.copy(),
            self.copy_bdic(self.bdic)
        )
        ntail.cvks_dic = self.copy_cvks_dic(self.cvks_dic)
        ntail.blbmgr = BlbManager(ntail) # self.blbmgr.clone(ntail)
        ntail.blbmgr.block_bv_dic = self.blbmgr.clone_block_bv_dic()
        ntail.split_sats = self.split_sats
        ntail.split_sats.append(split_sat_tpl)
        ntail.blbmgr.add_split_sat(split_sat_tpl)
        return ntail

    def proc_pairs(self):
        # find pairs of vk2s (vka, vka) bitting on the same 2 bits, and
        # vka.cvs vkb.cvs do have intersection
        pairs = []
        combo_pairs = []
        if 'C0115' in self.vk2dic:
            xx = 9
        vks = tuple(self.vk2dic.values())
        length = len(vks)
        i = 0
        while i < length - 1:
            x = i + 1
            while x < length:
                xvk = vks[x]
                if vks[i].bits == xvk.bits:
                    if vks[i].dic == xvk.dic:
                        combo_pairs.append((vks[i], xvk))
                    else:
                        xcvs = vks[i].cvs.intersection(xvk.cvs)  # common cvs
                        if len(xcvs) > 0:  # vk-i and xvk share xcvs != {}
                            sat_tpl = merge_vkpair(vks[i], xvk)
                            if sat_tpl:
                                pairs.append((vks[i], xvk, sat_tpl, xcvs))
                x += 1
            i += 1        
        for vka, vkb in combo_pairs:
            self.set_combo(vka, vkb)

        if len(pairs) == 0:
            return None
        return pairs

    def set_combo(self, vka, vkb):
        '''
        # in case vka and vkb having the same bits and the same dic,
        # 1. self.combos.append((vk1, vkb))
        # 2. make a new COMBOn: with uniofied cvs
        # 3 remove vka and vkb, 
        # 4. add COMBOn to vk2dic
        # 5. add COMBOn to self.cvks_dic[cvs]
        '''
        vk2 = vka.clone()
        # vk2-combo-n, shouldn't be more than 9 if this. So n:0..9
        vk2.kname = f"COMBO{len(self.combos)}"
        vk2.cvs = vk2.cvs.union(vkb.cvs)
        self.remove_vk2(vka.kname)    
        self.remove_kn2_from_cvk_dic(vka.cvs, vka.kname)
        self.remove_vk2(vkb.kname)
        self.remove_kn2_from_cvk_dic(vkb.cvs, vkb.kname)
        self.combos.append((vka, vkb))
        self.vk2dic[vk2.kname] = vk2
        x = 0

    def eval_combos(self):
        '''
        # for every combon vk2, if its bits overlpas with any existing 
        # sat in blbmgr: 
        # 1. pop off the sat-cvs
        # 2. if b in bits: for each bv in sat[b]:{bv0: cvs0, bv1: cvs1}
        #    if vk2[b] == bv, vk2 will create new sat
        # 3. put vk2.kname for all vk2.cvs in self.cvks_dic
        # -------------------------------------------------------------
        '''
        block_bv_dic = {}
        for index in range(len(self.combos)):
            vk2 = self.vk2dic[f'COMBO{index}']
            satbits = set(self.blbmgr.block_bv_dic).intersection(vk2.bits)
            for sb in satbits:
                for bv, cvs in self.blbmgr.block_bv_dic[sb].items():
                    # bv: val on the sat bit, covering cvs
                    xcvs = vk2.cvs.intersection(cvs)
                    vk2.pop_cvs(xcvs)
                    if vk2.dic[sb] != bv: 
                        if len(xcvs) > 0:
                            vk1 = vk2.clone([sb])
                            b, v = vk1.hbit_value()
                            block_bv_dic[b] = { v: xcvs, 'kn': vk1.kname }
            for cv in vk2.cvs:
                self.cvks_dic[cv].add(vk2.kname)
            x = 9
        if len(block_bv_dic) > 0:
            self.blbmgr.add_block_bv_dic(block_bv_dic)


    def pair2blocker(self, pair_tpls): # tpl: (vk-a, vk-b, sat-tpl, comm_cvs)
        block_bv_dic = {}
        for vka, vkb, stpl, cvs in pair_tpls:
            vka1 = vka.clone()
            kna = vka.kname
            vka1.pop_cvs(cvs)
            if len(vka1.cvs) == 0:
                self.remove_vk2(kna)
            else:
                self.vk2dic[kna] = vka1
            self.remove_kn2_from_cvk_dic(cvs, kna)

            vkb1 = vkb.clone()
            knb = vkb.kname
            vkb1.pop_cvs(cvs)
            if len(vkb1.cvs) == 0:
                self.remove_vk2(knb)
            else:
                self.vk2dic[knb] = vkb1
            self.remove_kn2_from_cvk_dic(cvs, knb)

            block_bv_dic[stpl[0]] = { stpl[1]: cvs }
            block_bv_dic[stpl[0]]['kn'] = kna

        self.blbmgr.add_block_bv_dic(block_bv_dic)


    def bdic_info(self):
        bs = sorted(self.bdic)
        msg = ''
        for b in bs:
            msg += f"{b}: {self.bdic[b]}\n"
        return msg

    def cvk_info(self, cv):
        msg = f'{self.nov}.{cv}({len(self.cvks_dic[cv])}X vks):\n'
        bdic = {}
        kns = sorted(self.cvks_dic[cv])
        for kn in kns:
            vk = self.vk2dic[kn]
            for b in vk.dic:
                bdic.setdefault(b, []).append(kn)
            msg += f'{kn}:{vk.dic}({vk.cvs})\n'
        msg += '-'* 40 + '\n'
        bks = sorted(bdic.keys())
        for bk in bks:
            msg += f" {bk}: {bdic[bk]}\n"
        print(msg)


    def add_vk2(self, vk2):
        self.vk2dic[vk2.kname] = vk2
        for cv in vk2.cvs:
            self.cvks_dic[cv].add(vk2.kname)

    def remove_kn2_from_cvk_dic(self, cvs, kn2):
        for cv in cvs:
            # cv may be missing in cvks_dic, in that case : []
            if kn2 in self.cvks_dic.get(cv, []):  
                self.cvks_dic[cv].remove(kn2)

    def copy_bdic(self, bdic):
        dic = {}
        for bit, val in bdic.items():
            dic[bit] = list(val)
        return dic

    def copy_cvks_dic(self, cvks_dic):
        dic = {}
        for cv, val in cvks_dic.items():
            dic[cv] = set(val)
        return dic

    def cvfoot_print(self, cv):
        vkdic = {}
        bdic = {}
        for kn in self.cvks_dic[cv]:
            vk = self.etail.vk2dic[kn]
            vkdic[kn] = vk
            for b, v in vk.dic.items():
                bdic.setdefault(b, set([])).add(kn)
        return vkdic, bdic

    def metrics(self):
        dic = {
            'vk2s': len(self.vk2dic),
            'bdic': len(self.bdic),
        }
        len1 = len(self.vk2dic)
        len2 = len(self.bdic)
        for cv, lst in self.cvks_dic.items():
            dic.setdefault(cv, len(lst))
        msg = f"{self.nov}/{self.split_sats}: vk2dic:{len1}, 'bdic:{len2}\n"
        msg += self.bdic_info()
        msg += f"{dic}, \nblbmap: {self.blbmgr.block_bv_dic}.\n"
        return msg