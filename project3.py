#!/usr/bin/env python

######################################################################################################################
# File name: project3.py
# Description: A program that implements a Huffman compression algorithm
# Author: Alexis Miranda
#
# Notes: N/A
#        
######################################################################################################################

#Build freq table
#num/total = freq

#Build Huffman Tree
#Use a heap to store all data
#Pull two smallest frequencies and combine them into one tree w/ head = sum of freq's
#Put combined tree back into its place in the heap
#Do this until heap is empty

#Build Compression table
#left = 0
#right = 1

#Each letter = 2 bits


import os, sys, time, heapq, math

bOps = 0

class Node(object):
	# size = 0
	def __init__(self, data):
		self.data = data
		self.lChild = []
		self.rChild = []

	def add_lChild(self, obj):
		self.lChild.append(obj)
		# self.size = self.size + 1

	def add_rChild(self, obj):
		self.rChild.append(obj)
		# self.size = self.size + 1


####################GET FILE NAME####################
def getfileName():
	#Get list of files
	dirs = os.listdir()

	#Ask user for file name
	print("Please select a file (0 to exit):")
	i = 0
	for file in dirs:
		i = i + 1
		print("(" + str(i) + ") " + file)

	choice = int(input("\nChoice: "))

	if(choice == 0):
		exit()

	i = 1
	fname = ""
	for file in dirs:
		if(i == choice):
			fname = file
		i = i+1

	if (fname == ""):
		print("Error: Invalid choice")
		exit()

	return fname
#####################################################





def createFreqTable(data):
	global bOps
	table = {}
	for i in range(len(data)):
		bOps = bOps + 1
		if(data[i] in table.keys()):
			val = table[data[i]]
			table[data[i]] = val + 1
		else:
			table[data[i]] = 1

	total = len(data)
	for i in (table.keys()):
		val = table[i]
		table[i] = val/total

	tableList = list(table.items())
	tableList = sorted(tableList, key=lambda x: x[1])
		
	return tableList


def createHTree(table):
	global bOps
	while(len(table) > 1):
		bOps = bOps + 1
		A = table.pop(0)
		B = table.pop(0)


		if(type(A) is tuple and type(B) is tuple):
			sumVal = A[1] + B[1]
			ac = Node(A)
			bc = Node(B)
		elif(type(A) is tuple and type(B) is Node):
			sumVal = A[1] + B.data
			ac = Node(A)
			bc = B
		elif(type(A) is Node and type(B) is tuple):
			sumVal = A.data + B[1]
			ac = A
			bc = Node(B)
		elif(type(A) is Node and type(B) is Node):
			sumVal = A.data + B.data
			ac = A
			bc = B

		#print(sumVal)
		n = Node(sumVal)
		n.add_lChild(ac)
		n.add_rChild(bc)

		# print(n.data)
		# print(n.lChild[0].data)
		# print(n.rChild[0].data)

		if(len(table) > 0):
			# print(">0")
			# print(table)
			ins(n, table)
			# print(table)
		else:
			# print("<=0")
			# print(table)
			table.insert(0, n)
			# print(table)

	# print(table)
	#exit()
	return table[0]

def ins(data, lst):
	# print("ins")
	# print(data)
	# print(lst)
	for i in range(len(lst)):
		if(type(lst[i]) is tuple):
			compVal = lst[i][1]
		elif(type(lst[i]) is Node):
			compVal = lst[i].data
		if(data.data <= compVal):
			lst.insert(i, data)
			return
	lst.insert(len(lst), data)
	return

def createCTable(tree):
	cTable = {}
	postOrder(tree,"",cTable)
	return cTable

def postOrder(tree, string, dic):
	global bOps
	bOps = bOps + 1 
	# if (type(tree) is tuple):
	# 	print(tree)
	# 	exit()
	if(len(tree.lChild) == 0 and len(tree.rChild) == 0):
		if(type(tree.data) is tuple):
			dic[tree.data[0]] = string
		return
	if(len(tree.lChild) > 0):
		postOrder(tree.lChild[0], string + "0", dic)
	if(len(tree.rChild) > 0):
		postOrder(tree.rChild[0], string + "1", dic)
	return


# def treeString(tree):
# 	global treeStr
# 	if(len(tree.lChild) == 0 and len(tree.rChild) == 0):
# 		if(type(tree.data) is tuple):
# 			treeStr = treeStr + "(" + str(tree.data[0]) + "," + str(tree.data[1]) + ")"
# 		return
# 	if(len(tree.lChild) > 0):
# 		treeString(tree.lChild[0])
# 		treeStr = treeStr + ",L,"
# 	if(len(tree.rChild) > 0):
# 		treeString(tree.rChild[0])
# 		treeStr = treeStr + ",R,"
# 	treeStr = treeStr + str(tree.data)
# 	return
	

def decompress(compressStr, tree):
	curr = tree
	decStr = ""
	for i in range(len(compressStr)):
		if(compressStr[i] == "0"):
			curr = curr.lChild[0]
			if(len(curr.lChild) == 0 and len(curr.rChild) == 0):
				decStr = decStr + curr.data[0]
				curr = tree
		if(compressStr[i] == "1"):
			curr = curr.rChild[0]
			if(len(curr.lChild) == 0 and len(curr.rChild) == 0):
				decStr = decStr + curr.data[0]
				curr = tree
	return decStr



while(True):
	####################Compress/decompress####################
	# print("Select an option (0 to exit):")
	# print("(1) Compress a file")
	# print("(2) Decompress a file")
	# choice = int(input("\nchoice: "))
	###########################################################

	# if(choice == 0):
	# 	exit()
	choice = 1

	#Compress a file
	if(choice == 1):
		# treeStr = ""
		fname = getfileName()
		file = open(fname)
		data = file.read()
		file.close()
		sz = len(data)
		start = time.time()
		freqTable = createFreqTable(data)
		fixedBits = len(freqTable)
		freqTable2 = freqTable[:]
		hTree = createHTree(freqTable2)
		cTable = createCTable(hTree)
		compressStr = ""
		for i in range(len(data)):
			bOps = bOps + 1
			compressStr = compressStr + cTable[data[i]]
		end = time.time()

		# fTableSize = sys.getsizeof(freqTable)
		# hTreeSize =  sys.getsizeof(hTree)
		# cTableSize = sys.getsizeof(cTable)
		# exData = fTableSize + hTreeSize + cTableSize
		# exData = exData*8

		bits = 0
		for i in range(len(freqTable)):
			ky = freqTable[i][0]
			Fq = freqTable[i][1]
			cdwrd = cTable[ky]


			bits = bits + (Fq * len(cdwrd))


		fixedBits =  math.ceil(math.log(fixedBits,2))
		cRatio = ((fixedBits - bits)/fixedBits) * 100
		total = end - start

		print("\nFile successfully encoded in " + str(float(total)) + "s")
		print(str(bits) + " avg bits per symbol required to encode the file (" + str(bits*sz) + " bits total)")
		print(str(fixedBits) + " bits per symbol required for a fixed length encoding of this file (" + str(fixedBits*sz) + " bits total)")
		print("Compression ratio: " + str(cRatio) + "%")
		print("Basic operations (freq table + h tree + c table + compression): " + str(bOps))
		print()


		cFname = input("Enter a filename for the compressed data: ")
		if not os.path.exists(os.getcwd() + "/Compressed/"):
			os.makedirs(os.getcwd() + "/Compressed/")
		cFname = os.getcwd() + "/Compressed/" + cFname

		file = open(cFname, "w")
		file.write(compressStr)
		file.close()

		# treeString(hTree)
		# print(compressStr)
		# print(treeStr)


		print("\nWould you like to decompress the file? (Y/N)")
		choice = input("\nchoice: ")

		if(choice == "Y" or choice == "y"):
			print()
			start = time.time()
			print(decompress(compressStr,hTree))
			end = time.time()
			total = end - start
			print()
			print("File successfully decompressed in " + str(float(total)) + "s")
			print()
		else:
			exit(0)




	#Decompress a file
	elif(choice == 2):
		fname = getfileName()
		file = open(fname)
	else:
		print("Error: Invalid choice")
		exit()




