# -*- coding: utf8 -*-
import re, os, sys

debug = 0

def Check_Main_Activity(activity):
	code = activity[1]

	if debug:
		print activity
	
	exp = re.compile(r"[\s]+<intent-filter[ \S]*?>([\s\w<>\"\/\=\-\.\:]+?)</intent-filter>\n") 
	intent_filter = re.findall(exp, code)

	if not code:
		return 0

	for tag in intent_filter:
		exp = re.compile(r"[\s]+<category[ \S]*?android:name=\"([\w.]+)\"[ \S]*?/>\n") 
		result = re.findall(exp, tag)
		if not result:
			continue
		if result[0].find("LAUNCHER") != -1:
			print "Find : " + result[0]
			return 1

	return 0

def Find_Main_Activity(Manifest_Path):
	global debug
	f = open(Manifest_Path, "rt")

	code = f.read()

	count = 0

	exp = re.compile(r"[\s]+<activity[ \S]+?android:name=\"([\w.]+)\"[ \S]*?>([\s\w<>\"\/\=\-\.\:]+?)</activity>\n") # 
	activity = re.findall(exp, code)

	if not activity:
		return "[-] Error. Don't found MainActivity."

	for i in range(0, len(activity), 1):
		if Check_Main_Activity(activity[i]) != 0:
			name = activity[i][0]
			print "[+] Num.{0} : {1}".format(count, name)
			count += 1
	
	if count != 1:
		return "[-] Error. MainActivity should only one."

	return name

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "Usage: {0} [AndroidManifest.xml Path]".format(sys.argv[0])
		os._exit(0)

	print "====================================================="
	print "|               Find Main Activity                  |"
	print "====================================================="
	Manifest_Path = sys.argv[1]
	print "[+] File Path : " + Manifest_Path
	Main_Activity = Find_Main_Activity(Manifest_Path)
	print "[+] Main Activity : " + Main_Activity
	print "====================================================="
	print "[+] Export Smali Path Done..."
