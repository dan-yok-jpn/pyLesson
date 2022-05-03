import os
import sys
import io
import pyperclip

COPY  = True
PASTE = False

def usage():

    bat = os.path.basename(__file__).replace(".py", ".bat")
    print(f'''
Usage:
    {bat} [Options]
Options:
    -c    : copy to clipboad (default)
    -p    : print clipboad
    -tsv  : replace comma to tab
    -csv  : replace tab to comma
    -utf  : convert charset to utf-8, use with -p
    -h    : show this help
Exsample:
    {bat} -tsv < foo.csv ............ file to clipboad
    {bat} -p -csv -utf > utf.csv .... clipboad to file
''', file = sys.stderr)

def copy(csv, tsv):

    buf = sys.stdin.buffer.read()
    try:
        buf = buf.decode("shift-jis")
    except:
        buf = buf.decode("utf-8")

    if csv:
        buf = buf.replace("\t", ",")
    elif tsv:
        buf = buf.replace(",", "\t")

    pyperclip.copy(buf)

def paste(csv, tsv, utf):

    buf = pyperclip.paste().replace("\r", "")

    if utf:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    if csv:
        print(buf.replace("\t", ","))
    elif tsv:
        print(buf.replace(",", "\t"))
    else:
        print(buf)

if __name__ == "__main__":

    mode = COPY
    csv, tsv, utf = False, False, False

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
            utf = True
        elif arg ==  "-h":
            usage()
            sys.exit()
        else:
            usage()
            sys.exit(f'\n ERROR !!! {arg} no such option.')

    if mode == COPY:
        copy(csv, tsv)
    else:
        paste(csv, tsv, utf)
