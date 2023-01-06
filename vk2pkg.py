
def merge_vkpair(vk2a, vk2b): # vk2a and vk2b must have common-cvs
    #         vk2a         vk2b                 return
    #---------------------------------------------------
    # dic1:{ 11:0, 21:1}, dic2:{11:1, 21:1} -> {(21,1)}
    # dic1:{ 11:0, 21:1}, dic2:{11:0, 21:0} -> {(11,0)}
    # dic1:{ 11:0, 21:1}, dic2:{11:1, 21:0} -> {}
    # -------------------------------------
    # not possible to have: dica == dicb
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

class Vk2Package:
    def __init__(self, parent, clone_src=None):
        self.parent = parent
        if clone_src:
            self.combvks = clone_src.combvks.copy()
            self.vkdic = clone_src.vkdic.copy()
            self.bdic = { b: s.copy() for b, s in clone_src.bdic.items() } 
            self.blocks = clone_src.blocks.copy()
        else:
            self.combvks = []
            self.vkdic = {}
            self.bdic = {}
            self.blocks = {}

    def clone(self):
        return self

    def add_block(self, b, v):
        if b in self.blocks:
            if v != self.blocks[b]:
                return False
        else:
            self.blocks[b] = v
        if b in self.bdic:
            kns = self.bdic.get(b, set([])).copy()  # bdic may change:use copy
            for kn in kns:
                vk = self.vkdic[kn]
                for bt in vk.bits:
                    if vk.kname in self.bdic[bt]:
                        self.bdic[bt].remove(vk.kname)
                        if len(self.bdic[bt]) == 0:
                            del self.bdic[bt]
                self.vkdic.pop(vk.kname)
                # A(A+B) = A. B can be ignored
                # A(not-A + B) = AB. B is a new block
                if vk.dic[b] != v: 
                    vk1 = vk.clone([b])
                    res = self.add_block(vk1.bits[0], vk1.dic[vk1.bits[0]])
                    if not res:
                        return False
        return True

    def filter_pairs(self): #
        # find pairs of vk2s (vka, vka) bitting on the same 2 bits, and
        # vka.cvs vkb.cvs do have intersection
        pairs = []
        combo_pairs = []
        vks = tuple(self.vkdic.values())
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
        return pairs, combo_pairs

    def proc_pair(self, vka, vkb):
        if vka.nov == vkb.nov:
            cmm_cvs = vka.cvs.intersection(vkb.cvs)
            if len(cmm_cvs) > 0:
                if vka.dic == vkb.dic: # overlap-pair
                    combvk = vka.clone()
                    combvk.cvs = cmm_cvs
                    self.combvks.append(combvk)
                    combvk.kname = f"COMB{len(self.combvks)}"
                    self.vkdic[combvk.kname] = combvk
                    vka1 = vka.clone()
                    vka1.cvs = vka.cvs - combvk.cvs
                    if len(vka1.cvs) > 0:
                        self.vkdic[vka.kname] = vka1
                    else:
                        self.vkdic.pop(vka.kname)
                    vkb1 = vkb.clone()
                    vkb1.cvs = vkb.cvs - combvk.cvs
                    if len(vkb1.cvs) > 0:
                        self.vkdic[vkb.kname] = vkb1
                    else:
                        self.vkdic.pop(vkb.kname)
                else:
                    t = merge_vkpair(vka, vkb)


    def finalize(self):
        return True

    def put_in_vk(self, vk):
        self.vkdic[vk.kname] = vk
        for b in vk.dic:
            self.bdic.setdefault(b, set([])).add(vk.kname)

    def add_vk(self, vk): # vk can be vk1 or vk2
        bs = set(self.blocks).intersection(vk.bits)
        if len(bs) > 0:
            for b in bs:
                if vk.dic[b] == self.blocks[b]: # this vk ignored
                    return True
                else:  # vk.dic[b] != self.blocks[b]
                    # vk drops b, and forma new block
                    vk1 = vk.clone([b])
                    if not self.add_block(vk1.bits[0], vk1.dic[vk1.bits[0]]):
                        return False
            return True
        # if 2 bits are in bdic?
        sbits = set(self.bdic).intersection(vk.bits)
        if len(sbits) < 2:
            self.put_in_vk(vk)
        else: # 2 bits of vk in bdic
            # loop thru kns sitting on 1 bit 
            # if put_in_vk called, bdic[] will change: if kns is s ref,
            # and bdic changed, for loop will err: reason to use kns.clone
            kns = self.bdic[vk.bits[0]].copy()
            for kn in kns:
                xvk = self.vkdic[kn]
                # see if xvk and vk are on the same 2 bits
                if vk.bits == xvk.bits:
                    # if dics are the same, skip vk
                    if vk.dic == xvk.dic:
                        continue
                    else:
                        t = merge_vkpair(vk, xvk)
                        if len(t) == 0:
                            # vk and xvk are not related
                            self.put_in_vk(vk)
                        else: #
                            if not self.add_block(t):
                                return False
                else:
                    self.put_in_vk(vk)

        return True
