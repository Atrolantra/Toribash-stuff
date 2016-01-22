from Tkinter import Tk
import tkMessageBox
from tkFileDialog import askopenfilename, askdirectory



def chooseFiles():
	Tk().withdraw() # We don't want a full GUI, so keep the root window from appearing.
	filename = askopenfilename(title="Select a replay file", filetypes=[("Replay files", ".rpl")]) 
	return open(filename, 'r+')


def parse(replay, number=1):
	lines = replay.read().splitlines()
	parsed_lines = []
	# If the line starts with newgame, frame or joint then keep it.
	for line in lines:
		if line.split(' ')[0] in ['NEWGAME', 'FRAME', 'JOINT', 'BOUT', 'GRIP']:
			parsed_lines.append(line)
	for line in parsed_lines:
		# Remove moves not done by the player (Tori bout).
		if line.split(';')[0] in ['JOINT 1', 'GRIP 1', 'BOUT 1']:
			parsed_lines.remove(line)

	# If this is the second replay being parsed then change all references of them being the Tori bout 
	# and change them to references of the Uke bout so that the finaly replay has one player on either side.
	if number == 2:
		parsed_lines = ['JOINT 1;' + x.split(';')[1] if x.split(';')[0] in 'JOINT 0' else x for x in parsed_lines]
		parsed_lines = ['BOUT 1;' + x.split(';')[1] if x.split(';')[0] in 'BOUT 0' else x for x in parsed_lines]
		parsed_lines = ['GRIP 1;' + x.split(';')[1] if x.split(';')[0] in 'GRIP 0' else x for x in parsed_lines]

	return parsed_lines

def getMoves(replay):
	indexes = []
	move_dict = {}
	# Save the index location of each frame line.
	for i, line in enumerate(replay):
		if line.split(' ')[0] == 'FRAME':
			indexes.append(i)
	# Add an entry to our dictionary where the key is the frame number
	# and the value is a list of studd that happens between it and the next
	# frame entry. So things like joint changes and grips.
	for i, index in enumerate(indexes):
		try:
			move_dict[replay[index].split(';')[0]] = replay[index+1:indexes[i+1]]
		except (IndexError): 
			move_dict[replay[index].split(';')[0]] = replay[index+1:len(replay) + 1]
	return move_dict


def merge(replay1, replay2):
	# This is the start of our merged replay file. Initialise the list to hold the lines with the Toribash shebang.
	merged_replay_lines = ['#!/usr/bin/toribash']

	# Parse the replays.
	r1parsed = parse(replay1)
	r2parsed = parse(replay2, 2)
	r1moves = getMoves(r1parsed)
	r2moves = getMoves(r2parsed)
	
	# Merge the dictionary of frames, joints and grips for both replays.
	output = dict((k, [r1moves[k], r2moves.get(k)]) for k in r1moves)
	output.update((k, [None, r2moves[k]]) for k in r2moves if k not in r1moves)


	# Add the bouts for both players to the new replay file.
	merged_replay_lines.append(r1parsed[0])
	merged_replay_lines.append(r2parsed[0])

	# If the newgame lines are the same (both players followed the rules and used correct settings).
	if (r1parsed[1] == r2parsed[1]):
		# Add that to our new replay.
		merged_replay_lines.append(r1parsed[1])
	else: 
		print
		print "The newgame lines are not identical."
		print "This means that both players didn't not use the same settings as prescribed in the event."
		return

	# Sort the dictionary so that it is ordered by frame of the game.
	for x in sorted(output, key=lambda line: int(line.split(' ')[1])):
		# Add the frame to the replay.
		merged_replay_lines.append(x + ';')
		# For the sub list in each frame entry for each player.
		for bout in output[x]:
			# For each thing for that bout on that turn (eg joint movements and grip).
			try:
				for line in bout:
					merged_replay_lines.append(line)
			except(TypeError):
				continue

	player1 = merged_replay_lines[1].split('; ')[1]
	player2 = merged_replay_lines[2].split('; ')[1]
	out_file_address = askdirectory(title="Choose save file location")
	output = open(out_file_address + '\%s v %s merged.rpl' % (player1, player2), 'w')
	for line in merged_replay_lines:
		output.write(line + '\n')
	print "Merged replay into file: \'%s v %s merged.rpl\'" % (player1, player2)


replay1 = chooseFiles()
replay2 = chooseFiles()
merge(replay1, replay2)

# From testing.
# merge(open('C:\Steam\steamapps\common\Toribash\\replay\\tori_replay1.rpl', 'r+'),
# 	  open('C:\Steam\steamapps\common\Toribash\\replay\\tori_replay2.rpl', 'r+'))


