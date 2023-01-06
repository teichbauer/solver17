# ----------------------------------------
# 2022-12
# solving 2sat with bit-splitting method
# ----------------------------------------
import os
from pathnode import PathNode
from lib2 import output_dic

if __name__ == '__main__':
    # fname = 'test3.py'  # this has 3 sats:
    #  [{1: 0, 2: 1, 3: 1, 0: 1}, {1: 1, 0: 0, 2: 0, 3:2}]
    # -----------------------------------------------------------
    # fname = "f4-5-0.py"
    # 4x sats: [{0:2, 1:1, 2:1,3:2}]
    # ---------------------------------
    # fname = "f4-5-1.py"
    # 2x sats: {0: 2, 1: 0, 2: 0, 3: 0}
    # ----------------------------------
    # fname = "f4-5-2.py"
    # 3x sats: [{0: 0, 1: 1, 2: 0, 3: 0}, {0: 0, 1: 1, 2: 2, 3: 1}]
    # -------------------------------------------------------------
    # fname = "f4-5-3.py"
    # 3x sats: [{0: 0, 1: 0, 2: 0, 3: 0}, {0: 0, 1: 0, 2: 0, 3: 1}, 
    #           {0: 1, 1: 1, 2: 0, 3: 0}]
    # -----------------------------------------------------------------
    # fname = "f5-7-0.py"
    # 2x sats:
    # [{0: 1, 1: 1, 2: 0, 3: 2, 4: 0}, {0: 2, 1: 1, 2: 1, 3: 1, 4: 0}]
    # -----------------------------------------------------------------
    # fname = "f5-8-0.py"
    # 4x sats:
    # [{0: 0, 1: 1, 2: 2, 3: 0, 4: 2}]
    # -----------------------------------------------------------------
    # fname = "f5-9-0.py"
    # 4x sats:
    # [{0: 2, 1: 1, 2: 1, 3: 0, 4: 0}, {0: 1, 1: 1, 2: 1, 3: 1, 4: 2}]
    # -----------------------------------------------------------------
    # fname = "f5-9-1.py"
    # 5x sats:
    #  [{0: 1, 1: 2, 2: 0, 3: 1, 4: 0}, {0: 1, 1: 2, 2: 2, 3: 1, 4: 1}]
    # -----------------------------------------------------------------
    fname = "f5-10-0.py"
    # 1x sat
    # [{0: 1, 1: 1, 2: 1, 3: 0, 4: 1}]
    # -----------------------------------------------------------------
    # fname = "f5-10-1.py"
    # no sat possible

    if os.getcwd().endswith('2sat'):
        filename = 'data/' + fname
    else:
        filename = '2sat/data/' + fname
    
    data = open(filename).read()
    TestKlauses = eval(data)
    pn = PathNode(None, TestKlauses)
    print(f"\n2SAT clauses from file {fname}:")
    pn.output_clauses()

    pn.split_me()
    pn.include_wildbits()
    print(f"solutions:")
    sats = [eval(output_dic(sd)) for sd in pn.solution_sats]
    print(f"    {sats}")
    pn.verify()

    x = 1

            
                


