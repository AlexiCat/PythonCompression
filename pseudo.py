createFreqTable(data):
	table = {}
	for i in range(len(data)):
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


createHTree(table):
	while(len(table) > 1):
		A = table.pop()
		B = table.pop()


		sumVal = A.data + B.data
		ac = Node(A)
		bc = Node(B)


		n = Node(sumVal)
		n.add_lChild(ac)
		n.add_rChild(bc)


		if(len(table) > 0):
			insert(n, table)
		else:
			table.insert(0, n)


	return table


createCTable(tree):
	cTable = {}
	postOrder(tree,"",cTable)
	return cTable

postOrder(tree, string, dic):
	if(tree.lChild == NULL and tree.rChild == NULL):
		dic[tree.data] = string
		return
	if(tree.lChild != NULL):
		postOrder(tree.lChild, string + "0", dic)
	if(ltree.rChild != NULL):
		postOrder(tree.rChild, string + "1", dic)
	return


	

decompress(compressStr, tree):
	curr = tree.head
	decStr = ""
	for i in range(len(compressStr)):
		if(compressStr[i] == "0"):
			curr = curr.lChild
			if(curr.lChild == NULL and curr.rChild == NULL):
				decStr = decStr + curr.data
				curr = tree.head
		if(compressStr[i] == "1"):
			curr = curr.rChild
			if(curr.lChild == NULL and curr.rChild == NULL):
				decStr = decStr + curr.data
				curr = tree
	return decStr


compress(string):
	for i in range(len(string)):
		compressStr = compressStr + cTable[data[i]]