from toripy import *

session = login()
token = getToken(session)
# for line in open("send_to_list_existing.txt", "r").read().splitlines():
#         pass
#         #send the existing item

preItems = getInventory(session, token, config.username)
invent_ids_pre = [i['inventid'] for i in preItems]
for line in open("send_to_list_new.txt", "r").read().splitlines():
    spawn(session, line.split(" ")[1], 1)

    #spawn a new item of that ID
    #find out it's id by taking the difference from my snapshot earlier
    #send it
items = getInventory(session, token, config.username)
invent_ids_post = [i['inventid'] for i in items]

#in here map the new inventids to that item's itemid then go through the list and send the inventid
#that corresponds to that winner's itemid
new_invent_ids = [str(i) for i in invent_ids_post if i not in invent_ids_pre]
print new_invent_ids