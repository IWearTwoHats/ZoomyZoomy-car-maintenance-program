#!/usr/bin/python3

# I'ma 'bouta watch all my skill go down the drain for this

import os
import json
from random import randint

from drawstring.color import (
	STYLE_BOLD,
	STYLE_RESET
)

# Constants
ACTION_START = 0
ACTION_QUIT = 1

TRIV_CORRECT = 2
TRIV_INCORRECT = 3

TRIVIA: list

def c_input(prompt: str='') -> str:
	"""This just exists so that I can make a a better prompt later."""
	return input(prompt)

def start_menu() -> int:
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
	triv = TRIVIA[t_num]
	nmsg = None
	while True:
		print(triv['scene'])
		if nmsg is not None:
			print(nmsg)
			nmsg = None
		for i, option in enumerate(triv['answers']):
			print(f'{i+1}: {option}')
		ans = None
		try:
			ans = int(c_input(f'Choose an option [1-{len(triv['answers'])}]> '))
		except ValueError:
			nmsg = 'Enter a valid number.'
		if ans in list(range(1,len(triv['answers'])+1)):
			if ans == triv['correct']+1:
				return TRIV_CORRECT
			else:
				return TRIV_INCORRECT
		else:
			nmsg = 'Enter a number within the given range.'

def start_game():
	for i in range(3): #FCHANGE: number of rounds
		start_day()

def main():
	global TRIVIA

	with open(f'{os.path.dirname(__file__)}/trivia.json') as f:
		TRIVIA = json.load(f)
	
	while True:
		menu_result = start_menu()
		if menu_result is ACTION_QUIT:
			break
		elif menu_result is ACTION_START:
			start_game()

if __name__ == '__main__':
	main()
