class PathSeg:
    def __init__(self, hnov,  # head-nov(hn)
                 blockdic,    # {<hn>:h-cvs, lower-nov: l-cvs, kn:<kn>}
                 bvdic={}):   # {bit:bv}
        dic = blockdic.copy()
        self.hnv = hnov
        self.vkname = dic.pop('kn')
        hcvs = dic.pop(hnov)
        self.dic = {hnov: hcvs}
        self.blockers = {
            'vkdic':{self.vkname: None}, # <kn>:<replace-vk under this kn>
            'ports': {},    # <nov>:(0,2,3,4) - ports blocked for nov
            'conflicts':[]  # have conflict with these psegs
        }
        if len(dic) == 0:
            # there may be a single blocker
            self.name = ((hnov, tuple(hcvs)))
        else:
            name_lst = [(hnov, tuple(hcvs))]
            while len(dic) > 0:
                lst = sorted(dic.keys(), reverse=True)
                lnov = lst.pop(0)
                lcvs = dic.pop(lnov)
                name_lst.append((lnov, tuple(lcvs)))
                # self.name = ((hnov, tuple(hcvs)),(lnov, tuple(lcvs)))
                self.dic[lnov] = lcvs
            self.name = self.compact_name(name_lst)
        self.bvdic = bvdic

    def compact_name(self, nlst):
        msg = ''
        while len(nlst) > 0:
            t = nlst.pop(0)
            msg += f"{t[0]}("
            for e in t[1]:
                msg += f"{e}"
            msg += ")"
            if len(nlst) > 0:
                msg += "+"
        return msg
            

    def filter_vk(self, vk, parent): #sumblbdic, psegs):
        bs = set(self.bvdic).intersection(vk.bits)
        self.blockers['vkdic'][vk.kname] = None
        if len(bs) == 2:
            if self.vkname != vk.kname:
                # in case vk.nov == self.hnv and self.dic[hnv] == vk.cvd:
                # it is normal. Otherwise, stop here and take a loop @ x = 9
                if vk.nov != self.hnv or self.dic[vk.nov] != vk.cvs:
                    p1, p2 = tuple(vk.dic.items())
                    d = self.bvdic
                    if (d[p1[0]] == p1[1] and d[p2[0]] == p2[1]) or \
                       (d[p1[0]] != p1[1] and d[p2[0]] != p2[1]):
                        self.blockers['vkdic'][vk.kname] = None
                    else:
                        # one same, one diff:
                        self.blockers['ports'][vk.nov] = vk.cvs
                else:
                    x = 9   # can thi shappend?
            return self
        else:
            b = bs.pop()
            if vk.nov == self.hnv:
                # if vk.dic[b] == self.bvdic[b]:  # <= 0.372
                if vk.dic[b] != self.bvdic[b]:
                    vk1 = vk.clone([b])
                    if vk.cvs == self.dic[vk.nov]:
                        self.bvdic.update(vk1.dic)
                        parent.sumblbdic.setdefault(vk1.bits[0],[]).append(self)
                    else:
                        cmm_cvs = vk.cvs.intersection(self.dic[vk.nov])
                        if len(cmm_cvs) > 0:
                            d = self.dic.copy()
                            bt,v = vk1.hbit_value()
                            d[vk.nov] = cmm_cvs
                            d['kn'] = vk.kname
                            pg = parent.verified_add_pseg(vk.nov, d, bt, v)
                            return pg
                        else:
                            # there is no intersection btwn vk.cvs and 
                            # self.dic[hnv] - vk is not involved/untouched:
                            # remove blockers['vkdic'][kvname]==None entry
                            self.blockers['vkdic'].pop(vk.kname)

                elif vk.kname != self.vkname:
                    new_cvs = vk.cvs - self.dic[self.hnv]
                    if len(new_cvs) > 0:
                        # vk's cvs not covered by self, forms a new-vk
                        new_vk = vk.clone()
                        new_vk.cvs = new_cvs
                        self.blockers[vk.kname] = new_vk
                return self
            # for vk.nov != self.hnv, if vk.dic[b] != self.bvdic[b]:# <= 0.372
            if vk.dic[b] == self.bvdic[b]: 
                return self
            # vk.dic[b] == self.bvdic[b]
            vk1 = vk.clone([b])
            bit, bv = vk1.hbit_value()
            d = self.dic.copy()
            d.update({vk.nov: vk.cvs})
            # if there exists a pseg(on the same nov) that better covers d
            if bit in parent.sumblbdic:
                for pseg in parent.sumblbdic[bit]:
                    if pseg in parent.psegs[vk.nov]: 
                        if pseg.bvdic[bit] == bv:
                            if pseg.vkname == vk.kname:
                                return pseg
                            if pseg.is_superset(d):
                                pseg.vkname += f"+{vk.kname}"
                                pseg.blockers['vkdic'][vk.kname] = None
                                return pseg
                        else:
                            cmm_cvs = pseg.dic[pseg.hnv].intersection(vk.cvs)
                            if len(cmm_cvs) > 0:
                                pseg.blockers['ports'][vk.nov] = cmm_cvs
            d['kn'] = vk.kname
            pseg = parent.verified_add_pseg(vk.nov, d, bit, bv)
            return pseg

    def is_superset(self, psegdic):
        for nv, cvs in self.dic.items():
            if nv in psegdic:
                if not cvs.issuperset(psegdic[nv]):
                    return False
            else:
                return False
        return True

    def add_pseg(self, pseg, sumblbdic, psegs):
        bs = set(pseg.dic)
        for xpg in psegs[pseg.hnv]:
            xbs = set(xpg.dic)
            if xbs in bs and xpg.is_superset(pseg):
                return
        psegs[pseg.hnv].append(pseg)
        for b in bs:
            sumblbdic.setdefault(b,[]).append(pseg)

    def has_conflict(self, pseg):
        comm_bits = set(pseg.bvdic).intersection(self.bvdic)
        for bit in comm_bits:
            if self.bvdic[bit] != pseg.bvdic[bit]:
                return True
            else:
                x = 0
        return False

    def show(self):
        msg = f'name{self.hnv}: {self.name}\n'
        msg += f'bit-bvs: {self.bvdic}\nBlockers:\n'
        rmvs = ''
        rpls = ''
        for kn in self.blockers['vkdic']:
            if self.blockers['vkdic'][kn] != None:
                rpls += f"{kn}  "
            else:
                rmvs += f"{kn}  "
        msg += f"  removes: {rmvs}\n"
        if len(rpls) > 0:
            msg += f"  repl: {rpls}\n"
        msg += "Conflicts:\n"
        for cf_pseg in self.blockers['conflicts']:
            msg += f"  {cf_pseg.name} : "
        msg += "\n==============\n"
        return msg

