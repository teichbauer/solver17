import random, sys, json
from sol1 import negate

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
            vname = f"C{i+1}"
            nvname = negate(vname)
            self.vpool.append(vname)
            self.vpool.append(nvname)
        self.vleng = len(self.vpool)

    def vname(self, v):
        if v[0] == '¬':
            return negate(v)
        return v

    def make_clause(self, vnames): # var-name-list, vname-set
        ind = random.randint(0, self.vleng - 1)
        v1 = self.vpool[ind]
        vnames.add(self.vname(v1))
        while True:
            ind = random.randint(0, self.vleng - 1)
            v = self.vpool[ind]
            if v != v1 and v != negate(v1):
                # return clause-tuple, and var-names set
                vnames.add(self.vname(v))
                return  (v1, v)
    
    def generate(self):
        clauses = set()
        vnames = set()
        cnt = self.nok
        while cnt > 0:
            clause = self.make_clause(vnames)
            if clause not in clauses:
                cnt -= 1
                clauses.add(clause)
        return clauses, vnames

def main(nv, nk, fname):
    m = {}
    gen = Generator(nv, nk)
    clauses, vnames = gen.generate()
    print(f"clauses: \n  {clauses}\n")
    names = sorted(vnames)
    m['vars'] = names
    m['clauses'] = list(clauses)
    print(f"variables: {names}")
    with open('data/' + fname, 'w', encoding='utf-8') as f:
        json.dump(m, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    an = len(sys.argv)
    if an != 4:
        print("usage: python <number of var> <number of clauses> <file-name>")
        # for testing:
        main(3, 4, 'test00.py')
    else:
        main(sys.argv[1], sys.argv[2],sys.argv[3])

        


