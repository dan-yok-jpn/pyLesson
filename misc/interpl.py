import os
import sys
import csv
import numpy
def usage():
    msg = '''
  使い方 : python {} [オプション] [csv ファイル名]
  オプション :
    -d# : 分割数 (既定 : -d2) 
    -f# : 少数点以下の桁数 (既定 : なし)
    -h, --help : この表示'''.format(sys.argv[0])
    sys.exit(msg)
def show_results(vs):
    sot = fmt.format(vs[0])
    for v in vs[1:]:
        sot += fmt_.format(v)
    print(sot)
def interpl(file_path, div):
    if file_path:
        if not os.path.exists(file_path):
            sys.exit('\n ERROR : {} no such file'.\
                format(file_path))
        f = open(file_path)
    else:
        f = sys.stdin
    rows = csv.reader(f)
    try:
        row = next(rows)
        v0  = numpy.array(row, dtype="float")
    except: # 1st line was header
        header = row[0]
        for col in row[1:]:
            header += "," + col
        print(header)
        v0 = numpy.array(next(rows), dtype="float")
    show_results(v0)
    for row in rows:
        v1 = numpy.array(row, dtype="float")
        dv = (v1 - v0) / div
        for i in range(1, div):
            show_results(v0 + i * dv)
        show_results(v1)
        v0 = v1
    f.close()
if __name__ == "__main__":
    global fmt, fmt_
    file_path, div, fmt = None, 2, "{}"
    if "-h" in sys.argv or "--help" in sys.argv:
        usage()
    for arg in sys.argv[1:]:
        if arg[0] == "-":
            arg_1, arg_2 = arg[1], arg[2:]
            if   arg_1 == "d" and arg_2.isdigit():
                div = int(arg_2)
            elif arg_1 == "f" and arg_2.isdigit():
                fmt = "{:." + arg_2 + "f}"
            else:
                sys.exit("\n ERROR : unknown option {}.".\
                    format(arg))
        else:
            file_path = arg
    fmt_ = "," + fmt
    interpl(file_path, div)