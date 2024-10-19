import chardet


with open('/home/bangtable001/data/flag.txt', 'rb') as file:
	data1 = file.read()

with open('/home/bangtable001/data/flag_test.txt', 'w', encoding='utf-8') as file:
	file.write("False")

with open('/home/bangtable001/data/flag_test.txt', 'rb') as file:
	data2 = file.read()

print("data : " + data1.hex())
print("test : " + data2.hex())
