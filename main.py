#!/usr/bin/python3

# I'ma 'bouta watch all my skill go down the drain for this

import os
import json
from random import randint
from copy import deepcopy

from drawstring.color import (
	STYLE_BOLD,
	STYLE_RESET,
	CLEAR_SCREEN,
	CUR_HOME
)

# Constants
ACTION_START = 0
ACTION_QUIT = 1

TRIV_CORRECT = 2
TRIV_INCORRECT = 3

TRIVIA: list
DIALOGUE: dict

class Car:
	def __init__(self):
		self.attrs = {
			"carStranded": False
		}
		self.events = [
			"engineSeize",
			"engineRefill"
		]

	def engineSeize(self):
		...
		
	def engineRefill(self):
		...

car = Car() # good coding practices

def c_input(prompt: str='') -> str:
	"""This just exists so that I can make a better prompt later."""
	return input(prompt)

def usercon():
	input('Press ENTER to continue...')

def start_menu() -> int:
	"""It's the start menu."""
	print(STYLE_BOLD+'Automobile S*** (The Game)'+STYLE_RESET)
	while True:
		try:
			ans = c_input('cars > ')
		except EOFError:
			print() # Put a newline so the user prompt doesn't go over the game crap
			return ACTION_QUIT
		cmd, *args = ans.split(' ')
		if cmd in ['exit', 'quit']:
			return ACTION_QUIT
		elif cmd == 'start':
			return ACTION_START

def start_day():
	"""Present the player with a problem, and update data accordingly."""
	t_num = randint(0,len(TRIVIA)-1) # Pick a random trivia question.
	triv = deepcopy(TRIVIA[t_num])
	nmsg = None
	while True:
		print(CLEAR_SCREEN+CUR_HOME+triv['scene'])
		# Print options
		for i, option in enumerate(triv['answers']):
			print(f'{i+1}: {option['name']}')
		# Print status message
		if nmsg is not None:
			print(nmsg)
			nmsg = None
		# Take input from the user
		ans = None
		try:
			ans = int(c_input(f'Choose an option [1-{len(triv['answers'])}]> '))-1
		except ValueError:
			nmsg = 'Enter a valid number.'
			continue
		if ans not in list(range(len(triv['answers']))):
			nmsg = 'Enter a number in the given range.'
			continue
		match (adata := triv['answers'][ans])['type']:
			case 'one_time_dialogue':
				print(DIALOGUE[adata['dialogue']])
				usercon()
				del triv['answers'][ans]

			case 'triv_success':
				print(adata['correctDialogue'])
				usercon()
				return

			case 'event':
				...

def start_game():
	"""Start the game."""
	for i in range(3): #FCHANGE: number of rounds
		start_day()

def main():
	"""Main entry point."""
	global TRIVIA, DIALOGUE

	# TODO: add some form of competence to this
	with open(f'{os.path.dirname(__file__)}/trivia.json') as f:
		TRIVIA = json.load(f)
	with open(f'{os.path.dirname(__file__)}/dialogue.json') as f:
		DIALOGUE = json.load(f)
	
	while True: # Loop until the user chooses to quit the game.
		menu_result = start_menu()
		if menu_result is ACTION_QUIT:
			break
		elif menu_result is ACTION_START:
			start_game()

if __name__ == '__main__':
	main()
