#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import re
import argparse

### ArgParse configuration.
parser = argparse.ArgumentParser(description='Format a file into a table-like view.')
parser.add_argument("-i","--input", type=str, metavar="N", required=True, help="the file with the data to be formatted (required)")
parser.add_argument("-o","--output", type=str, metavar="N", default="output", help="the file with the formated data (default: output)")
parser.add_argument("-c","--columns", type=int, metavar="N", default=2, help="the amount of columns (default: 2)")
parser.add_argument("-w","--width", type=int, metavar="N", nargs='+', default=[], help="the width(s) between each column (default: 40)")
parser.add_argument("-n","--names", type=str, metavar="N", nargs='+', default=[], help="the name(s) for the columns")
parser.add_argument("-b","--borders", action="store_true", help=" draws the table borders.")
args = parser.parse_args()

### Variable Extraction
input_arg = args.input
output_arg = args.output
line_arg = args.columns
width_arg = args.width
table_arg = args.borders
name_arg = args.names

### Evaluate if header names will be drawed.
if (len(name_arg) > 0):
	name_eval = True
else:
	name_eval = False

### Evaluate if the width will be auto calculated.
if (len(width_arg) == 0):
	width_eval = True
else:
	width_eval = False

### Read the input.
with codecs.open(input_arg, "r", "utf-8") as text_file:
	input = text_file.read()

result = u""

### Calculate widths if not specified.
if width_eval:
	count = 0
	for x in range(0, line_arg):
		width_arg.append(0)
	for line in input.split("\n"):
		linetemp = re.sub("[\r\n\b]", "", line)
		if len(linetemp) + 1 > width_arg[count]:
			width_arg[count] = len(linetemp) + 1
		if count < line_arg - 1:
			count += 1
		else:
			count = 0

### Calculate the longitude.
longitude = 0
tempvalue = 0
for i in range(0, line_arg):
	longitude += width_arg[tempvalue] + 1
	if (tempvalue + 1) < len(width_arg):
		tempvalue += 1
longitude += 1

### Draws the header names.
if name_eval and table_arg:
	count = 0
	### Header top
	width_count = 0
	breaks = 1 + width_arg[width_count]
	if (width_count + 1) < len(width_arg):
		width_count += 1
	
	for x in range(0, longitude):
		if (x == 0):
			result += u"╔"
		elif (x == longitude - 1):
			result += u"╗"
		elif (x == breaks):
			result += u"╦"
			breaks += 1 + width_arg[width_count]
			if (width_count + 1) < len(width_arg):
				width_count += 1
		else:
			result += u"═"
	result += "\n"

	### Header names
	width_count = 0
	line_result = ""
	column = 1
	linetemp = ""
	count = 0
	for name in name_arg:
		count += 1
		if (count > line_arg):
			break
		line_result += u"║"
		line_result += name

		for x in range(0, (width_arg[width_count] - len(name))):
			line_result += u" "
		
		if (width_count + 1) < len(width_arg):
			width_count += 1
		column += 1
	
	if (len(line_result) != longitude):
		breaks = len(line_result) + 1 + width_arg[width_count]
		line_result += u"║"
		if (width_count + 1) < len(width_arg):
			width_count += 1
		
		for x in range(len(line_result), longitude):
			if (x == breaks):
				line_result += u"║"
				breaks += 1 + width_arg[width_count]
				if (width_count + 1) < len(width_arg):
					width_count += 1
			else:
				line_result += " "
	

	line_result += "\n"
	result += line_result

### Top border
count = 0
if table_arg:
	width_count = 0
	breaks = 1 + width_arg[width_count]
	if (width_count + 1) < len(width_arg):
		width_count += 1
	
	for x in range(0, longitude):
		if (x == 0):
			if name_eval:
				result += u"╠"
			else:
				result += u"╔"
		elif (x == longitude - 1):
			if name_eval:
				result += u"╣"
			else:
				result += u"╗"
		elif (x == breaks):
			if name_eval:
				result += u"╬"
			else:
				result += u"╦"
			breaks += 1 + width_arg[width_count]
			if (width_count + 1) < len(width_arg):
				width_count += 1
		else:
			result += u"═"
	result += u"\n"

### Data lines
column = 1
line_result = ""
width_count = 0
for line in input.split("\n"):
	linetemp = re.sub("[\r\n\b]", "", line)
	if (len(linetemp) != 0):
		if (count == line_arg):
			line_result += u"\n"
			count = 0
			width_count = 0
		if (table_arg and count == 0):
			line_result += u"║"
		else:
			line_result += u""

		line_result += unicode(linetemp.replace("\n", "").replace("\r", ""))

		for x in range(0, (width_arg[width_count] - len(linetemp))):
			line_result += u" "
		if (table_arg):
			line_result += u"║"
			if (width_count + 1) < len(width_arg):
				width_count += 1
		else:
			if (width_count + 1) < len(width_arg):
				width_count += 1
		count += 1
		column += 1
		
	if (column > line_arg):
		result += line_result
		line_result = ""
		column = 1

### Complete the line if it isn't.
if (len(line_result) != longitude and len(line_result) != 0):
	breaks = len(line_result) - 1 + width_arg[width_count]
	if (width_count + 1) < len(width_arg):
		width_count += 1
	for x in range(len(line_result) - 1, longitude):
		if (x == breaks):
			line_result += u"║"
			breaks += 1 + width_arg[width_count]
			if (width_count + 1) < len(width_arg):
				width_count += 1
		else:
			line_result += " "

result += line_result

### Botton border.
width_count = 0
if table_arg:
	result += "\n"
	breaks = 1 + width_arg[width_count]
	if (width_count + 1) < len(width_arg):
		width_count += 1
	for x in range(0, longitude):
		if (x == 0):
			result += u"╚"
		elif (x == longitude - 1):
			result += u"╝"
		elif (x == breaks):
			result += u"╩"
			breaks += 1 + width_arg[width_count]
			if (width_count + 1) < len(width_arg):
				width_count += 1
		else:
			result += u"═"

### Write the output.
with codecs.open(output_arg, "w", "utf-8") as text_file:
	text_file.write(result)
