#!/usr/bin/env python3

import argparse
import re
import os

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--file', required=True, type=argparse.FileType('r'), 
	help="File: annot.opcorpora.xml")
parser.add_argument('-d', '--dir', default="text")

args = parser.parse_args()

FILE = args.file
DIR = args.dir

if not os.path.exists(DIR):
	os.makedirs(DIR)

token_re = re.compile(
	'\s*<token\s.*?<l\s\S*\st="([^"]*?[а-яёА-ЯЁ][^"]*?)".*<g\sv="(NOUN|ADJF)"')
name_re = re.compile('\s*<text\s.*?name="([^"]+)"')
file_re = re.compile('[^\sa-zA-Zа-яА-Я0-9]')

buf = []
flag = 0
name = ''

for line in FILE:

	if flag == 0 and "<text" in line:
		buf = []
		flag = 1
		m = name_re.match(line)
		if not m is None:
			name = file_re.sub('', m.group(1))
		else:
			name = ''
		buf.append(line)

		continue

	if flag == 1 and "</text" in line:
		flag = 0
		buf.append(line)

		lst = []
		for l in buf:
			m = token_re.match(l)
			if not m is None:
				lst.append(m.group(1).lower())

		if len(lst) > 0:
			if name != '' :
				with open(DIR + "/" + name, 'tw') as f:
					f.write(" ".join(lst) + '\n')
			else:
				print("Oops")

		continue

	buf.append(line)

print("Done")
