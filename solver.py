tab = [[ 0, 0, 0, 0, 0, 0, 0],
       [ 0, 0, 0, 0, 0, 0, 0],
       [ 0, 0, 0, 0, 0, 0, 0],
       [ 0, 0, 1, 1, 1, 0, 0],
       [ 0, 0,-1, 1,-1,-1, 0],
       [ 0,-1, 1,-1,-1, 1,-1]]
       
max_depth = 3
max_log = 0
n = 0
    
# player 1 start: player = 1
# player 2 start: player = -1
player = 1

# checks if one player won, if there are empty cells or if it's draw 
def gameState(tab):
    # horizontal win
    for i in range(len(tab)):
        for j in range(len(tab[0])-3):
            if tab[i][j] == 1 and tab[i][j+1] == 1 and tab[i][j+2] == 1 and tab[i][j+3] == 1:
                return 1
            if tab[i][j] == -1 and tab[i][j+1] == -1 and tab[i][j+2] == -1 and tab[i][j+3] == -1:
                return -1
    			
    # vertical win
    for i in range(len(tab)-3):
    	for j in range(len(tab[0])):
    		if tab[i][j] == 1 and tab[i+1][j] == 1 and tab[i+2][j] == 1 and tab[i+3][j] == 1:
        	    return 1
    		if tab[i][j] == -1 and tab[i+1][j] == -1 and tab[i+2][j] == -1 and tab[i+3][j] == -1:
    			return -1
                
    # diagonal 1 win
    for i in range(len(tab)-3):
    	for j in range(len(tab[0])-3):
    		if tab[i][j] == 1 and tab[i+1][j+1] == 1 and tab[i+2][j+2] == 1 and tab[i+3][j+3] == 1:
        	    return 1
    		if tab[i][j] == -1 and tab[i+1][j+1] == -1 and tab[i+2][j+2] == -1 and tab[i+3][j+3] == -1:
    			return -1
                
    # diagonal 2 win
    for i in range(3, len(tab)):
        for j in range(len(tab[0])-3):
    		if tab[i][j] == 1 and tab[i-1][j+1] == 1 and tab[i-2][j+2] == 1 and tab[i-3][j+3] == 1:
        	    return 1
    		if tab[i][j] == -1 and tab[i-1][j+1] == -1 and tab[i-2][j+2] == -1 and tab[i-3][j+3] == -1:
    			return -1
    		
    # optimization for empty cell
    if tab[5][6] == 0:
    	return -2
    # empty cell
    for i in range(len(tab)):
    	for j in range(len(tab[i])):
    		if tab[i][j] == 0:
    			return -2
    # draw
    return 0
	
# recursive method to check possibility branches
def search(tab, player, t):
    if t < max_log:
    	print("\t"*t + "tab: " + str(tab[2]))
    state = gameState(tab)
    if state != -2:
    	if t < max_log:
    		print("\t"*t + "endState: " + str(state))
    	return (state*player, -1, -1)
    if t > max_depth - 1:
        return (0, -1, -1)
    	
    # list_best[0] contains best result and list_best[1:] moves to get this result
    list_best = [-2]
    for celly in range(len(tab[0])):
        cellx = 5
        while tab[cellx][celly] != 0:
            cellx -= 1
            if cellx == 0:
                break
        if tab[cellx][celly] == 0:
            tab[cellx][celly] = player
			
			# val is best value found by one child call
            global n 
            n += 1
            val = -search(tab, - player, t + 1)[0]
			
            if val > list_best[0]:
            	list_best = [val, celly]
            elif val == list_best[0]:
            	list_best.append(celly)
			
			# reset tab
            tab[cellx][celly] = 0
    if t < max_log:
    	print("\t"*t + "list_best: " + str(list_best))
    return list_best
	
# Start the recursive loop
res = search(tab, player, 0)

# See who won: res[0] == -1 means starting player lost, not player 1 lost
winner = res[0]*player

print("n: " + str(n))
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
	
