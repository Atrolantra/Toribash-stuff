from toripy import *
session = login('mod')
name_list = findNames(session, "ip here")
for x in name_list:
	banUser(session, x, "reason here", "duration here")