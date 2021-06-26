import os
import re # Regular Expression : 正規表現
import sys

def search(words):
    s = words[0]
    if len(words) > 1:
        for word in words[1:]:
            s += "|" + word
        s = "(" + s + ")" # (a|b|c) : a or b or c
    reg = re.compile(s, re.IGNORECASE)
    for p in os.environ["PATH"].split(";"):
        if reg.search(p):
            print(p)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        search(sys.argv[1:])
    else:
        exit("\n Usage : {} word [word ...]\n".\
            format(os.path.basename(__file__)))