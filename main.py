#!/usr/bin/python3

# I'ma 'bouta watch all my skill go down the drain for this

import os
import copy
import json
from random import randint
from typing import Any

from drawstring.color import (
	FG_YELLOW,
	FG_GREEN,
	FG_BLUE,
	FG_MAGENTA,
	STYLE_BOLD,
	STYLE_RESET,
	CLEAR_SCREEN,
	CUR_HOME,
	STYLE_ITALIC,
	STYLE_NOITALIC
)

ACTION_QUIT = 0 # You get global variables!

TRIV_CORRECT = 1 # And you get global variables!
TRIV_INCORRECT = 2

ALL_TRIVIA: dict[str, dict[str, Any]] # Everyone gets global variables!
CAN_RANDOM_ENCOUNTER: list[str]
RANDOM_ENCOUNTER: list[str]

class GameExit(Exception):...

def markdownish(string: str):
	"""Etsy markdown parser"""
	i = False

	newstr = ''

	for char in string:
		if char == '*':
			i = not i
			if i:
				newstr += STYLE_ITALIC
			else:
				newstr += STYLE_NOITALIC
		else:
			newstr += char

	return newstr

def fdialogue(dialogue: str):
	"""If there is dialogue, return dialogue. Otherwise, return what you requested."""
	return markdownish(ALL_DIALOGUE[dialogue] if dialogue in ALL_DIALOGUE else dialogue)

class Car:
	def __init__(self):
		self.attrs = {
			"carStranded": False,
			"batteryBad": False,
			"carLocation": "home", # I might not even use these lmao
			"engineSeizeTime": -1
		}
		self.next_event: str|None = None

	def __getattr__(self, attr: str) -> Any:
		if attr in self.attrs:
			return self.attrs[attr]
		raise AttributeError

	def __setattr__(self, attr: str, value: Any):
		if attr in ['attrs', 'next_event']:
			super().__setattr__(attr, value)
			return
		if attr not in self.attrs:
			raise AttributeError(f'Attribute "{attr}" does not exist.')
		if type(value) is not type(self.attrs[attr]):
			raise AttributeError(f'Attribute "{attr}" must be of type {type(value).__name__}.')
		self.attrs[attr] = value
		
car = Car() # good coding practices

def c_input(prompt: str='') -> str:
	"""This just exists so that I can make a better prompt later."""
	return input(prompt)

def usercon():
	input(f'{FG_BLUE+STYLE_BOLD}Press ENTER to continue...{STYLE_RESET}')

def start_day():
	"""Present the player with a problem, and update data accordingly."""
	try:
		if car.next_event is None:
			t_num = randint(0,len(CAN_RANDOM_ENCOUNTER)-1) # Pick a random trivia question.
			triv = copy.deepcopy(TRIVIA[enc_name := CAN_RANDOM_ENCOUNTER[t_num]])
		else:
			triv = copy.deepcopy(enc_name := TRIVIA[car.next_event])
	except KeyError:
		print(f'ERROR: "{enc_name}" is not a valid encounter!')
	car.next_event = None
	nmsg = None
	while True:
		# Print scene
		print(
			STYLE_RESET + \
			CLEAR_SCREEN + \
			CUR_HOME + \
			STYLE_BOLD + \
			triv['scene'] + \
			STYLE_RESET
		)

		# Print options
		for i, option in enumerate(triv['answers']):
			print(f'{i+1}: {option['name']}')

		# Print status message
		if nmsg is not None:
			print(FG_YELLOW+nmsg+STYLE_RESET)
			nmsg = None

		# Take input from the user
		ans = None
		try:
			ans = int(c_input(f'{FG_BLUE+STYLE_BOLD}Choose an option [1-{len(triv['answers'])}]> {STYLE_RESET+FG_MAGENTA}'))-1
			print(end=STYLE_RESET, flush=True)
		except ValueError:
			nmsg = 'Enter a valid number.'
			continue
		except KeyboardInterrupt:
			continue
		except EOFError:
			raise GameExit
		if ans not in list(range(len(triv['answers']))):
			nmsg = 'Enter a number in the given range.'
			continue

		print()

		adata = triv['answers'][ans]

		# Update car attributes (if present)
		if 'setattrs' in adata:
			for k, v in adata['setattrs'].items():
				setattr(car, k, v)

		# Check to see if a next encounter has been provided
		if 'nextEvent' in adata:
			car.next_event = adata['nextEvent']

		# Make this event not encounterable randomly
		if 'removeRandomEncounter' in adata:
			if adata['removeRandomEncounter'] is True:
				CAN_RANDOM_ENCOUNTER.remove(enc_name)

		match adata['type']:
			case 'one_time_dialogue':
				# Show dialogue and remove option
				print(fdialogue(adata['dialogue']))
				usercon()
				del triv['answers'][ans]

			# Yes, I know these do the same thing.

			case 'triv_success':
				# No immediate repercusions
				print(fdialogue(adata['dialogue']))
				usercon()
				return

			case 'triv_failure':
				# Whatever the user did, it's bad.
				print(fdialogue(adata['dialogue']))
				usercon()
				return

		# Show a hint
		if 'hint' in adata:
			print(f'{FG_GREEN}HINT{STYLE_RESET}: ' + fdialogue(adata['hint']))

		# Add an option to the list
		if 'addOptions' in adata:
			for opt in adata['addOptions']:
				newopt = copy.deepcopy(opt)
				newopt['name'] = FG_GREEN+'[NEW] '+STYLE_RESET+opt['name']
				triv['answers'].insert(0,newopt)

		if 'changeScene' in adata:
			triv['scene'] = fdialogue(adata['changeScene'])

def start_game():
	"""Start the game."""
	global CAN_RANDOM_ENCOUNTER
	CAN_RANDOM_ENCOUNTER = copy.copy(RANDOM_ENCOUNTER)
	print(STYLE_BOLD+'PRELOGUE'+STYLE_RESET)
	print(fdialogue('gamePrelogue'))
	print()
	usercon()

	for i in range(10):
		start_day()
	print(CLEAR_SCREEN + CUR_HOME + 'gameEnding')
	usercon()

def start_menu() -> int:
	"""It's the start menu."""
	print(
		CLEAR_SCREEN + \
		CUR_HOME + \
		STYLE_BOLD + \
		'Uncar (The Game)' + \
		STYLE_RESET + \
		'\nType "start" or "help" and press ENTER.'
	)
	while True:
		try:
			ans = c_input('[main menu] > ')
		except KeyboardInterrupt:
			return ACTION_QUIT
		except EOFError:
			return ACTION_QUIT
		cmd, *args = ans.split(' ')
		if cmd == '':
			pass
		elif cmd in ['exit', 'quit']:
			return ACTION_QUIT
		elif cmd == 'start':
			try:
				start_game()
			except GameExit:
				return ACTION_QUIT
			return
		elif cmd == 'help':
			print('TODO: help function') # TODO: help function
			usercon()
			return
		else:
			print(f'{cmd} is not recognized as a valid command.')
			print('Maybe try "help"?')

def main():
	"""Main entry point."""
	global TRIVIA, ALL_DIALOGUE, RANDOM_ENCOUNTER

	# Load various things
	fpath = os.path.dirname(__file__)
	with open(f'{fpath}/trivia.json') as f:
		TRIVIA = json.load(f)
	with open(f'{fpath}/dialogue.json') as f:
		ALL_DIALOGUE = json.load(f)
	with open(f'{fpath}/random_encounter.json') as f:
		RANDOM_ENCOUNTER = json.load(f)
	
	while True: # Loop until the user chooses to quit the game.
		menu_result = start_menu()
		if menu_result is ACTION_QUIT:
			print() # Put a newline so the user prompt doesn't go over the game crap
			break

# yada yada python stuff
if __name__ == '__main__':
	main()
