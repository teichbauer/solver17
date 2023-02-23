def output_dic(sat_dic):
    m = '{ '
    bits = sorted(sat_dic)
    for ind, bit in enumerate(bits):
        m += f" {bit}:{sat_dic[bit]}"
        if ind < len(bits) - 1:
            m += ','
    m += ' }'
    return m

def output_clause(clause):
    m = "  " + clause.kname +': {'
    m += f" {clause.bits[0]}:{clause.dic[clause.bits[0]]}, "
    m += f"{clause.bits[1]}:{clause.dic[clause.bits[1]]} " + "}"
    return m


# _get_bv(v = 1, bit = 0): 1, 
# _get_bv(v = 1, bit = 1): 0, 
# -------------------
# _get_bv(v = 5, bit = 0): 1, 
# _get_bv(v = 5, bit = 1): 0, 
# _get_bv(v = 5, bit = 2): 1, 
# _get_bv(v = 5, bit = 3): 0, 
# _get_bv(v = 5, bit = 4): 0, 
# -------------------
def _get_bv(v, bit):
    mask = 1 << bit
    if mask > v:
        return 0
    x = v >> bit
    return x & 1

def expand_bitcombo(bits):
    # return a list of dics with 4 possible bit/bv combinations
    # example: bits = [2, 5]
    # output: [{2:0, 5:0}, {2:0, 5:1}, {2:1, 5:0}, {2:1, 5:1}, ]
    # ----------------------------------------------------------
    maxv = 2 ** len(bits)
    bleng = len(bits)
    sats = []
    for r in range(maxv):
        dic = {}
        for b in range(bleng):
            v = _get_bv(r, b)
            dic[bits[b]] = v
        sats.append(dic)
    return sats

def expand_wildcard(sats):  
    # sats is a list of sat(dict). For a sat containing 1 or more 2s as value
    # 0. ss = sats.copy() - list of dic-refs
    # 1. pop out this xsat
    # 2. expand xsat to mutiple sats, add them to ss
    # 3. return ss
    # ------------------------------------------------------------------------
    ss = []
    candis = []
    for sat in sats:
        vs = sat.values()
        if 2 in vs:
            candis.append(sat)
        else:
            ss.append(sat)
    for sdic in candis:
        bs = [] # bits with bv == 2
        for bit, bv in sdic.items():
            if bv == 2:
                bs.append(bit)
        for b in bs:
            sdic.pop(b)
        edics = esxpand_bitcombo(bs)
        for xdic in edics:
            ndic = sdic.copy()
            ndic.update(xdic)
            ss.append(ndic)
    return ss


if __name__ == '__main__':
    ds = esxpand_bitcombo([2,4,5])
    # fixed sat
    sat1 = {0:1,1:1,2:0,4:1, 3:1}   

    # 2 wild-card on bit 2, 3. It will be expanded to 4 sats
    sat2 = {0:1,1:0,2:2,4:0, 3:2}   
    
    print(f"Before expansion: 2 sats\n")
    print(f"\t{sat1}")
    print(f"\t{sat2}")
    print("-----------------------------")
    sats = expand_wildcard([sat1, sat2])
    print(f"After expansion, there are {len(sats)} sats:")
    for sat in sats:
        print(f"\t{sat}\n")
    x = 1