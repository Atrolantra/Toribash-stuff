from toripy import *
session = login('mod')
names = open('names.txt', 'r')

for name in names.read.splitlines():
	banUser(session, name, 'Reason', 'Length')
	
	