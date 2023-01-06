from sol1 import negate

def evaluate_clause(clause, vdic):
    if vdic[clause[0]] == 0 and vdic[clause[1]] == 0:
        return False
    return True

def verifier(vdic, # vdic: {"¬a":0, "b":1,...}
        clauses):  # a clause is formatted like: ("¬a", "b")
    result = True
    for clause in clauses: 
        must = (clause[0] in vdic) and (clause[1] in vdic)
        assert (must), f"{clause[0]} or {clause[1]} not in vars."
        if not evaluate_clause(clause, vdic):
            return False
    return True

def simplify_solution(vdic):
    dic = {}
    for var, val in vdic.items():
        if var[0] == '¬':
            v = negate(var)
            if v not in dic:
                dic[v] = int(not val)
        else:
            if var not in dic:
                dic[var] = val
    return dic
