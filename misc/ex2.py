import os

def search(word):
    WORD = word.upper()
    for p in os.environ["PATH"].split(";"):
        if WORD in p.upper():
            print(p)

# search("python")
# search("Program Files")
search("windows")