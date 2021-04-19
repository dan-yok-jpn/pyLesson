from quadFnc import QuadFnc

f = QuadFnc(1, 6, -1)
print('solution of {}=0 : x={}'.format(f, f.solve()))
f.plot(-8, 2, 0.2)
