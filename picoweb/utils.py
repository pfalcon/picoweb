import re


qu_re = re.compile(r"%([0-9A-Fa-f]{2})")

def unquote_plus(s):
    def decode(s):
        val = int(s.group(1), 16)
        return chr(val)
    return qu_re.sub(decode, s.replace("+", " "))

def parse_qs(s):
    res = {}
    if s:
        pairs = s.split("&")
        for p in pairs:
            vals = [unquote_plus(x) for x in p.split("=", 1)]
            if len(vals) == 1:
                vals.append(True)
            if vals[0] in res:
                res[vals[0]].append(vals[1])
            else:
                res[vals[0]] = [vals[1]]
    return res

#print(unquote("foo"))
#print(unquote("fo%41o+bar"))
