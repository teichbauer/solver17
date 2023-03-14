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
        self.downwards(branch.chain)

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
        # msg = self.cluster_sat(24)
        x = 8

    def downwards(self, tailchain):
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
                        if nam[0] in cluster.blocker_set or \
                            nam[1] in cluster.blocker_set:
                            continue
                        ibits = dsbits.intersection(cl.sat)
                        if len(ibits) > 0:
                            idic = {b: dsat[b] for b in ibits}
                            hit, nm = cl.test_sat(idic)
                            if hit:
                                print(f"{nam} hit")
                                bnv, cvs = nm
                                for cv in cvs:
                                    cluster.blocker_set.add((bnv, cv))
                                continue
                            # else:
                            #     print(f"{nam} passed")
                            x = 9
                        x = 0
                    nv -= 6
                x = 0
            print("=================")
            nov -= 6
        x = 0

    def downward_blocker(self):
        for nov in self.branch.novs:
            tail = self.branch.chain[nov]
            for cvn2 in tail.node2s.values():
                nv = nov -3
                while nv >= Center.minnov:
                    t = self.branch.chain[nv]
                    head = t.bgrid.bitset
                    for b, v in cvn2.sat.items():
                        if b in head:
                            cvs = t.bgrid.bv2cvs(b,int(not v))
                            for cv in cvs:
                                cvn2.lower_blocks.add((t.nov, cv))
                    # heads of lower tail.cvn2s piercing into cvn2.bitdic
                    xbits = head.intersection(cvn2.bitdic)
                    if xbits:
                        for tcv, tcvn2 in t.cvn2s.items():
                            xcvn2 = cvn2.clone()
                            sat = t.bgrid.grid_sat(tcv).copy()
                            # new_sat = {}
                            # if not xcvn2.add_sat(sat, new_sat):
                            if not xcvn2.add_sat(sat):
                                x = 0
                            else:
                                pass
                                # if len(new_sat) > 0:
                                #     x = 8
                            if xcvn2.add_cvn2(tcvn2):

                                x = 8
                            else:
                                x = 0
                        x = 9
                    nv = nv - 3

                x = 0
            x = 9
        x = 9

    def cluster_sat(self, gname):
        msg = {}
        for g in Cluster.groups[gname]:
            name, satdic = g[0], sortdic(g[1].sat)
            print(name, satdic)

    def find_solutions(self):
        # for cvn2 in self.etail.node2s.values():
        #     self.find_path(self.etail, cvn2)
        nov = self.millipede.etail.nov
        while True:
            tail = self.branch.chain[nov+3]
            self.millipede.grow(tail)
            if tail.nov == Center.maxnov: 
                return
            nov = tail.nov
        x = 1
