#Toribash Replay Merger

##Requirements
Python 2.7.10 (though you can probably get away with a few version below too if you're really keen...)

##How to use
Simply run the file: *merger.py*  
You will then be asked to input the first and second replay files that are to be merged.  
Input the whole path to the file like this *C:\Steam\steamapps\common\Toribash\\replay\\tori_replay1.rpl*  
If the file isn't there the program will let you know and you can try again.  
The rplays can't both be the same either and the program will let you know that too.  

The only other issue you may come across is if both players who have submitted the replay haven't used the exact same game settings. This information is stored towards the beginning of a replay file and looks something like this:  
>*NEWGAME 0;500 10 15 0 0 2 500 0 0 classic 0 0 100 0 0 0 1 0 2 0 0 0 0 0 0 0.000000 0.000000 -9.820000 0 0 0 0 8*  

Really this issue shouldn't come up as long as you prescribe easy to follow gamerules like just a mod name or a mod name and altered engage-distance. If both users's settings match up then the program will go ahead and mash the replays together and spit you out a file called *'player1 v player2 merged.rpl'* which will appear in whatever directory/folder you're running the script from.

##Assumptions
The script assumes that both players are playing as the Tori bout (the default character you control in free play) and converts one to the uke bout automatically. So it is important that both players play as Tori or else the merged replay outcome will have only one player since the script doesn't take Uke's moves into account.

The script should be able to handle any mod or settings so there's no need to set a limit on turn frames or anything like that unless you want to.

##Example
I have included three replays in this directory:  
*tori_replay1.rpl*  
*tori_replay2.rpl*  
*Solax v Solax merged.rpl*  

The first two are stand alone files I made of me doing some random moves as Tori. These were then fed into the script and the third file was produced. Feel free to watch all three to get a better idea of how this looks and works in practice.

##How It Works (If you're interested)
If you're curious about how it works and don't want to read my (lovingly commented) python code then this is the section for you.

The general theory is that replay files are full of a lot of garbage that isn't really necessary. My guess is that it's saved there to make running the replay in the future faster since the physics don't need to be calculated again. Happily for us we can cut away most of this and run a barebones version that still works perfectly. The most important lines in a replay are the FRAME and JOINT lines. They occur in a pattern that looks like this (afforementioned excess information removed):

>FRAME 0;  
JOINT 0; 1 2 4 2 5 2 7 2 12 2 14 2  
JOINT 1; 0 4 1 1 2 4 3 4 4 1 5 1 6 4 7 1 8 1 9 4 10 4 11 4 12 1 13 4 14 1 15 1 16 4 17 2 18 2 19 4  
FRAME 10;  
JOINT 0; 5 2 8 1 12 2 13 1 15 2  
JOINT 1; 12 2 16 2  
FRAME 20;  
JOINT 0; 2 1 7 1 12 2 13 2 14 1 16 2 17 2  
JOINT 1; 12 1 14 1  

This tells the game what joints are changing and what they're changing to for each player and on what frame. When grips are used they have their own line too.  
So this lightweight information can be extracted from two different files and merged into a new one.

1. Ask the user for the two files to merge.  
  * Gracefully handle any errors that happen with that.  
2. For each replay file:  
  1. Go through each replay file and remove any lines that aren't crucial for the merged outcome file.
    * The only lines we need are those relating to newgame, bout, frame, joint or grip.
  2. Remove anything referring to Uke.  
  3. Turn one of the replays into Uke's bout (the other stays as the Tori bout).  
  4. Make a dictionary in which each frame line is a key  and the value is anything that happens in the replay before the next frame.  
    * So things like joint movements or grip changes.
3. Merge these two dictionaries together.  
4. Write the contents of the merged dictionary into a file in order of ascending frames.
5. Save the replay and print that the merge finished.
