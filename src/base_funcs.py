import os
import re
from colicoords import load
from addict import Dict


def gen_paths(src):
    for d in os.listdir(src):
        pth = os.path.join(src, d)
        if os.path.isdir(pth):
            yield from gen_paths(pth)
        else:
            yield pth


def load_dirs_to_dict(src, client, regex=''):
    files = [f for f in gen_paths(src) if re.search(regex, os.path.split(f)[1])]

    cell_f = client.map(load, files)
    cells = client.gather(cell_f)

    cd = Dict()
    for f, c in zip(files, cells):
        p, fname = os.path.split(f)
        name = os.path.splitext(fname)[0]
        dirs = p.split(os.sep)[1:]
        temp_d = cd
        for d in dirs:
            temp_d = temp_d[d]
        temp_d[name] = c

    return cd


def yield_class(d):
    for k, v in d.items():
        if isinstance(v, Dict):
            yield from yield_class(v)
        else:
            yield (k, v)