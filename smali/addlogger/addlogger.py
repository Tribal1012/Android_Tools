# -*- coding: utf8 -*-
import re, os, sys

dir_path = ""
smali_full_path = []
smali_relative_path = []
except_path = ['android', 'uk']
debug = 0

def addLogger(smali, target, tag):
	global debug
	f = open(smali, "rt")

	code = f.read().split("\n")

	count = 0
	countlist = list()
	loggerlist = list()

	for line in code:
		exp = re.compile(r"^\.method p[abceilortuv]{5,6} [\w]{6,11} ([\w<>]+)[\n]?\(([\w/;]*?)\)[\w/]+;?") # only constructor
		line = re.findall(exp, line)

		count += 1
		if not line:
			continue
		if debug:
			print line
		logger = "Log.i({0}, {1}({2}))".format(tag, line[0][0], line[0][1])
		print "[+] Num.{0} {1}: ".format(count, logger)
		countlist.append(count+len(countlist))
		loggerlist.append(logger)

	for i in range(0, len(countlist), 1):
		code.insert(countlist[i], loggerlist[i])

	f.close()

	f = open(target, "wt")

	for i in range(0, len(code), 1):
		f.write(code[i] + "\n")

	f.close()


def cutfullpath(full_path):
	global dir_path
	global smali_relative_path

	if full_path.find(dir_path) != -1:
		smali_relative_path.append(full_path[len(dir_path)+1:])
		return 1

	return 0

def checksmalifile(item):
	if item.find('.smali') is not -1:
		return 1	# smali file
	else:
		return 0	# is not smali file

def exportsmalipath(dir_path):
	global smali_full_path
	global smali_relative_path
	global except_path
	temp_list = os.listdir(dir_path)#.sort()

	for item in temp_list:
		if checksmalifile(item):
			smali_full_path.append(dir_path + "\\" + item)
		elif item in except_path:
			continue
		elif os.path.isfile(item):
			continue
		else:
			exportsmalipath(dir_path + "\\" + item)

def checkdir(base_path, relative_path):
	relative_dir = relative_path.split("\\")
	checkdir = base_path
	global debug
	if debug:
		print relative_dir

	for i in range(0, len(relative_dir)-1, 1):
		checkdir += "\\" + relative_dir[i]
		if not os.path.isdir(checkdir):
			os.mkdir(checkdir)

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Usage: {0} [smali path] [store path]".format(sys.argv[0])
		os._exit(0)

	print "====================================================="
	print "|                Export Smali Path                  |"
	print "====================================================="
	dir_path = sys.argv[1]
	exportsmalipath(dir_path)

	for i in range(0, len(smali_full_path), 1):
		if cutfullpath(smali_full_path[i]) != 1:
			print "Unknown Error!"
			os._exit(-1)
		print "[+] {0}".format(smali_relative_path[i])
	print "====================================================="
	print "[+] Export Smali Path Done..."
	if debug:
		print "Pause"
		raw_input("")
	print "====================================================="
	print "|                    Add Logger                     |"
	print "====================================================="
	tag = "BoB6_Tribal"
	for smali in smali_relative_path:
		target = sys.argv[2] + "\\"
		target += smali
		global debug
		if debug:
			print "[+] " + smali
			print "[+] " + target
		checkdir(sys.argv[2], smali)
		addLogger(dir_path + "\\" + smali, target, tag)
	print "====================================================="
	print "[+] Add Logger Done..."
	