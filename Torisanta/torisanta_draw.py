from toripy import *
from random import shuffle

session = login()
iadmin = session.get('http://forum.toribash.com/tori_admin_item.php')

token = session.get(BASE_URL + '/bank_ajax.php?bank_ajax=get_token').json()['token']

# Open the list of names and read them into a list.
users = open('names.txt').read().splitlines()

# Go through all users and removed banned ones from the event.
# Check in batches of the API max of 25 at a time for efficiency.
for i in range(0, len(users), 25):
    # Get the user data of entrants.
    data = session.get(BASE_URL + '/bank_ajax.php', params={
        'bank_ajax': 'get_userinfo',
        'username': ','.join(users[i:i+25]),
        'token': token
    }).json()

    # If they're banned, remove them.
    for y in data['users']:
        if y['is_banned']:
            users.remove(y['username'])

sent_counter = 0
total = len(users)

# Shuffle the ordering of the list.
# Then use a sliding window of size 2 to join all the names up into a big circle.
shuffle(users)
file = open('giving.txt', 'w')
for x in range (len(users) - 1):
    file.write("%s gives to %s\n" % (users[x], users[x + 1]))
    sendPm(session, users[x], 'Secret Santa', 'You send your secret santa gift to the user %s.' % (users[x + 1]))
    sent_counter += 1
    print "Sent %i of %i" % (sent_counter, total)
file.write("%s gives to %s\n" % (users[-1], users[0]))
sendPm(session, users[-1], 'Secret Santa', 'You send your secret santa gift to the user %s.' % (users[0]))
sent_counter += 1
print "Sent %i of %i" % (sent_counter, total)

file.close()