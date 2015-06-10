#!/usr/bin/env python3

import argparse
import re

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--file', required=True, type=argparse.FileType('r'), 
	help="File: annot.opcorpora.xml")
parser.add_argument('-o', '--output', type=argparse.FileType('tw'), 
	default="text.txt")

args = parser.parse_args()

FILE = args.file
FOUT = args.output

token_re = re.compile('\s*<token\s\S*\stext="([^"]*?[а-яё][^"]*?)".*')

buf = []
flag = 0

for line in FILE:

	if flag == 0 and "<sentence" in line:
		buf = []
		flag = 1
		buf.append(line)

		continue

	if flag == 1 and "</sentence" in line:
		flag = 0
		buf.append(line)

		lst = []
		for l in buf:
			m = token_re.match(l.lower())
			if not m is None:
				lst.append(m.group(1))

		if len(lst) > 0:
			FOUT.write(" ".join(lst) + '\n')

		continue

	buf.append(line)

print("Done")
