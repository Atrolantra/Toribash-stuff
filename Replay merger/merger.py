# def chooseFiles():
# 	try: 
# 		replay1 = (raw_input("Input file path link for first replay: "))
# 		replay1open = open(replay1, 'r+')
# 		replay2 = (raw_input("Input file path link for second replay: "))
# 		while replay2 == replay1:
# 			print "Replay 2 may not be the same as replay 1."
# 			replay2 = (raw_input("Input file path link for second replay: "))
# 		replay2open = open(replay2, 'r+')

# 	except IOError as error: 
# 		print str(error) + '\nTry again.'
# 		return chooseFiles()
# 	return (replay1open, replay2open)

def parse(replay, number=1):
	# Remove everything but the game, frame, and joint lines.
	lines = replay.read().splitlines()
	parsed_lines = []
	# If the line starts with newgame, frame or joint then keep it.
	for line in lines:
		if line.split(' ')[0] in ['NEWGAME', 'FRAME', 'JOINT', 'BOUT', 'GRIP']:
			parsed_lines.append(line)
	for line in parsed_lines:
		# Remove moves not done by the player.
		if line.split(';')[0] in ['JOINT 1', 'GRIP 1', 'BOUT 1']:
			parsed_lines.remove(line)

	# If this is the second replay being parsed then change all references of them being Tori 
	# and change them to references of Uke.
	if number == 2:
		parsed_lines = ['JOINT 1;' + x.split(';')[1] if x.split(';')[0] in 'JOINT 0' else x for x in parsed_lines]
		parsed_lines = ['BOUT 1;' + x.split(';')[1] if x.split(';')[0] in 'BOUT 0' else x for x in parsed_lines]
		parsed_lines = ['GRIP 1;' + x.split(';')[1] if x.split(';')[0] in 'GRIP 0' else x for x in parsed_lines]

	for line in parsed_lines: print line
	return parsed_lines



def merge(replay1, replay2):
	# This is the start of our merged replay file. Initialise the list to hold the lines with the Toribash shebang.
	merged_replay_lines = ['#!/usr/bin/toribash']

	# Parse the replays.
	r1parsed = parse(replay1)
	r2parsed = parse(replay2, 2)

	# Add the bouts for both players to the new replay file.
	merged_replay_lines.append(r1parsed[0])
	merged_replay_lines.append(r2parsed[0])

	# If the newgame lines are the same (both players followed the rules and used correct settings)
	# then add that to our new replay.
	if (r1parsed[1] == r2parsed[1]):
		merged_replay_lines.append(r1parsed[1])

	
	print merged_replay_lines


# replay1, replay2 = chooseFiles()
merge(open('C:\Steam\steamapps\common\Toribash\\replay\\tori_replay.rpl', 'r+'),
	  open('C:\Steam\steamapps\common\Toribash\\replay\\tori_replay2.rpl', 'r+'))
# Get them to pick an output file name