#!/usr/bin/env python3

import sys

def main():
	for line in sys.stdin:
		words = line.split()

		for i in range(len(words)):

			one = words[i]
			if i < len(words) - 1:
				two = words[i + 1]
				if i < len(words) - 2:
					three = words[i + 2]

					print("%s %s %s %i" % (one, two, three, 1))
				else:
					print("%s %s %i" % (one, two, 1))

if __name__ == '__main__':
	main()
