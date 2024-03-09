import matplotlib.pyplot as plt
import numpy as np
import random

def main():
	# arr = list(map(int, input("Enter your array:\n").split()))
	arr = sorted(np.random.randint(1, 101, random. randint(15, 26)))
	# key = int(input("Enter your key:\n"))
	key = random.choice(arr)
	n = len(arr)
	x_label = range(0, n)
	plt.title(f'Binary Search Algorithm \n Key: {key}')
	plt.pause(1)

	ans, beg, end = -1, 0, n - 1
	while beg <= end:
		bars = plt.bar(x_label, arr, align='edge', width=0.75)
		for i in range(beg, end + 1):
			bars[i].set_color('g')
			plt.text(x=i, y=arr[i]+1, s=f"{arr[i]}")
		plt.draw()
		mid = beg + (end - beg) // 2
		bars[mid].set_color('b')
		if arr[mid] == key:
			bars[mid].set_color('r')
			ans = mid
			break
		elif arr[mid] > key:
			end = mid - 1
		else:
			beg = mid + 1
		plt.pause(1)
		plt.clf()
	plt.show()

if __name__ == '__main__':
	main()

print("hello world")