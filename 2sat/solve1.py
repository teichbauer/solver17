from lib1 import negate, satisfy
import os
from verify import verifier, simplify_solution

def main(file_name):
    # this may run from ROOT (solver17): then prefix with '2sat/'
    if os.getcwd().endswith('solver17'):
        file_name = '2sat/' + file_name
    with open(file_name) as fil:
        data = fil.read()
        dic = eval(data)
    res = satisfy(dic['vars'], dic['clauses'])
    if res:
        vdic = {}
        for v in res:
            vdic[v] = 0
            nv = negate(v)
            if nv in dic['vars']:
                vdic[nv] = 1
        if verifier(vdic, dic['clauses']):
            # simplify {'¬b': 0, 'b': 1, '¬a': 0, 'a': 1, '¬c': 0, 'c': 1}
            # into     {'a': 1, 'b': 1, 'c': 1} 
            sdic = simplify_solution(vdic)
            msg = f"{file_name} has a solution: {sdic}"
        else:
            msg = "algorithm failed"
    else:
        msg = f"There is no solution for {file_name}"
    print(msg)

    
if __name__ == "__main__":
    # main("twosat_01.py")
    # main("data/test01.py") ## no solution
    # main("data/test02.py") ## no solution
    main("data/test03.py") # 3x solutions(C1 C2 C3 C4): 1011, 0100, 0101
                           # only 1011 is found. how to get next solutions?