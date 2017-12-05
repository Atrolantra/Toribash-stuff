from Toribash_stuff.library.toripy import *
session = login()
token = getToken(session)

# Take snapshot of inventory before spawning.
preItems = getInventory(session, token, config.username)
items_ids_pre = [i['inventid'] for i in preItems]

with open("shopping.txt", 'r') as shoppingList:
    data = [map(int, line.split()) for line in shoppingList]

for item in data:
    spawn(session, item[0], item[1])

# Take snapshot of inventory after spawning.
items = getInventory(session, token, config.username)
items_ids_post = [i['inventid'] for i in items]

# Itemids of all new items can be obtained as the difference in items compared to the first snapshot.
new_item_ids = [str(i) for i in items_ids_post if i not in items_ids_pre]

# Send all of the spawned items to magicalsack for gm use.
sendItem(session, new_item_ids, 'magicalsack', override=False, shop_admin=False, omit_errors=False)