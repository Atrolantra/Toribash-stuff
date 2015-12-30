from Toribash_stuff.library.toripy import *

session = login()

counter = 0
for name in open("send_to_list.txt", "r").read().splitlines():
	sendItem(session, first_item_id_of_batch_buy + counter, name)
	counter += 1
