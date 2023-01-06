from symbol import namedexpr_test
from vk2pkg import Vk2Package
from pathseg import PathSeg
from center import Center

class LevelPath:
    def __init__(self, branch, path_pool):
        self.branch = branch
        self.path_pool = path_pool
        self.tail = branch.chain[Center.minnov]
        self.vkdic = self.tail.vk2dic
        # a path-segment is a dic like: {24:{1,2,3}, 21:{0,4,5}}
        # [{24:{1,2,3}, 21:{0,4,5}},{<p-seg},{<p-seg}, ...]
        self.psegs = {}         # {<nov>:[pseg, pseg,..], <nov>:[]}
        self.path_blockers = {} # {<pseg-name>: (pseg, [kns]), ...}
        # self.path_blockdic = {} # {<bit>: {0:[<p-seg>m,,], 1:[..]} } }
        self.sumbdic = self.tail.bdic
        self.sumblbdic = {} #{<bit>:[pseg,..]}

    def get_psegs(self, nov):
        ps = []
        while nov > Center.minnov:
            for pseg in self.psegs[nov]:
                ps.append(pseg)
            nov -= 3
        return ps

    def grow(self): # current tail grow to next_tail
        nxt_tail = self.branch.chain[self.tail.nov + 3]
        x = 0
        for bit, bvd in nxt_tail.bchecker.checkdic.items():
            for bv, lst in bvd.items():
                for d in lst:
                    pseg = self.verified_add_pseg(nxt_tail.nov, d, bit, bv)
        self.vkdic.update(nxt_tail.vk2dic)
        self.sumbdic = self.merge_bdics(nxt_tail.bdic, self.sumbdic)
        kns, bits = self.touched_tail_kns(nxt_tail)
        for kn in kns:
            vk = nxt_tail.vk2dic[kn]
            bs = bits.intersection(vk.bits)
            psgs = set([])
            while len(bs) > 0:
                psgs = psgs.union(self.sumblbdic[bs.pop()])

            for pseg in psgs:
                ps = pseg.filter_vk(vk, self)

        self.tail = nxt_tail
        return self.tail.nov

    def verified_add_pseg(self, nv, # nov for the potential pseg
                          bdic,     # {kn:kname, nv:{cvs}, nv: <cvs>}
                          bit,      # bit in {bit:bit-val}
                          bv):      # bit-val in {bit:bit-val}
        # make a pseg(nv, bdic, bvdic) and add it to self.psegs and
        # self.sumblbdic, if there is not conflict
        # return: True: added, False there is conflict, not added
        pseg = PathSeg(nv, bdic, {bit:bv})
        if bit in self.sumblbdic:
            for psg in self.sumblbdic[bit]:
                if psg.has_conflict(pseg):
                    if psg.hnv == pseg.hnv:
                        c_cvs = psg.dic[psg.hnv].intersection(pseg.dic[psg.hnv])
                        if len(c_cvs) > 0:
                            psg.blockers['ports'][psg.hnv] = c_cvs
                            pseg.blockers['ports'][psg.hnv] = c_cvs
                    else:
                        pseg.blockers['conflicts'].append(psg)
                        # psg.blockers['conflicts'].append(pseg)
                elif psg.vkname == bdic['kn']:
                    if psg.dic == pseg.dic:
                        return psg
        self.psegs.setdefault(nv, []).append(pseg)
        self.sumblbdic.setdefault(bit,[]).append(pseg)
        return pseg

    def merge_bdics(self, bdic1, bdic0):
        bdic = { xb:kns.copy() for xb, kns in bdic1.items()}
        for b, kns in bdic0.items():
            if b in bdic:
                for kn in kns:
                    bdic[b].append(kn)
            else:
                bdic[b] = kns
        return bdic

    def touched_tail_kns(self, tail):
        bits = set(self.sumblbdic).intersection(tail.bdic)
        kns = set([])
        for b in bits:
            for kn in tail.bdic[b]:
                kns.add(kn)
        return kns, bits
