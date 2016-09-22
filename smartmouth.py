from msvcrt import getch,kbhit
from time import time,sleep
from random import randint
from os import system
level=0 #difficulty that the player choses
players_name=""
minimum_word_length=0
number_of_rounds=0
players_points=0 #how many times the player correctly guesses the word
computers_points=0 #how many times the computer guesses the word
smart_mode=False #the mode in which the level depends on the players skill level.
level_reccomendation="(If this is your first time, you should choose an easy level)" #default reccomendation

"""this function takes in the first and last letter, and an amount of time(timeout) and lets the player input anything, but cuts them off at the time limit, and returns what they wrote, along with whether or not they had pressed enter (finishing their word). It also calls the printing_board function to print the board"""
def input_and_time(timeout,first_letter,last_letter): #partially from stack overflow: http://stackoverflow.com/questions/2933399/how-to-set-time-limit-on-input
	finish_time=time()+timeout #this determines when the player runs out of time
	input_word=""
	printing_board(first_letter,last_letter,input_word)
	while True:
		if kbhit():
			key_pressed=str(getch()) #if they're pressing a letter, then it gets that letter
			if key_pressed[3]=="r": #pressing enter
				return [input_word,True]
			elif key_pressed[3]=="x": #pressing backspace
				input_word=input_word[:-1]
			elif key_pressed[3]!="t": #makes sure that nothing is added if they press tab
				input_word+=key_pressed[2] #adds the letter to the word
			printing_board(first_letter,last_letter,input_word)
		if time() > finish_time:
			return [input_word,False] #False means that they did not hit enter, and assumedly did not complete the word. this affects how the computer phrases it when it says its word.

"""This takes in the first and last letters, and returns a list of words that fill the requirements."""
def check_word_matches(first,last):
	words=[]
	for line in open("words.txt"):
		word=line.strip()
		if len(word)>=minimum_word_length and word[0]==first and word[-1]==last: #checking if the word fits the requirements
			words.append(word)
	return words

"""Introduces the game, then gets the players name, saves it as a global variable"""
def get_name(): #this function neccesary so that when a player plays again, they do not need to reenter their name
	global players_name
	system('cls')
	input("\nHi there, welcome to SmartMouth!\n\nIn this game, you will be presented with two letters, and will have to think of a word of at least a certain length that starts with the first letter and ends  with the other letter! \n\nPress enter to continue.")
	system('cls')
	while True: #validates the input
		players_name=input("\nwhat is your name (maximum 16 letters)?\n")
		if len(players_name)<=16:
			break
		print("That's too long.\n")
	start_game()

"""gets the rest of the players information, and their preferences, and then facilitates the rounds, using random letters, and keeps track of the score. It also deals with what happens at the end of the game, and lets the player start over."""
def start_game():
	global level,minimum_word_length,number_of_rounds,players_points,computers_points,level_reccomendation
	matches=["No Matches Yet"] #has to be defined because it later sets old matches to matches
	players_points=0 #resetting things if they want to play again
	computers_points=0
	smart_mode=False
	system('cls')
	while True: #Validating the level they enter
		level=input("\nHi "+players_name+". there are 12 levels in this game, level 12 is the hardest.\nWhich level would you like to play?\n\n"+level_reccomendation+"\n\n\nYou can also write 's' for smart-mode, where the difficulty depends upon your   skill level.\n")
		if level=="s":
			level=4.5 #arbitrarily chosen as a moderate level
			smart_mode=True
			break
		elif level.isdigit():
			if 0<int(level)<13:
				level=int(level)
				break
		print("Please enter a valid level number, or write 's'.")
		sleep(3)
		system('cls')
	system('cls')
	while True: #validating their minnimum word length
		minimum_word_length=input("\nWhat is the minimum word length (a number from 3-10)?\n")
		if minimum_word_length.isdigit():
			if 2<int(minimum_word_length)<11:
				minimum_word_length=int(minimum_word_length)
				break
		print("Please enter a valid number from 3 to 10.")
		sleep(3)
		system('cls')
	system('cls')
	while True: #Validating how many rounds they want to play
		number_of_rounds=input("\nHow many rounds do you want to play (ten to forty recommended)?\n")
		if number_of_rounds.isdigit():
			number_of_rounds=int(number_of_rounds)
			break
		print("Please enter a number.")
		sleep(3)
		system('cls')
	for i in range(number_of_rounds):
		old_matches=matches #so that you can look at the matches from last round when you are playing
		while True: #makes sure there are enough combinations
			rand1=chr(randint(0,25)+97)
			rand2=chr(randint(0,25)+97)
			matches=check_word_matches(rand1,rand2)
			if len(matches)>20-(level*2) and len(matches)>0: #depending on their level, they car get harder combinations.
				break
		if i==0: #they have no matches to see the first time around
			can_show_matches=False
		else:
			can_show_matches=True
		if players_turn(rand1,rand2,matches,old_matches,can_show_matches): #checks to see if they won the round.
			players_points+=1
			if smart_mode and level<12: #to make sure it doesn't go over 12
				level+=.45 #slightly less than the amount the level goes down when you lose (.5). this ensures that whoever is playing will eventually score more than the computer. this makes people feel good about themselves.
		else:
			computers_points+=1
			if smart_mode and level>1: #so that they don't go below 1.
				level-=.5
	while True:
		print("\nPress tab to continue, or a number to view matches.") #this lets them view the matches after the last round of the game.
		their_input=str(getch())
		if their_input[3]=="t": #validation
			break
		elif their_input[2].isdigit(): #validation
			print_matches(matches)
			while True:
				print("press tab to continue.")
				if str(getch())[3]=="t":
					break
			break
	system('cls')
	if players_points>computers_points:
		print("You win!\n")
	elif players_points<computers_points:
		print("Sorry, you lose.\n")
	else:
		print("Tie\n")
	print(players_name+"'s points: "+str(players_points)+"   my points (level "+str(int(level))+"): "+str(computers_points))
	sleep(2)
	while True: #validates input
		quitting=input("Press enter to play again, or write 'quit' to stop.\n")
		if quitting=="quit":
			return #leaves the function to quit the program
		elif quitting=="":
			break
		print("Invalid input...")
	if smart_mode:
		level_reccomendation=level #usually in smartmode the player ends up with a level that suits them.
	else:
		level_reccomendation=level+((players_points-computers_points)*7/(players_points+computers_points)) #this makes it so that the recommendation is more/less extreme depending on the difference of points.
	if level_reccomendation>12:
		level_reccomendation==12 #don't want to reccomend a level that does not exist
	elif level_reccomendation<1:
		level_reccomendation=1
	level_reccomendation=int(round(level_reccomendation))
	level_reccomendation="(You were just on level "+str(int(level))+". I think that you should try level "+str(level_reccomendation)+")"
	start_game()

"""takes in the first and last letters, and their guess. prints the letters, their guess, and the current scores."""
def printing_board(first_letter,last_letter,current_guess):
	system('cls')
	print("\n["+first_letter+"]   ["+last_letter+"]\n\n\n"+current_guess+"\n\n"+players_name+"'s points: "+str(players_points)+"   my points (level "+str(int(level))+"): "+str(computers_points))

"""Takes in first and last letters, the list of matches, the matches from last round, and whether the player has an option to show the matches. It waits for them to press tab, or a number to show matches depending on whether there are matches to show. It then sets the correct time for the computer to wait before guessing, and calls input_and_time with that time. It gets the players answer, and print whether they were right or not. returns whether they won or not."""
def players_turn(first_letter,last_letter,matches,old_matches,can_show_matches):
	if can_show_matches: # I used tab and number keys, because the player would not otherwise use them. I do not want them to axidentally write something after the computer cut them off, and have it in the input buffer, and make the next round start imeadiately.
		print("\nPress tab to play, or a number to view matches!")
	else:
		print("Press tab to play!")
	while True:
		inputted_value=str(getch())
		if inputted_value[3]=="t": # if they press tab, it goes on to the next round
			system('cls')
			break
		elif inputted_value[2].isdigit(): #if they wrote a number
			print_matches(old_matches)
			print("press tab to play!") #after that, they can only press tab to play
			while True:
				if str(getch())[3]=="t": #if they press tab
					break
			break
	sleep(.05)
	time_to_input=(80/len(matches)+5)*(((10-level)/8)+.6)*(minimum_word_length/20+.75) #this is how long they have to input. the more matches there are, the less time you get. the higher your level, the less time you get. the shorter the minnimum word length you chose, the less time you get. 
	results_of_input=input_and_time(time_to_input,first_letter,last_letter) #first index is their word, second index is  whether they pressed enter after they typed their word
	computers_word=matches[randint(0,len(matches)-1)] #a random word that meets the requirements
	if results_of_input[0] in matches:
		print("Nice Job!") #if they got a valid word
		return True
	elif results_of_input[1]:
		print("Sorry, that word was invalid. how about "+computers_word+"?") #this assumes that they thought what they inputted was a word
	else:
		print("Too late! I guess "+computers_word+"!") #this assumes that they ran out of time, because they did not press enter
	sleep(.5)
	return False

"""this takes in a list of all of the matches and prints them up to the 28th word."""
def print_matches(matches):
	matches_to_print=""
	print("\nMatches: "+str(len(matches))+"  Showing: ",end="")
	for i in range(28):
		if i==len(matches): #it stops when all of the matches have been printed, if that happens.
			i-=1 #subtracted because 1 is added at the bottom
			break
		elif len(matches[i])<21: #checks that its not too long
			matches_to_print+=(matches[i]+" "*(20-len(matches[i]))) #adds it to matches to print
	print(str(i+1)+"\n") #how many matches are showing. 1 is added because i starts at 0
	print(matches_to_print+"\n\n") #prints all at once, more efficient
while True:
	if input("\nWelcome. Hit enter to play, or write 'check' to check the matches for a specific letter pair.\n\n")=="check":
		system('cls')
		print(check_word_matches(input("first: "),input("last: ")))
	else:
		get_name()
		break