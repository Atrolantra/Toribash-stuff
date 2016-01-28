session = login()
token = getToken(session)

# Take snapshot of inventory before spawning.
items = getInventory(session, token)
items_ids_pre = [i['inventid'] for i in items]

# Generate 5 of every force, lax and blood (2, 22, and 1) of all colors with <= 4000 qi requirement.
r = session.get(BASE_URL + '/ingame_store.php?json').json()
items = [i["itemid"] for i in r if (i["catid"] == 2 or i["catid"] == 22 or i["catid"] == 1) and i["qi"] <= 4000]
for itemid in items:    
    spawn(session, itemid, 5)

# Take snapshot of inventory after spawning.
items = getInventory(session, token)
items_ids_post = [i['inventid'] for i in items]

# Itemids of all new items can be obtained as the difference in items compared to the first snapshot.
new_item_ids = [str(i) for i in items_ids_post if i not in items_ids_pre]

# Send all of the spawned items to magicalsack for gm use.
sendItem(session, new_item_ids, 'magicalsack', override=False, shop_admin=False, omit_errors=False)