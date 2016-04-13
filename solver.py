tab = [[ 0, 0, 0, 0, 0],
       [ 0, 0, 1, 0, 0],
       [ 0, 1,-1, 0, 0],
       [ 1,-1, 1,-1, 0]]
       
max_depth = 15
max_log = 0
n = 0
    
# player 1 start: player = 1
# player 2 start: player = -1
player = -1

# checks if one player won, if there are empty cells or if it's a draw 
def gameState(tab, cellx, celly):
	player = tab[cellx][celly]
	if player == 0:
		return -2
		
	# vertical win
	x = cellx
	y = celly
	while x > 0 and tab[x-1][y] == player:
		x -= 1
	ver = 0
	while x < len(tab) and tab[x][y] == player:
		ver += 1
		x += 1
	if ver >= 4:
		return player
	
	# horizontal win
	x = cellx
	y = celly
	while y > 0 and tab[x][y-1] == player:
		y -= 1
	hor = 0
	while y < len(tab[0]) and tab[x][y] == player:
		hor += 1
		y += 1
	if hor >= 4:
		return player
		
	# diagonal 1 win
	x = cellx
	y = celly
	while x < len(tab) - 1 and y > 0 and tab[x+1][y-1] == player:
		x += 1
		y -= 1
	dia1 = 0
	while x >= 0 and y < len(tab[0]) and tab[x][y] == player:
		dia1 += 1
		x -= 1
		y += 1
	if dia1 >= 4:
		return player
		
	# diagonal 2 win
	x = cellx
	y = celly
	while x > 0 and y > 0 and tab[x-1][y-1] == player:
		x -= 1
		y -= 1
	dia2 = 0
	while x < len(tab) and y < len(tab[0]) and tab[x][y] == player:
		dia2 += 1
		x += 1
		y += 1
	if dia2 >= 4:
		return player
    		
    # optimization for empty cell
	if tab[0][len(tab[0])-1] == 0:
		return -2
	# empty cell
	for i in range(len(tab)):
		for j in range(len(tab[i])):
			if tab[i][j] == 0:
				return -2
	# draw
	return 0
	
# recursive method to check possibility branches
def search(tab, player, cellx, celly, t):
	#if t < max_log:
		#print("\t"*t + "tab: " + str(tab[2]))
	state = gameState(tab, cellx, celly)
	if state != -2:
		if t < max_log:
			print("\t"*t + "endState: " + str(state))
		return (state*player, -1, -1)
	if t > max_depth - 1:
		return (0, -1, -1)
		
	# list_best[0] contains best result and list_best[1:] moves to get this result
	list_best = [-2]
	for celly in range(len(tab[0])):
		if tab[0][celly] != 0:
			continue
		cellx = len(tab)-1
		while tab[cellx][celly] != 0:
			cellx -= 1
		tab[cellx][celly] = player

		# val is best value found by one child call
		global n 
		n += 1
		#if n%1000 == 0:
			#print(n)
		val = -search(tab, - player, cellx, celly, t + 1)[0]

		if val > list_best[0]:
			list_best = [val, celly]
		elif val == list_best[0]:
			list_best.append(celly)

		# reset tab
		tab[cellx][celly] = 0
    #if t < max_log:
    	#print("\t"*t + "list_best: " + str(list_best))
	return list_best
	
# Start the recursive loop
res = search(tab, player, 0, 0, 0)

# See who won: res[0] == -1 means starting player lost, not player 1 lost
winner = res[0]*player

print("Number of branches explored: " + str(n))
# Print output
if player == 1:
	print("Player 1 start.")
elif player == -1:
	print("Player 2 start.")

if winner == 0:
	print("It's a draw !")
else:
	# winner_number does 1 -> 1 and -1 -> 2
	winner_number = int(winner*-0.5 + 1.5)
	print("Player " + str(winner_number) + " wins !")

# Where you can play is displayed as numbers corresponding to this:
#|1|2|3|4|5|6|7|

str_poss = str(res[1] + 1)
i = 2
while i < len(res):
    str_poss += ", " + str(res[i] + 1)
    i += 1
if (winner != -player):
    print("You can play " + str_poss)
	
