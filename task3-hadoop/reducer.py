#!/usr/bin/env python3

import sys

def main():
	curr_value = []

	curr_couple = 0
	curr_triple = 0

	for line in sys.stdin:

		prs = line.split()
		if len(prs) == 4:
			one, two, three, count = prs
		else:
			one, two, count = prs
			three = ''
		
		count = int(count)

		if len(curr_value) == 3 and curr_value[0] == one and curr_value[1] == two:
			curr_couple += count

			if curr_value[2] == three:
				curr_triple += count
			else:
				if len(curr_value) == 3 and curr_value[2] != '':
					print("%s %s %s %i %i %f" % \
						(curr_value[0], curr_value[1], curr_value[2], \
							curr_triple, curr_couple, curr_triple/curr_couple))
			
				curr_value = [ one, two, three ]
				curr_triple = count

		else:
			if len(curr_value) == 3 and curr_value[2] != '':
				print("%s %s %s %i %i %f" % \
					(curr_value[0], curr_value[1], curr_value[2], \
						curr_triple, curr_couple, curr_triple/curr_couple))
			
			curr_value = [ one, two, three ]
			curr_couple = count
			curr_triple = count

	if len(curr_value) == 3 and curr_value[2] != '':
		print("%s %s %s %i %i %f" % \
			(curr_value[0], curr_value[1], curr_value[2], \
				curr_triple, curr_couple, curr_triple/curr_couple))

if __name__ == '__main__':
	main()