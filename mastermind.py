
"""To import random choices/items."""
import random

"""To add new players, find the existing players,validating them and creating scoreboard."""
class Players:
	def __init__(self):
		self.__players__ = [ComputerPlayer("HAL9000"), ComputerPlayer("VIKI")]

	def newPlayer(self, player):
		"""To add new players in the player list."""
		self.__players__.append(player)

	def findPlayer(self, name):
		"""To find players if already exist"""
		for player in self.__players__:
			if player.getName() == name:
				return player

	def validate(self, name):
		"""To validate the player i.e if already exist then they can play otherwise they need to register themselves."""
		for player in self.__players__:
			if name == player.getName():
				return True
		return False

	def createScoreBoard(self):
		"""To create the scoreboard for players that are not computer players."""
		print(37*"=" + "\n" + "Name" + 13*" " + "Score Games Average\n" + 37*"=")
		for player in self.__players__:
			if player.getName() not in ["HAL9000", "VIKI"]:
				if player.getGame() != 0:
					print(player.getName() + (19-len(player.getName()))*" " + str(player.getScore()) + 5*" " + str(player.getGame()) + 5*" " + str(player.getScore()/player.getGame()))
				else:
					print(player.getName() + (19 - len(player.getName())) * " " + "0" + 5 * " " + "0" + 5 * " " + "0")
		print(37*"=")

"""To deal with computer players i.e HAL9000 and VIKI"""
class ComputerPlayer:
	def __init__(self, name):
		self.__pname__ = name
		self.__secret__ = []
		self.__colorSet__ = ["R", "G", "B", "W", "Y", "K"]
		self.feedCode = []
		self.feedBack = []
		self.scorebank = []
		self.__games__ = 0
		self.__score__ = 0
		self.broken = False

	def setSecret(self):
		"""Setting secret code by computer player"""
		self.__secret__ = random.sample(self.__colorSet__, 4)

	def guessCode(self):
		"""Guessing the secret code by computer player"""
		return random.sample(self.__colorSet__, 4)

	def getName(self):
		"""To get the player name"""
		return self.__pname__

	def giveFeedback(self, code):
		"""Giving feedback to the computer player after they have guessed."""
		code = list(code)
		secret = self.__secret__
		w = 0
		k = 0
		i = 0
		feedback = ""
		while i < 4:
			if secret[i] == code[i]:
				k += 1
				secret[i] = ""
				code[i] = ""
			i += 1
		i = 0
		while i < 4:
			if secret[i] != code[i]:
				if code[i] in secret:
					w += 1
			i += 1

		if k != 0 or w != 0:
			feedback = k * "K " + w * "W "

		return feedback

	def feedbackBank(self, code, feedback):
		"""Adding the feedback to the feedback list that will show the player their guessed codes."""
		self.feedCode.append(code)
		self.feedBack.append(feedback)

	def increaseScore(self, score):
		"""To increase the score if the guessed code is correct"""
		self.__score__ += score

	def scoreBank(self, score):
		"""To keep a track of scores"""
		self.scorebank.append(score)

	def increaseGame(self):
		self.__games__ += 1

"""To handle the computer players if user input 'HAL9000' or 'VIKI'"""
class Player(ComputerPlayer):

	def __init__(self, name):
		super().__init__(name)


	def validateSecretCode(self,secret):
		"""To validate the secret code entered by the player"""
		colorSet = ["R", "G", "B", "Y", "W", "K"]
		flag = True
		if len(secret) == 4:
			for letter in secret:
				if letter not in colorSet:
					flag = False
					break
		else:
			flag = False

		return flag


	def setSecret(self):
		"""To ask for user input for secret code"""
		print("Please enter the code")
		secret = input("> ").upper()
		result = self.validateSecretCode(secret)
		if (not result):
			print("Invalid Code.")
			print("It must be exactly four characters, each can be R, G, B, Y, W, or K.")
			self.setSecret()

		self.__secret__ = list(secret)

	def guessCode(self):
		"""To ask for code guesses while the game is on."""
		code = []
		while list(code) not in self.__colorSet__ and len(list(code)) != 4:
			print("Please enter the code")
			code = input(">")
			if list(code) not in self.__colorSet__ and len(list(code)) != 4:
				print("Invalid Code.")
				print("It must be exactly four characters, each can be R, G, B, Y, W, or K.")
		return code


	def getGame(self):
		return self.__games__

	def getScore(self):
		return self.__score__

"""To handle the game methods i.e start,makeCode,breakCode."""
class Game:
	def __init__(self, players, attempts):
		self.__players__ = players
		self.__attempts__ = attempts

	def start(self, players):
		"""Starting the game and then calling other methods."""
		attempts = self.__attempts__
		self.makeCode(players)
		self.breakCode(players, attempts)
		print("\nThe game is finished")

		for player in players:
			self.__players__.findPlayers(player).broken = False

		for player in players:
			scorebank = self.__players__.findPlayer(player).scorebank
			if scorebank != []:
				if len(scorebank) == 2:
					print(player, " receives ", scorebank[0], " + ", scorebank[1], " = ", int(scorebank[0])+int(scorebank[1]))
				elif len(scorebank) == 1:
					print(player, " receives ", scorebank[0], " points.")
				self.__players__.findPlayer(player).scorebank = []
			self.__players__.findPlayer(player).increaseGame()


	def makeCode(self, players):
		"""Showing the user about who's turn is to set the code for."""
		i = 0
		while i < len(players):
			if i < len(players)-1:
				print(players[i], "'s turn to set the code for ", players[i+1])
				self.__players__.findPlayer(players[i]).setSecret()
				print("The code is now set for ", players[i+1], " to break.\n")
			else:
				print(players[-1], "'s turn to set the code for ", players[0])
				self.__players__.findPlayer(players[-1]).setSecret()
				print("The code is now set for ", players[0], " to break.\n")
			i += 1

	def breakCode(self, players, attempts):
		"""To provide feedback when a player breaks the code set by codeMaker."""
		t = 0
		while t < attempts:
			i = 0
			while i < len(players):
				feedCode = self.__players__.findPlayer(players[i]).feedCode
				feedBack = self.__players__.findPlayer(players[i]).feedBack

				if not self.__players__.findPlayer(players[i]).broken:
					print(players[i], "'s turn to guess the code")
					print("Previous attempts: ", t)
					if len(feedCode) != 0:
						print(14 * "=")
						print("Code Feedback")
						j = 0
						while j < len(feedCode):
							print(feedCode[j] + " " + feedBack[j])
							j += 1
						print(14 * "=")

					print("Attempts left: ", attempts - t)
					code = self.__players__.findPlayer(players[i]).guessCode()

					if i < len(players)-1:
						feedback = self.__players__.findPlayer(players[i+1]).giveFeedback(code)

					else:
						feedback = self.__players__.findPlayer(players[0]).giveFeedback(code)

					print("Feedback: ", feedback)
					self.__players__.findPlayer(players[i]).feedbackBank(code, feedback)
					if feedback == 4*"K ":
						print(players[i], "broke the code in ", t+1, " attempts!")
						self.__players__.findPlayer(players[i]).increaseScore(attempts-t-1)
						self.__players__.findPlayer(players[i]).scoreBank(attempts-t-1)
						self.__players__.findPlayer(players[i]).feedCode = []
						self.__players__.findPlayer(players[i]).feedBack = []
						self.__players__.findPlayer(players[i-1]).increaseScore(t+1)
						self.__players__.findPlayer(players[i-1]).scoreBank(t+1)
						self.__players__.findPlayer(players[i]).broken = True

				if t == attempts - 1 and feedBack[-1] != 4*"K ":
					print(players[i], "failed to break the code")
				i += 1
			t += 1

"""WorldOfMastermind main class that will run other classes."""
class WorldOfMastermind:

	def __init__(self):
		self.__players__ = Players()
		self.__colorSet__ = ["R", "G", "B", "W", "Y", "K"]

	def intro(self):
		"""Game Introduction"""
		print("Welcome to World of Mastermind !" +
			  "\nDeveloped by Nicole Ocampo" +
			  "\nCOMP 1046 Object-Oriented Programing\n")

	def menu(self):
		"""To display the menu on the screen"""
		option = ""
		while option != "R" or option != "S" or option != "P" or option != "Q":
			print("What would you like to do?\n"
				  + " (r) register a new user\n"
				  + " (s) show the score board\n"
				  + " (p) play a game\n"
				  + " (q) quit")
			option = input(">").upper()
			self.menuOption(option)

	def menuOption(self, option):
		"""Output based on the selected option from the menu"""
		if option == "R":
			self.register()
		elif option == "S":
			self.scoreboard()
		elif option == "P":
			self.play()
		elif option == "Q":
			self.quit()

	def register(self):
		"""Register a new user"""
		print("What is the name of the new user?")
		name = input('>')
		if self.__players__.validate(name):
			print("Sorry, the name is already taken")
		else:
			player = Player(name)
			self.__players__.newPlayer(player)
			print("Welcome, ", name)
		self.menu()

	def scoreboard(self):
		"""To have scoreboard calculations"""
		self.__players__.createScoreBoard()
		self.menu()

	def getNoOfPlayers(self):
		"""To get number of players"""
		noOfPlayers = 0
		try:
			print("How many players (2-4)?")
			noOfPlayers = int(input(">"))
			if noOfPlayers > 4 or noOfPlayers < 2:
				print("Please enter a valid argument")
				self.getNoOfPlayers()
		except:
			print("Please enter a valid argument")
			self.getNoOfPlayers()
		return noOfPlayers

	def getNoOfAttempts(self):
		"""To get number of attempts"""
		noOfAttempts = 0
		try:
			print("How many attempts will be allowed for each player (5-10)?")
			noOfAttempts = int(input(">"))
			if noOfAttempts > 10 or noOfAttempts < 5:
				print("Please enter a valid argument")
				self.getNoOfAttempts()
		except:
			print("Please enter a valid argument")
			self.getNoOfAttempts()
		return noOfAttempts


	def play(self):
		"""To start the play after getting player names and number of attempts."""
		print("Let's play the game of Mastermind!")
		noOfPlayers = self.getNoOfPlayers()
		players = []
		i = 1
		while i <= noOfPlayers:
			name = ""
			while not self.__players__.validate(name):
				print("What is the name of player #" + str(i) + "?")
				name = input(">")
				if self.__players__.validate(name):
					players.append(name)
				else:
					print("Invalid user name.")
			i += 1
		noOfAttempts = self.getNoOfAttempts()
		g = Game(self.__players__, noOfAttempts)
		g.start(players)
		self.menu()

	def run(self):
		"""Method to run the WorldOfMastermind introduction and menu."""
		self.intro()
		self.menu()

	def quit(self):
		"""To quit the game."""
		print("\nThank you for playing the World of Mastermind!")
		exit()

"""Creating object for WorldOfMastermind class and calling the run() method."""
wom = WorldOfMastermind()
wom.run()
