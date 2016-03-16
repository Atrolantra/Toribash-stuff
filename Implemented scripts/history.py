from Toribash_stuff.library.toripy import *

session = login()
token = getToken(session)


transactions = []
offset = 0
# Load all transactions matching the parameters.
# All can be found here http://forum.toribash.com/showpost.php?p=7455329&postcount=26
while True:
	payload = {
		'owner_username': '',
		'ip': '',
		'date_from': '',
		'date_to': '',
		'offset': offset,
		'token': token
	}

	history = session.get(BASE_URL + '/tori_transaction_log.php?format=json', params=payload).json()
	offset += 50
	transactions.extend(
		history['transactions']
	)

	if offset > len(transactions):
		break

# Make a list of all of the loaded items' inventids.
items = [x['inventid'] for x in transactions]

# Send them all somewhere.
for i in items:
	sendItem(session, i, 'itemdump', shop_admin=True, override=True)


