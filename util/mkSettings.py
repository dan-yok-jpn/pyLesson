import os
import sys

def usage(path_to_prog):

    prg = os.path.basename(path_to_prog)
    msg = '\n Usage : python {} path_to_python'.format(prg)
    print(msg, file=sys.stderr)
    sys.exit()

def replace_all(path_to_py):

    path_to_py = path_to_py.replace('\\', '\\\\')
    with open('template', 'r') as f:
        while True:
            line = f.readline()
            if not line: # EOF
                break
            if '_PYTHONHOME_' in line:
                line = line.replace('_PYTHONHOME_', path_to_py)
            print(line[:-1])

if __name__ == '__main__':

    if len(sys.argv) == 2:
        replace_all(sys.argv[1])
    else:
        usage(sys.argv[0])
