from center import Center
from pathketten import PathKetten
from levelpath import LevelPath

class PathFinder:
    def __init__(self, branch):
        self.branch = branch
        self.sumbdic = branch.sumbdic
        self.etail = branch.chain[branch.novs[-1]]
        self.sat = branch.sat
        self.path_pool = {}  # {<nov>: [<children-vals>]}
        for nv in branch.novs:
            self.path_pool[nv] = sorted(branch.chain[nv].bgrid.chvset)

    def solve(self):
        sats = []
        vals = sorted(self.etail.bgrid.chvset)
        sat = self.sat.copy()
        ppool = {nv: chvs.copy() for nv, chvs in self.path_pool.items()}
        # pthketten = PathKetten(self, ppool, self.etail)
        lpath = LevelPath(self.branch, ppool)
        while True:
            nxt_nov = lpath.grow()
            if nxt_nov == Center.maxnov:
                x = 0
                break
        tail = self.etail
        ketten = PathKetten(ppool, tail)
        while True:
            nxnov = tail.nov + 3
            if nxnov > Center.maxnov:
                break
            ntail = Center.snodes[nxnov].tail
            res = ketten.walkup(ntail)
        x = 0

    def search_path(self, path_ketten):
        """
        search for a complete path. A path is like
        [(20.1),(24.2),...(60.3)].  If a path can not be completed, as in
        [(20.1),(24.2),(27,4)] failed on 27.4, then 27.4 purged from ppool,
        and will try [(20.1),(24.2),(27,5)]
        """
        return True


    def search_path1(self, lnode):
        return lnode.grow()

    def find_path(self, 
                  vkdic, bdic,  # from path sofar, till/including stail
                  ppool,
                  path):
        start_nv, start_cv = path[-1]
        vdc, bdc = vkdic.copy(), bdic.copy()
        nxt_nv = start_nv + 3    # next nov
        if len(ppool[nxt_nv]) == 0:
            return False
        nxt_cv = ppool[nxt_nv].pop(0)
        ntail = self.branch.chain[nxt_nv]

        for kn in ntail.cvks_dic[nxt_cv]:
            vk = ntail.vk2dic[kn]
            vdc[kn] = vk
            for b, v in vk.dic.items():
                bdc.setdefault(b,[]).append(kn)
        blck_dc = ntail.blbmgr.clone_block_bv_dic()
        for pnv, pcv in path:
            if pnv in ntail.blbmgr.cbdic:
                for kn, tp in ntail.blbmgr.cbdic[pnv].items():
                    # tp[0]: {cvs from tail[pnv] this vk has influence}
                    # tp[1]: {cvs of ntail this vk is in}
                    # tp[2]: (b,v): if hit, resulting this blocker (b,v)
                    if start_cv in tp[0] and nxt_cv in tp[1]:
                        if kn in vdc:
                            vdc.pop(kn)
                        if tp[2][0] in blck_dc:
                            x = 0
                        else:
                            blck_dc[tp[2][0]] = 100
        if self.filter(vdc, bdc, blck_dc):
            path.append((nxt_nv, nxt_cv))
            if len(path) == len(self.branch.novs):
                return True
            else:
                return self.find_path(vdc, bdc, ppool, path)
        return False

    def filter(self, vkdic, bitdic, block_dic):
        return True

    def get_pathsat(self, path):
        return 1


    def ppool_wholly(self, ppool):
        '''
        each nov-entry in path_pool must be non-0-length : wholly
        Otherwise, it is broken/wholly: false
        '''
        for nv, chvs in ppool.items():
            if len(chvs) == 0:
                return False
        return True
