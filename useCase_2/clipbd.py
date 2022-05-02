import os
import sys
import io
import pyperclip

def copy():
    pyperclip.copy(sys.stdin.read())
    exit()

def paste():
    buf = pyperclip.paste()
    if utf:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if sjis:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='shift-jis')
        buf = buf.replace("\x80", "")
    if csv:
        sys.stdout.write(buf.replace("\r", "").replace("\t", ","))
    elif tsv:
        sys.stdout.write(buf.replace("\r", "").replace(",", "\t"))
    else:
        sys.stdout.write(buf.replace("\r", ""))

if __name__ == "__main__":

    global csv, tsv, utf, sjis
    csv = tsv = utf = sjis = False

    if len(sys.argv) == 1:
        copy()
    else:
        for arg in sys.argv[1:]:
            if arg == "-c":
                copy()
            elif arg == "-p":
                pass
            elif arg == "-tsv":
                tsv = True
            elif arg == "-csv":
                csv = True
            elif arg == "-utf":
                utf = True
            elif arg == "-sjis" and not utf:
                sjis = True
            elif arg == "-h" or arg == "--help":
                msg = '''
Usage:
  py {} [Options]

Options:
 -c : copy to clipboad (default)
 -p : print clipboad
 -tsv : translate comma to tab, use with -p
 -csv : translate tab to comma, use with -p
 -utf : use code page utf-8, use with -p
 -sjis : use code page shift-jis, use with -p
 -h, --help : show this help '''.format(os.path.basename(__file__))
                sys.exit(msg)
            else:
                sys.exit(f'''
 {arg} no such option.''')

        paste()