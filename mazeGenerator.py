import random

EMPTY   = ' '
BARRIER = '#'

def adjacent(cell):
	
	i, j = cell
	
	for y,x in ((1, 0) , (0, 1), (-1, 0), (0, -1)):
		yield(i + y, j + x) ,(i + 2 * y, j + 2 * x)

def generate(width: int, height: int, barrierSize: int = 1):
	
	spaceCells = set()
	connected  = set()
	barriers   = set()
	maze       =    {}

	for     i in range(height):
		for j in range(width ):
			if i % 2 and j % 2:
				maze[(i, j)] = EMPTY
			else:
				maze[(i, j)] = BARRIER
		
	for i in range(height):
		maze[(i,       0)] = BARRIER
		maze[(i, width-1)] = BARRIER
		
	for j in range(width):
		maze[(0,        j)] = BARRIER
		maze[(height-1, j)] = BARRIER
		
	for i in range(height):
		for j in range(width):
			if maze[(i,j)] == EMPTY:
				spaceCells.add((i,j))
			elif maze[(i,j)]==BARRIER:
				barriers.add((i,j))

		connected.add((1,1))

	while len(connected) < len(spaceCells):
		statusA, statusB = None, None
		shuffled = list(connected)
		random.shuffle(shuffled)
		for(i, j) in shuffled:
			if statusA is not None: break
			for A, B in adjacent((i,j)):
				if A not in barriers:
					continue
				if B not in spaceCells or B in connected:
					continue
				statusA, statusB=A,B
				break

		A,B = statusA, statusB
		maze[A] = EMPTY
		
		barriers    .remove(A)
		spaceCells  .add(A)
		
		connected   .add(A)
		connected   .add(B)

		strings = []

	for i in range(height):
		strings.append(''.join(maze[(i, j)]for j in range(width)))

	return strings