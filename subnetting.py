import re
from os import path

def expandSubnet(ip):
	ansList = []
	ipComponents = re.split('\.|/', ip)
	if 24 <= int(ipComponents[4]) <= 31:
		l = 32 - int(ipComponents[4])
		mask = int((8 - l) * '1' + l * '0', 2)
		ip4masked = (int(ipComponents[3]) & mask)
		for i in range(0, int(l * '1', 2) + 1):
			ipTemp = ipComponents[0:3]
			ipTemp.append(str(ip4masked + i))
			ansList.append('.'.join(ipTemp))
		return ansList
	else:
		return

def commonprefix(array):
	mini = min(array)
	maxi = max(array)
	for ind, char in enumerate(mini):
		if char != maxi[ind]:
			return mini[:ind]

def ipValidate(ipStr):
	if re.match(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", ipStr):
		return True
	else:
		return False

def ipDec2Bin(ip):
	ansList = []
	digList = ip.split('.')
	for dig in digList:
		binDig = bin(int(dig))
		binDig = binDig[2:len(binDig)]
		eightDigBin = '0' * (8 - len(binDig)) + binDig
		ansList.append(eightDigBin)
	return '.'.join(ansList)

def ipPrefixNSize(ipList):
	ansList = []
	for ip in ipList:
		if ipValidate(ip):
			ansList.append(ipDec2Bin(ip))
	prefix = commonprefix(ansList)
	size = 0
	for char in prefix:
		if char != '.':
			size += 1
	return prefix, size

def ip2Subnet(ipList):
	prefix, size = ipPrefixNSize(ipList)
	binList = prefix.split('.')
	decList = []
	for numStr in binList:
		if numStr != '':
			numStr += (8 - len(numStr)) * '0'
			decList.append(int(numStr, 2))
		else:
			binList.remove('')
	ipDecSub = '.'.join(str(num) for num in decList)
	ipDecSub += '.0' * (4 - len(binList))
	ipDecSub += '/%d' % size
	return ipDecSub

def prepareData(ipFilePath):
	ipFile = open(ipFilePath)
	ipList = []
	toExpand = []
	for line in ipFile:
		if '\n' in line:
			line = line[0:len(line)-1]
		if ipValidate(line):
			ipList.append(line)
		elif ('-' in line) or ('~' in line):
			ipStart, end = re.split('-|~', line)
			ipEnd = ipStart.split('.')[0:3]
			ipEnd.append(end)
			ipEnd = '.'.join(ipEnd)
			ipList.append(ipStart)
			ipList.append(ipEnd)
		elif ('/' in line):
			toExpand.append(line)
	ipList = sorted(ipList)
	binList = []
	for ip in ipList:
		binList.append(ipDec2Bin(ip))
	blockCount = -1
	toConsolidate = []
	prevPrefix = ''
	currPrefix = ''
	for ind, ip in enumerate(binList):
		prevPrefix = currPrefix
		currPrefix = ip[0:26]
		if currPrefix == prevPrefix:
			toConsolidate[blockCount].append(ipList[ind])
		else:
			blockCount += 1
			toConsolidate.append([])
			toConsolidate[blockCount].append(ipList[ind])
	return toConsolidate, toExpand


# EXTREMELY UGLY AND (NOT SO) EVIL TESTS

# ip = '192.168.15.123/28'
# print '\n'.join(subnet(ip))

# ipFile = open('ip.text', 'r')
# tmp = []
# for line in ipFile:
# 	if ipValidate(line):
# 		tmp.append(ipDec2Bin(line))
# prefix = commonprefix(tmp)
# print prefix
# print max(tmp)
# maxii = max(tmp)[len(prefix):]
# print maxii

# prefix, size = ipPrefixNSize('ip.text')
# binList = prefix.split('.')
# decList = []
# for numStr in binList:
# 	if numStr != '':
# 		print numStr
# 		numStr += (8 - len(numStr)) * '0'
# 		print numStr
# 		decList.append(int(numStr, 2))
# 	else:
# 		binList.remove('')
# ipDecSub = '.'.join(str(num) for num in decList)
# ipDecSub += '.0' * (4 - len(binList))
# ipDecSub += '/%d' % size
# print ipDecSub

# filePath = path.relpath("./ip.text")

# print '\n'.join(expandSubnet(ip2Subnet(filePath)))
# print ip2Subnet(filePath)

# print '12.3.4.5-122'.split('-')
# ipstart,end = re.split('-|~', '12.3.4.5~122')

# line = '12.3.4.5-122'
# if ('-' in line) or ('~' in line):
# 	ipStart, end = re.split('-|~', line)
# 	ipEnd = ipStart.split('.')[0:3]
# 	ipEnd.append(end)
# 	ipEnd = '.'.join(ipEnd)
# print ipStart, ipEnd


# MAIN

filePath = path.dirname(path.abspath(__file__))
filePath = path.join(filePath, 'ip.text')
# print ip2Subnet(prepareData(filePath))
toConsolidate, toExpand = prepareData(filePath)
for item in toConsolidate:
	print ip2Subnet(item)
for item in toExpand:
	print '\n'.join(expandSubnet(item))