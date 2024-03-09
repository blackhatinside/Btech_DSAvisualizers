import matplotlib.pyplot as plt
import numpy as np

def main():
	n = 10
	lst = np.random.randint(0, 100, n)
	x_label = np.arange(1, n + 1, 1)
	fig = plt.figure()
	for i in range(n):
		for j in range(0, n - 1 - i):
			bars = plt.bar(x_label, lst)
			bars[j].set_color('g')
			bars[j + 1].set_color('g')
			plt.draw()
			if lst[j] > lst[j + 1]:
				plt.draw()
				bars[j].set_color('r')
				bars[j + 1].set_color('r')
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
			plt.pause(0.001)
			plt.clf()
	plt.show()

if __name__ == '__main__':
	main()

print("hello world")