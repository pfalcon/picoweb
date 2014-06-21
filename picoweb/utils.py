import re


qu_re = re.compile(r"%([0-9A-Fa-f]{2})")

def unquote_plus(s):
    def decode(s):
        val = int(s.group(1), 16)
        return chr(val)
    return qu_re.sub(decode, s.replace("+", " "))

def parse_qs(s):
    res = {}
    pairs = s.split("&")
    for p in pairs:
        k, v = p.split("=", 1)
        k, v = unquote_plus(k), unquote_plus(v)
        if k in res:
            res[k].append(v)
        else:
            res[k] = [v]
    return res

#print(unquote("foo"))
#print(unquote("fo%41o+bar"))
