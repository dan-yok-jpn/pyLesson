import os
import sys
import pyperclip

def copy(tsv=None):
    if tsv:
        pyperclip.copy(sys.stdin.read().replace(",", "\t"))
    else:
        pyperclip.copy(sys.stdin.read())

def paste(csv=None):
    if "-unicode" in sys.argv:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if csv:
        sys.stdout.write(pyperclip.paste().replace("\r", "").replace("\t", ","))
    else:
        sys.stdout.write(pyperclip.paste().replace("\r", ""))

if __name__ == "__main__":

    if len(sys.argv) == 1 or "-c" in sys.argv:
        copy()
    elif "-tsv" in sys.argv:
        copy(True)
    elif "-p" in sys.argv:
        paste()
    elif "-csv" in sys.argv:
        paste(True)
    else:
        exit("\n ERROR {} unknown option(s) {}".\
        format(os.path.basename(sys.argv[0]), sys.argv[1:]))
