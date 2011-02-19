def read_bytearray(fn):
    f = open(fn,'rb')
    out = []
    while True:
        line = f.read(498)
        if len(line)<498: break
        out.append(bytearray(line))
    return iter(out)
