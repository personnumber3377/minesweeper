
import numpy as np
import random
import sys

HIDDEN_SPACE = 100
MARKED_SPACE = 101
EMPTY_SHOWN = 102
MINE_NUMBER = 10

# def update(self, position, move_type):

MARK_MOVE = 0
REVEAL_MOVE = 1

class Minefield:
	def __init__(self, width, height, num_mines):
		assert num_mines <= width * height # the amount of mines must be less than or equal to the amount of spaces in the minefield.

		self.mines = np.zeros((width, height)) # Minefield.
		self.shown = np.ones((width, height)) # What we show to the user.
		self.shown = self.shown * HIDDEN_SPACE # Mark them as hidden.
		self.width = width
		self.height = height
		# Thanks to https://stackoverflow.com/questions/22842289/generate-n-unique-random-numbers-within-a-range

		positions = random.sample(range(0,width*height), num_mines)
		positions = [[pos//height, pos % height] for pos in positions] # Decode the positions, this should make it such that there are no duplicates.

		# Sanity check

		if len(positions) != len(set([str(x) for x in positions])):
			print("Error!")
			exit(1)
		self.mine_positions = positions

		for pos in positions:
			self.mines[pos[0]][pos[1]] = MINE_NUMBER

	def render(self):

		# Show the "shown" matrix
		print("Printing the minefield now:")
		print("-"*(self.width + 2))

		for line in self.shown:
			print("|", end="")
			for elem in line:
				if elem == HIDDEN_SPACE:
					print("#", end="")
				elif elem == MARKED_SPACE:
					print("X", end="")
				elif elem == EMPTY_SHOWN:
					print(" ",end="")
				else:
					#print("Elem == "+str(elem))
					print(str(int(elem)), end="")

			print("|", end="\n")
		print("-"*(self.width + 2))

	def get_neighbours(self,position):
		
		if position in self.mine_positions:
			print("Tried to call get_neighbours with a position which is a mine!")
			exit(1)
		
		if position[0] >= self.width or position[0] < 0 or position[1] >= self.height or position[1] < 0:
			print("Tried to call get_neighbours with an out of bounds position!")
			exit(1)


		x = position[0]
		y = position[1]
		neig_positions = [[x+1,y],[x-1,y],[x,y+1],[x,y-1],[x+1,y+1],[x-1,y-1],[x-1,y+1],[x+1,y-1]]

		for i,pos in enumerate(neig_positions):
			
			if pos[0] >= self.width or pos[0] < 0:
				neig_positions[i] = None
			
			if pos[1] >= self.height or pos[1] < 0:
				neig_positions[i] = None

		neig_positions = [x for x in neig_positions if x != None]
		return neig_positions


	def count_neighbours(self,position) -> int:
		neig_positions = self.get_neighbours(position)
		# Count how many of them are bombs.

		count = 0
		for pos in neig_positions:
			if pos in self.mine_positions:
				count += 1

		return count

	def update(self, position, move_type):
		position = list(position)
		if move_type == REVEAL_MOVE:
			#print("self.mine_positions == "+str(self.mine_positions))
			#print("position == "+str(position))
			if position in self.mine_positions:

				# Lost.

				print("You hit a mine! You lost.")
				self.reveal_mines()
				#exit(0)
				return 1

			# First count the neigbhour bombs.

			neig_count = self.count_neighbours(position)

			if neig_count == 0:
				if self.shown[position[0]][position[1]] != EMPTY_SHOWN:

					self.shown[position[0]][position[1]] = EMPTY_SHOWN # Show as empty
					for pos in self.get_neighbours(position):
						self.update(pos, REVEAL_MOVE) # recursively show the mines.
				return
			self.shown[position[0]][position[1]] = neig_count # Just show the number.
		return 0

	def have_won(self):
		#print("self.shown == "+str(self.shown))
		for i, line in enumerate(self.shown):
			for j, elem in enumerate(line):
				if elem == HIDDEN_SPACE:
					# Check if a bomb spot, if yes, then continue, if not, then there are bombs, which aren't been designated yet.
					#print("[j,i] == "+s)
					if [j,i] not in self.mine_positions:
						return False # We have not won
		return True



	def reveal_mines(self):

		print("Revealing mines: (X means mine)")

		print("-"*(self.width + 2))

		for line in self.mines:
			print("|", end="")
			for elem in line:
				if elem == MINE_NUMBER:
					print("X", end="")
				else:
					print(" ",end="")
				#else:

				#	print(str(elem), end="")

			print("|", end="\n")
		print("-"*(self.width + 2))








def setup_minefield() -> Minefield:
	width = int(input("How wide do you want the minefield to be? : "))
	height = int(input("How long do you want the minefield to be? : "))
	num_mines = int(input("How many mines do you want? : "))

	print("Creating game...")

	field = Minefield(width, height, num_mines)

	return field




def get_move() -> tuple:
	move_input = str(input("Which position would you like to reveal? : "))
	while move_input == "":
		move_input = str(input("Which position would you like to reveal? :" ))
	if move_input == "showmines":
		return move_input

	if ", " not in move_input:
		if "," not in move_input:
			print("Invalid input.")
			exit(0)
		return reversed([int(x) for x in move_input.split(",")])
	return reversed([int(x) for x in move_input.split(", ")])



def main() -> int:
	field = setup_minefield()
	print("Input coordinates are in the format x, y")
	while True:
		field.render()
		
		move = get_move()
		if move == "showmines":
			field.reveal_mines()
			continue
		if(field.update(move, REVEAL_MOVE)):
			break
		field.render()
		if field.have_won():
			print("You have won! Congratulations!")
			return 0
		#field.render()
		#field.reveal_mines()
		print("\n"*100+"\r"*100)
		sys.stdout.flush()

	return 0

if __name__=="__main__":

	exit(main())
