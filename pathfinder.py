from center import Center
from millipede import Millipede
from cluster import Cluster
from basics import sortdic

class PathFinder:
    def __init__(self, branch):
        self.branch = branch
        self.sumbdic = branch.sumbdic
        self.sat = branch.sat
        end_tail = branch.chain[Center.minnov]  # end-tail
        self.millipede = Millipede(end_tail)
        self.clusters = Cluster.cluster_dic
        start_tail = branch.chain[Center.maxnov]
        self.grow_cluster(start_tail)
        hit_cnt = self.downwards(branch.chain)
        # self.find_solutions()
        self.find_path()

    def grow_cluster(self, tail):
        while tail.nov >= Center.minnov:
            if tail.nov >= Center.minnov + 3:
                ntail = self.branch.chain[tail.nov - 3]
                for cv, cvn2 in tail.cvn2s.items():
                    cluster = Cluster((tail.nov,cv), cvn2)
                    # grow cluster between (tail, ntail)
                    cluster.grow(ntail)
                if ntail.nov == Center.minnov:
                    break
                elif ntail.nov - 3 < Center.minnov:
                    tail = self.branch.chain[Center.minnov]
                else:
                    tail = self.branch.chain[ntail.nov - 3]
        x = 8

    def upwards(self):
        x = 0

    def downwards(self, tailchain):
        cnt = 0
        nov = Center.maxnov
        while nov in Cluster.groups:
            group = Cluster.groups[nov]
            #nov: 60, 54, ...
            for name, cluster in group:
                print(f"{name}-cluster.")
                # name:((60,1),(57,2)),cl: cluster.name == name
                nv = nov - 6
                dsbits, dsat = cluster.delta_sat()
                while nv in Cluster.groups:
                    for nam, cl in Cluster.groups[nv]:
                        if cluster.block.name_inblock(name):
                            continue
                            continue
                        ibits = dsbits.intersection(cl.sat)
                        if len(ibits) > 0:
                            idic = {b: dsat[b] for b in ibits}
                            hit, nm = cl.test_sat(idic)
                            if hit:
                                if nm:
                                    bnv, cvs = nm
                                    for cv in cvs:
                                        cluster.block.add_block((bnv, cv))
                                    cnt += len(cvs)
                                    print(f"({bnv}, {cv}) hit")
                                    continue
                                else:
                                    cluster.block.add_block(name)
                                    cnt += 1
                                    print(f"{nam}-hit")
                    nv -= 6
            print("=================")
            nov -= 6
        return cnt

    def find_solutions(self):
        gnvs = list(Cluster.groups.keys())
        gi = gnvs.pop()
        while len(gnvs) > 0:
            g = Cluster.groups[gi]
            g1i = gnvs.pop()
            g1 = Cluster.groups[g1i]
            for name, clu in g:
                for nam, cl in g1:
                    new_cl = clu.merge_cluster(cl)
                    x = 0
        x = 1

    def find_path(self):
        pathdic = {}
        lnv, lind = 60, 0
        nlnv = lnv - 6
        cluster = Cluster.groups[lnv][lind][1]
        ngrp = Cluster.groups[nlnv]
        path = [ cluster ]
        if not self.pathdown(path, cluster, ngrp):
            lind += 1
        else:
            x = 9

    def pathdown(self, path, clustr, ngrp):
        ind = 0
        found = False
        while not found:
            nclstr = ngrp[ind][1]
            if clustr.block.name_inblock(tuple(nclstr.name)):
                ind += 1
                if ind > (len(ngrp) - 1):
                    return None
                continue
            nx = clustr.merge_cluster(nclstr)
            if not nx:
                ind += 1
                if ind > (len(ngrp) - 1):
                    return None
            else:
                cl, mv = nx
                path.append(cl)
                mgrp = Cluster.groups[mv]
                mx = self.pathdown(path, cl, mgrp)
                if not mx:
                    ind += 1
                else:
                    return True
        x = 0