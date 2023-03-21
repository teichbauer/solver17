from center import Center
from cluster import Cluster
from basics import sortdic, print_bitdic, print_clause_dic

class PathFinder:
    def __init__(self, branch):
        self.branch = branch
        self.sumbdic = branch.sumbdic
        self.sat = branch.sat
        self.cluster_groups = Cluster.groups
        self.grow_cluster( branch.chain[Center.maxnov] )
        hit_cnt = self.downwards()
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

    def downwards(self):
        cnt = 0
        nov = Center.maxnov
        while nov in Cluster.groups:
            # nov: 60, 54, 48, 42, 36, 30, 24
            for name, cluster in self.cluster_groups[nov]:
                print(f"{name}-cluster.")  # cluster.name:((60,1),(57,2))
                nv = nov - 6
                body_satbits, body_sat = cluster.body_sat()
                while nv in self.cluster_groups:
                    for nam, cl in self.cluster_groups[nv]:
                        if cluster.block.name_inblock(nam):
                            continue
                        ibits = body_satbits.intersection(cl.sat)
                        if len(ibits) > 0:
                            idic = {b: body_sat[b] for b in ibits}
                            hit, nm = cl.test_sat(idic)
                            if hit:
                                if nm:
                                    bnv, cvs = nm
                                    for cv in cvs:
                                        cluster.block.add_block((bnv, cv))
                                    cnt += len(cvs)
                                    print(f"({bnv}, {cvs}) hit")
                                    continue
                                else:
                                    cluster.block.add_block(nam)
                                    cnt += 1
                                    print(f"{nam}-hit")
                    nv -= 6
            print("=================")
            nov -= 6 # nov/while loop, 60 ->54 ->48 ->42 ->36 ->30 ->24
        return cnt

    def find_path(self):
        lnv, lind = 60, 0
        nlnv = lnv - 6
        cluster = self.cluster_groups[lnv][lind][1]
        path = [ cluster ]
        if not self.pathdown(path, cluster, self.cluster_groups[nlnv]):
            lind += 1
        else:
            x = 9

    def pathdown(self, path, clustr, ngrp):
        # set pblock for the next 2 lower tails
        nv = clustr.nov - 6
        tails = []
        while nv >= Center.minnov and nv >= clustr.nov - 9:
            tails.append(Center.snodes[nv].tail)
            nv -= 3
        clustr.set_pblock(tails)

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
        