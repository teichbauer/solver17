from datetime import datetime

def flip_tuple_bitvalue(tp, index):
    lst = list(tp)
    lst[index] = oppo_binary(tp[index])
    return tuple(lst)

def verify_sat(vkdic, sat, collect=False):
    lst = set([])
    for vk in vkdic.values():
        if vk.hit(sat):
            if collect:
                lst.add(vk.kname)
            else:
                return False
    if collect and len(lst) > 0:
        return lst
    return True


def nov_val(msg):  # '12.4' -> 12, 4
    lst = []
    for m in msg.split("."):
        lst.append(int(m))
    return lst


def get_bit(val, bit):
    return (val >> bit) & 1


def set_bit(val, bit_index, new_bit_value):
    """Set the bit_index (0-based) bit of val to x (1 or 0)
    and return the new val.
    the input param val remains unmodified, for val is passed-in by-value !
    """
    mask = 1 << bit_index  # mask - integer with just the chosen bit set.
    val &= ~mask  # Clear the bit indicated by the mask (if x == 0)
    if new_bit_value:
        val |= mask  # If x was True, set the bit indicated by the mask.
    return val  # Return the result, we're done.


def set_bits(val, d):
    for b, v in d.items():
        val = set_bit(val, b, v)
    return val

def oppo_binary(binary_value):
    return (binary_value + 1) % 2


def get_sdic(filename):
    path = "./configs/" + filename
    sdic = eval(open(path).read())
    return sdic


def ordered_dic_string(d):
    v2cnt = 0
    m = "{ "
    ks = sorted(d.keys(), reverse=True)
    for k in ks:
        if d[k] == 2:
            v2cnt += 1
        m += str(k) + ": " + str(d[k]) + ", "
    m = m.strip(", ")
    m += " }"
    return m, v2cnt


def print_json(nov, vkdic, fname):
    sdic = {"nov": nov, "kdic": {}}
    for kn, vk in vkdic.items():
        sdic["kdic"][kn] = vk.dic
    ks = sorted(list(sdic["kdic"].keys()))

    with open(fname, "w") as f:
        f.write("{\n")
        f.write('    "nov": ' + str(sdic["nov"]) + ",\n")
        f.write('    "kdic": {\n')
        # for k, d in sdic['kdic'].items():
        for k in ks:
            msg = ordered_dic_string(sdic["kdic"][k])[0]
            line = f'        "{k}": {msg},'
            f.write(f"{line}\n")
        f.write("    }\n}")


def topvalue(vk):
    # shift all bit to top positions and return that n-bits value
    # E.G. {7:1, 5:0, 0:1} -> 101/5
    bits = vk.bits[:]
    v = 0
    while bits:
        v = (v << 1) | vk.dic[bits.pop(0)]
    return v


def topbits(nov, nob):
    lst = list(range(nov)[-nob:])
    lst.reverse()
    return lst


def vkdic_remove(vkdic, kns):
    """remove vk from vkdic, if vk.kname is in kns(a list)"""
    kd = {}
    for kn, vk in vkdic.items():
        if kn not in kns:
            kd[kn] = vk
    return kd

def sortdic(d):
    ks = sorted(d)
    dd = {}
    for k in ks:
       dd[k] = d[k]
    return dd

def display_vkdic(vkd, title=None, outfile=None):
    kns = sorted(vkd.keys())
    kns.sort()
    if outfile:
        now = datetime.now()
        with open(outfile, 'w') as ofile:
            ofile.write(f"{now.isoformat()}\n----------------------\n")
            if title:
                ofile.write(f"{title}\n---------\n")
            for kn in kns:
                vk = vkd[kn]
                msg, dummy = ordered_dic_string(vk.dic)
                ofile.write(f"{kn}: {msg}\n")
    else:
        if title:
            print(title)
        for kn in kns:
            vk = vkd[kn]
            msg = f"{kn}: " + ordered_dic_string(vk.dic)[0]
            if len(vk.bits) < 3:
                msg += f" {vk.nov},{vk.cvs}"
            print(msg)
        print("-------------")


def testing(bgrid):
    from vklause import VKlause
    """ 
    cvd:[0,5]/000, 101
    bits: 16,6,1
    """
    vk1 = VKlause('vk1', {16: 0, 6: 0})
    vk2 = VKlause('vk2', {16: 0, 6: 1})
    vk3 = VKlause('vk3', {16: 1, 6: 0})
    vk4 = VKlause('vk4', {16: 1, 6: 1})
    vk5 = VKlause('vk5', {16: 0, 1: 0})
    vk6 = VKlause('vk6', {16: 0, 1: 1})
    vk7 = VKlause('vk7', {16: 1, 1: 0})
    vk8 = VKlause('vk8', {16: 1, 1: 1})
    vk9 = VKlause('vk9', {6: 0, 1: 0})
    vkA = VKlause('vkA', {6: 0, 1: 1})
    vkB = VKlause('vkB', {6: 1, 1: 0})
    vkC = VKlause('vkC', {6: 1, 1: 1})
    vkD = VKlause('vkD', {16: 0, 10: 1})
    vkE = VKlause('vkE', {16: 1, 10: 1})
    vkF = VKlause('vkF', {6: 0, 10: 1})
    vkG = VKlause('vkG', {6: 1, 10: 1})
    vkH = VKlause('vkH', {1: 0, 10: 1})
    vkI = VKlause('vkI', {1: 1, 10: 1})

    x = 1
def test_clauses(clause_dic, sat):
    hits = []
    for kn, clause in clause_dic.items():
        if 'verify' in dir(clause):     # Clause class
            if not clause.verify(sat):
                print(f"{kn}:{clause.dic} -({clause.mark}) HIT")
                hits.append((kn, clause.dic))
        elif clause.hit(sat):           # VKlause class
            print(f"{kn}:{clause.dic} - HIT")
            hits.append((kn, clause.dic))
    return hits

def sat_compatible(sat1, sat2):
    # see if case like s1[10]==0, s2[10]==1 exists (not compatible)
    bits = set(sat1).intersection(sat2)
    for bit in bits:
        if sat1[bit] != sat2[bit]:
            return False
    return True

def print_clause_dic(clauses):
    ks = sorted(clauses.keys())
    for k in ks:
        dic = clauses[k].dic
        mark = clauses[k].mark
        print(f"{k}: {dic}-{mark}")
    
def print_bitdic(bdic):
    bs = sorted(bdic)
    for b in bs:
        print(f"{b}: {bdic[b]}")