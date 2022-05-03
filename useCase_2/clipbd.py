import os
import sys
import io
import pyperclip

COPY  = True
PASTE = False

def usage():

    print('''
Usage:
    py {} [Options]
Options:
    -c    : copy to clipboad (default)
    -p    : print clipboad
    -tsv  : replace comma to tab
    -csv  : replace tab to comma
    -utf  : encoding utf-8
    -sjis : encoding shift-jis (default)
    -h    : show this help
'''.format(os.path.basename(__file__)),
    file = sys.stderr)

def copy(csv, tsv, encoding):

    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding = encoding)

    buf = sys.stdin.read()
    if sjis:
        buf = buf.replace("\x80", "")

    if csv:
        pyperclip.copy(buf.replace("\t", ","))
    elif tsv:
        pyperclip.copy(buf.replace(",", "\t"))
    else:
        pyperclip.copy(buf)

def paste(csv, tsv, utf, sjis):

    buf = pyperclip.paste().replace("\r", "")

    if utf:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    elif sjis:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="shift-jis")
        buf = buf.replace("\x80", "")

    if csv:
        sys.stdout.write(buf.replace("\t", ","))
    elif tsv:
        sys.stdout.write(buf.replace(",", "\t"))
    else:
        sys.stdout.write(buf)

if __name__ == "__main__":

    mode = COPY
    csv, tsv  = False, False
    sjis, utf = True,  False

    for arg in sys.argv[1:]:
        if arg == "-c":
            mode = COPY
        elif arg == "-p":
            mode = PASTE
        elif arg == "-tsv":
            tsv = True
        elif arg == "-csv":
            csv = True
        elif arg == "-utf":
            sjis, utf = False, True
        elif arg == "-sjis":
            sjis, utf = True,  False
        elif arg ==  "-h":
            usage()
            sys.exit()
        else:
            usage()
            sys.exit(f'\n ERROR !!! {arg} no such option.')

    if mode == COPY:
        copy(csv, tsv, "utf-8" if utf else "shift-jis")
    else:
        paste(csv, tsv, utf, sjis)
