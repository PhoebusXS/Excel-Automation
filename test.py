import re

def ipValidate(ipStr):
	a = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}$", ipStr)
	if a:
		return True
	else:
		return False

print ipValidate('192.159.123.4/12')