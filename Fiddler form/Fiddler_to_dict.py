import json
import pprint
data = []
for line in open("fiddlerform.txt", "r").read().splitlines():
	line = line.split()
	if len(line) > 2:
		line = [line[0], ' '.join(line[1:])]
	if len(line) == 1:
		line.append('')
	data.append(line)

f = open('result.txt', 'w')
pprint.pprint(dict(data), stream = f)
f.close()

f = open('result.txt', 'r')
fin = open('result_finished.txt', 'w')
fin.write("payload = {\n")

for line in f.read().splitlines():
	if line[0] == '{':
		line = line.replace('{', ' ')
	if line[-1] == '}':
		line = line[:-1]
	fin.write(line + '\n')

fin.write("}")
f.close()
fin.close()

