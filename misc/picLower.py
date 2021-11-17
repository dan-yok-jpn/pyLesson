
from read_file import read_file
import matplotlib.pyplot as plt

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

def cross_at(x0, x1, f0, f1, g0, g1):
    dx, df, dg = x1 - x0, f1 - f0, g1 - g0
    xc = x0 - (f0 - g0) * dx / (df - dg)
    return xc, f0 + df * (xc - x0) / dx

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
            xc, yc = cross_at(x0, x1, f0, f1, g0, g1)
            xs, ys = xs + [xc], ys + [yc]
        xs, ys = xs + [x1], ys + [min([f1, g1])]
        x0, f0, g0, d0 = x1, f1, g1, d1

    plt.plot(sec_1.xs, sec_1.ys, label="$y_1$")
    plt.plot(sec_2.xs, sec_2.ys, label="$y_2$")
    plt.plot(   xs,       ys   , label="$y_L$")
    plt.legend()
    plt.show()

if __name__ == "__main__":

    xys_1, xys_2 = read_file() # instead of actual file reading
    pic_lower(xys_1, xys_2)