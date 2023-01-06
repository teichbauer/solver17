import random, sys, json
from lib1 import negate

class Generator:
    '''
    A instance of this class (gen), will generate a 2sat-problem, with 
    number of variables == nov, number of clauses == nok, with gen.generate()
    Each time .gen is called, it will generate next random 2sat problem, with
    the same nov/nok. And this problem will be saved under data/<fname>
    '''
    def __init__(self, nov, nok):
        self.nov = int(nov)     # number of variable
        self.nok = int(nok)     # number of clasues
        self.datadir = 'data'   # sub-dic name for storing the result-file
        self.gen_varpool()
        self.cpool = set()      # set of nok (2SAT)clauses

    def gen_varpool(self):
        # based on n==self.nov, generate var names like C1, C2, ... Cn
        self.vpool = []     # C1, C2, ..., Cn, ¬C1, ¬C2, ..., ¬Cn
        for i in range(self.nov):
            vname = f"{i}"
            nvname = negate(vname)
            self.vpool.append(vname)
            self.vpool.append(nvname)
        self.vleng = len(self.vpool)

    def vname(self, v):
        if v[0] == '¬':
            return negate(v)
        return v

    def make_dic(self, tup):  # tup: ()
        dic = {}
        for v in tup:
            if v[0] == '¬':
                bit = int(v[1])
                bv = 1
            else:
                bit = int(v)
                bv = 0
            dic[bit] = bv
        return dic
                

    def make_clause_tup(self, vnames): # var-name-list, vname-set
        ind = random.randint(0, self.vleng - 1)
        v1 = self.vpool[ind]
        vnames.add(self.vname(v1))
        while True:
            ind = random.randint(0, self.vleng - 1)
            v = self.vpool[ind]
            if v != v1 and v != negate(v1):
                # return clause-tuple, and var-names set
                vnames.add(self.vname(v))
                return  tuple(sorted([v1, v]))
    
    def generate(self):
        tup_set = set()
        vnames = set()
        cnt = self.nok
        while cnt > 0:
            tup = self.make_clause_tup(vnames)
            if tup not in tup_set:
                cnt -= 1
                tup_set.add(tup)
        dics = []
        for t in tup_set:
            dics.append(self.make_dic(t))
        return dics

def main(nv, nk, fname):
    m = {}
    gen = Generator(nv, nk)
    dics = gen.generate()
    for ind, dic in enumerate(dics):
        m[f"K{ind + 1}"] = dic
    print(f"clauses: \n  {m}\n")
    with open('data/' + fname, 'w', encoding='utf-8') as f:
        f.write('{\n')
        for kn, klause in m.items():
            msg = "\t" + f"'{kn}': {klause}" + ",\n"
            f.write(msg)
        f.write("}")

if __name__ == '__main__':
    an = len(sys.argv)
    if an != 4:
        print("usage: python <number of var> <number of clauses> <file-name>")
        # for testing:
        main(3, 4, 'test100.py')
    else:
        main(sys.argv[1], sys.argv[2],sys.argv[3])

        


