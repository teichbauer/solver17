# -----------------------------------------------------------------------------
# 2020-04-21
# ------------ Raymond Wei ----------------------------------------------------
# https://fairmut3x.wordpress.com/2011/07/29
#       /cnf-conjunctive-normal-form-dimacs-format-explained/
# cnf file format
# comment lines start with a 'c'
# parameter line starts with a 'p'
# every clause line ends with a 0
# n variables are represented by 1..n
# Example, for expression
#
#     (A v ¬B v C) ^ (B v D v E) ^ (D V F)
#
#     A,B,C,D,E,F  are represented by
#     1,2,3,4,5,6
#
# negative number represent NOT/¬
#     c This is a comment
#     c This is another comment
#     p cnf 6 3
#     1 -2 3 0
#     2 4 5 0
#     4 6 0
# =============================================================================
# the class Generator generates such a file, by taking
# nov : number of variables (n in above), and
# nok : number of clauses
# output files are stored under ./data/
# =============================================================================

import random
from datetime import datetime
import sys


class Generator:
    def __init__(self, nov, nok):
        self.nov = int(nov)
        self.nok = int(nok)
        self.datadir = 'data'

    def gen_newset(self):

        def get_r(nov):
            r = random.randint(1, 2 * nov)
            rr = r - self.nov
            if rr <= 0:
                rr -= 1
            return rr

        lst = []
        abslst = []   # prevent the case x and -x both in lst
        for i in range(3):
            rr = get_r(self.nov)
            abs_rr = abs(rr)
            while (rr in lst) or (abs_rr in abslst):
                rr = get_r(self.nov)
                abs_rr = abs(rr)
            lst.append(rr)
            abslst.append(abs_rr)
        return set(lst)

    def generate(self, fname):
        fil = open(f'{self.datadir}/{fname}', 'wt')  # wt: rite-text mode
        ts = datetime.now().isoformat()
        fil.write('c\n')
        fil.write(f'c {ts}\n')
        fil.write(f'c Raymond Wei\n')
        fil.write('c\n')
        pline = f'p cnf {self.nov} {self.nok}\n'
        fil.write(pline)
        fil.write('c\n')

        lines = []
        for i in range(self.nok):
            newset = self.gen_newset()
            while newset in lines:  # the same clause cannot be in twice
                newset = self.gen_newset()
            lines.append(newset)
        lines.append('%')
        lines.append('0')
        print(f'{fname} generated.')

        for pairset in lines:
            if type(pairset) == type(''):  # end of file lines: %\n and 0\n
                fil.write(str(pairset) + '\n')
            else:
                l = [str(e) for e in pairset]
                l.append('0')
                fil.write(' '.join(l) + '\n')
        fil.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('python cnf_generat.py <nov> <nok>')
        nov = 8
        nok = 38
        gen = Generator(nov, nok)
        filename = f'cnf{nov}-{nok}.cnf'
        gen.generate(filename)
    else:
        nov = sys.argv[1]
        nok = sys.argv[2]
        gen = Generator(nov, nok)
        filename = f'cnf{nov}-{nok}.cnf'
        gen.generate(filename)
