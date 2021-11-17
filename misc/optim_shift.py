
from read_file import read_file
import matplotlib.pyplot as plt
import copy

class Section:

    def __init__(self, xys):
        self.n = len(xys)
        self.xs = [xy[0] for xy in xys]
        self.ys = [xy[1] for xy in xys]
        self.xmin = self.xs[ 0]
        self.xmax = self.xs[-1]
        self.i0 = 0

    def x2y(self, xx):
        if not (self.xmin <= xx and xx <= self.xmax):
            return 9999 # never select at min()
        x0 = self.xs[self.i0]
        for i in range(self.i0 + 1, self.n):
            x1 = self.xs[i]
            if x0 <= xx and xx <= x1:
                self.i0 = i - 1
                y0, y1 = self.ys[self.i0], self.ys[i]
                # not thinking about 0 divide
                return y0 + (xx - x0) * (y1 - y0) / (x1 - x0)
            x0 = x1

    @staticmethod
    def cross_at(x0, x1, f0, f1, g0, g1):
        dx, df, dg = x1 - x0, f1 - f0, g1 - g0
        xc = x0 - (f0 - g0) * dx / (df - dg)
        return xc, f0 + df * (xc - x0) / dx

    def area(self, other, dx, total=False):
        shift = copy.deepcopy(other)
        for i, x in enumerate(shift.xs):
            shift.xs[i] = x + dx
        delete = True
        shift.xmin, shift.xmax = shift.xs[0], shift.xs[-1]
        xset = sorted(set(self.xs + shift.xs))
        sw, As, x0 = None, [0, 0], xset[0]
        f0, g0 = self.x2y(x0), shift.x2y(x0)
        d0 = f0 - g0
        for x1 in xset[1:]:
            f1, g1 = self.x2y(x1), shift.x2y(x1)
            d1 = f1 - g1
            has_cross = (d0 >= 0 and d1 < 0) or (d0 <= 0 and d1 > 0)
            if has_cross:
                xc, _ = self.cross_at(x0, x1, f0, f1, g0, g1)
                if sw is None: # cross 1st
                    sw = False # = 0
                else:
                    As[sw] += sum + d0 * (xc - x0)
                    sw = not sw
                sum = d1 * (x1 - xc)
            elif sw is not None:
                sum += (d0 + d1) * (x1 - x0)
            x0, f0, g0, d0 = x1, f1, g1, d1

        if total:
            return abs(As[0] - As[1]) / 2
        else:
            return [A / 2 for A in As]

def pic_lower(xys_1, xys_2):
    sec_1, sec_2 = Section(xys_1), Section(xys_2)
    xset = sorted(set(sec_1.xs + sec_2.xs))
    x0 = xset[0]
    f0, g0 = sec_1.x2y(x0), sec_2.x2y(x0)
    d0 = f0 - g0
    xs, ys = [x0], [min([f0, g0])]
    for x1 in xset[1:]:
        f1, g1 = sec_1.x2y(x1), sec_2.x2y(x1)
        d1 = f1 - g1
        has_cross = (d0 >= 0 and d1 < 0) or (d0 <= 0 and d1 > 0)
        if has_cross:
            xc, yc = Section.cross_at(x0, x1, f0, f1, g0, g1)
            xs, ys = xs + [xc], ys + [yc]
        xs, ys = xs + [x1], ys + [min([f1, g1])]
        x0, f0, g0, d0 = x1, f1, g1, d1

    plt.plot(sec_1.xs, sec_1.ys, label="$y_1$")
    plt.plot(sec_2.xs, sec_2.ys, label="$y_2$")
    plt.plot(   xs,       ys   , label="$y_L$")
    plt.legend()
    plt.show()

def area(xys_1, xys_2):
    sec_1, sec_2 = Section(xys_1), Section(xys_2)
    a1, a2 = sec_1.area(sec_2, 0)
    if a1 > 0:
        print('y1 > y2: {:10.3f} sq.m'.format( a1))
        print('y1 < y2: {:10.3f} sq.m'.format(-a2))
    else:
        print('y1 > y2: {:10.3f} sq.m'.format(-a1))
        print('y1 < y2: {:10.3f} sq.m'.format( a2))

def diff(xys_1, xys_2, num=10, pitch=0.25):
    sec_1, sec_2 = Section(xys_1), Section(xys_2)
    dxs, das = [], []
    for i in range(-num, num + 1):
        dx = i * pitch
        da = sec_1.area(sec_2, dx=dx, total=True)
        dxs, das = dxs + [dx], das + [da]
        sec_1.i0 = 0

    plt.plot(dxs, das)
    plt.xlabel("shift (m)")
    plt.ylabel("diff. of area (m${}^2$)")
    plt.show()

if __name__ == "__main__":

    xys_1, xys_2 = read_file()
    pic_lower(xys_1, xys_2)
    area(xys_1, xys_2)
    diff(xys_1, xys_2)