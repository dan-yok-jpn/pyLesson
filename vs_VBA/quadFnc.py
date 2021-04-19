import numpy as np
import matplotlib.pyplot as plt

class QuadFnc:

	def __init__(self, a, b, c):
		self.a = a
		self.b = b
		self.c = c

	def f(self, x):
		return (self.a * x + self.b) * x + self.c

	def solve(self):
		if self.a == 0: return (np.nan, np.nan)
		d  = pow(self.b * self.b - 4 * self.a * self.c, 0.5)
		a2 = 2 * self.a
		return ((-self.b - d) / a2, (-self.b + d) / a2)

	def plot(self, xmin, xmax, xdiv):
		n = int((xmax - xmin) / xdiv)
		x = np.linspace(xmin, xmax, n)
		y = (self.a * x + self.b) * x + self.c
		plt.plot(x, y)
		plt.title('$' + self.__str__() + '$')
		plt.xlim(xmin, xmax)
		plt.grid()
		plt.show()

	def __str__(self):
		return 'f(x)={}x^2{:=+}x{:=+}'.format(self.a, self.b, self.c)

if __name__ == '__main__':

	myFnc = QuadFnc(2, 3, -4)
	print('solutions omyFnc {}=0 : x={}'.format(myFnc, myFnc.solve()))
	myFnc.plot(-3, 1, 0.1)
