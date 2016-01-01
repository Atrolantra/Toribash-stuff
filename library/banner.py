from toripy import *
session = login('mod')
names = open('names.txt', 'r')

for name in findNames(session, 'ip'):
	names.write(name + '\n')

for name in alts:
	banUser(session, name, 'ban reason', 'ban length')