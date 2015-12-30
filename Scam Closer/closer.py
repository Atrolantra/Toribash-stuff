#!/usr/bin/python
from Toribash.library.toripy import *

session = login()
while True:
	thread_url = raw_input("Which thread to resolve: ")
	thread_page =  session.get(thread_url)

	# Grab thread page to get admin hash and security token value.
	s = getS(session, thread_page)
	security_token = getSecurity(session, thread_page)
	title_value = getTitle(session, thread_page)
	title_to_use = re.sub(r'\[(.*)\]', '[Solved]', title_value)
	threadnum = getThreadNum(thread_url)
	last_post = getLastPost(session, thread_page)


	# Post 'Sent'.
	postMessage(session, last_post, "Sent.", s, security_token, thread_url)

	# Close and solve.
	payload = {
	'title': title_to_use,
	't' : threadnum,
	's': s,
	'securitytoken': security_token,
	'do': 'updatethread',
	'notes': '',
	'visible': 'yes',
	'iconid': '0'
	}

	# Actually do it.
	print "Closing and solving thread"
	r = session.post(BASE_URL + '/postings.php?do=updatethread&t=%s' % (threadnum), payload)
