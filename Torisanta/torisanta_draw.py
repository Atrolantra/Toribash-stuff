from Toribash_stuff.library.toripy import *
from random import shuffle

session = login()
iadmin = session.get('http://forum.toribash.com/tori_admin_item.php')

token = session.get(BASE_URL + '/bank_ajax.php?bank_ajax=get_token').json()['token']

# Open the list of names and read them into a list.
users = open('names.txt').read().splitlines()
to_remove = []

# Go through all users and removed banned ones from the event.
for i in range(0, len(users), 25):
    # Get the user data of entrants.
    data = session.get(BASE_URL + '/bank_ajax.php', params={
        'bank_ajax': 'get_userinfo',
        'username': ','.join(users[i:i+25]),
        'token': token
    }).json()

    # If they're banned, queue them up to be removed.
    for y in data['users']:
        if y['is_banned'] == True:
            to_remove.append(y['username'])

# Go through the list of users to be removed and take them off the list.
for user in to_remove:
    users.remove(user)

print users

# Shuffle the ordering of the list.
# Then use a sliding window of size 2 to join all the names up into a big circle.
shuffle(users)
file = open('giving.txt', 'w')
for x in range (len(users) - 1):
	file.write("%s gives to %s" % (users[x], users[x + 1]))
file.write("%s gives to %s" % (users[-1], users[0]))

Send the pms.
exchanges = open("giving.txt", "r").read().splitlines()
sent_counter = 0
total = len(exchanges)
for line in exchanges:
    names = line.split(" gives to ")
    pm_recipient = names[0]
    present_to = names[1]
    sendPm(pm_recipient, 'Secret Santa', 'You send your secret santa gift to the user %s.' % (present_to)) 
    sent_counter += 1
    print "Sent %i of %i" % (sent_counter, total)