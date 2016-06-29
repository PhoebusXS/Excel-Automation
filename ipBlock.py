from openpyxl import load_workbook
import re

wb = load_workbook('ip.xlsx')
ws = wb['Sheet 1']

def ipValidate(ipStr):
	if re.match(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", ipStr):
		return True
	else:
		return False

ipList = []

for col in ws.columes[0:1]:
	for cell in col:
		if ipValidate(cell.value):
			ipList.append(cell.value)

for ip in ipList:
