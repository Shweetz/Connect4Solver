#include <iostream>
#include <vector>
#include <string>

using namespace std;

int nbLig = 4;
int nbCol = 5;

int tab[4][5] = 
  {{ 0, 0, 0, 0, 0},
   { 0, 0, 1, 0, 0},
   { 0,-1,-1, 0, 0},
   { 0, 1, 1,-1, 0}};
  
// player 1 start: playerStarting = 1
// player 2 start: playerStarting = -1
int playerStarting = 1;
     
int max_depth = 25;
long n = 0;

// Checks if one player won, if there are empty cells or if it's a draw 
int gameState(int cellx, int celly) {
	int player = tab[cellx][celly];
	if (player == 0)
		return -2;
		
	// vertical win
	int x = cellx;
	int y = celly;
	while (x > 0 and tab[x-1][y] == player)
	{
		x -= 1;
	}
	int ver = 0;
	while (x < nbLig and tab[x][y] == player)
	{
		ver += 1;
		x += 1;
	}
	if (ver >= 4)
	{
	  //cout << "ver win" << endl;
		return player;
	}
	
	// horizontal win
	x = cellx;
	y = celly;
	while (y > 0 and tab[x][y-1] == player)
	{
		y -= 1;
	}
	int hor = 0;
	while (y < 5 and tab[x][y] == player)
	{
		hor += 1;
		y += 1;
	}
	if (hor >= 4)
	{
	  //cout << "hor win" << endl;
		return player;
	}
		
	// diagonal 1 win
	x = cellx;
	y = celly;
	while (x < nbLig - 1 and y > 0 and tab[x+1][y-1] == player)
	{
		x += 1;
		y -= 1;
	}
	int dia1 = 0;
	while (x >= 0 and y < nbCol and tab[x][y] == player)
	{
		dia1 += 1;
		x -= 1;
		y += 1;
	}
	if (dia1 >= 4)
	{
	  //cout << "dia1 win" << endl;
		return player;
	}
		
	// diagonal 2 win
	x = cellx;
	y = celly;
	while (x > 0 and y > 0 and tab[x-1][y-1] == player)
	{
		x -= 1;
		y -= 1;
	}
	int dia2 = 0;
	while (x < nbLig and y < nbCol and tab[x][y] == player)
	{
		dia2 += 1;
		x += 1;
		y += 1;
	}
	if (dia2 >= 4)
	{
	  //cout << "dia2 win" << endl;
		return player;
	}
    		
  // no one won, but if board isn't full then we can still play
	// so check if there's still room on the board
	for (int j = nbCol-1; j >= 0; j--)
	{
		if (tab[0][j] == 0)
			return -2;
	}
	
	// no one won and board is full, it's a draw
	return 0;
}

// recursive method to check possibility branches
vector<int> search(int cellx, int celly, int t, int a, int b, bool playerMaxes)
{
	n += 1;
  vector<int> list_best;
  int max_log = 0;
		
	int state = gameState(cellx, celly);
	if (state != -2)
	{
  	list_best[0] = state;
		return list_best;
	}
	/*if (t > max_depth - 1)
	{
  	list_best.clear();
  	list_best.push_back(0);
		return list_best;
	}*/
	
  int cellValue = playerMaxes ? 1 : -1;
  
  // list_best[0] contains best result and list_best[1:] moves to get this result
	if (playerMaxes)
	{
	  //int v = -2;	
	  list_best.clear();
	  list_best[0] = -2;
	  
	  for (int celly = 0; celly < nbCol; celly++)
  	{
  	  // find cell to fill
  		if (tab[0][celly] != 0)
  			continue;
  		cellx = nbLig - 1;
  		while (tab[cellx][celly] != 0)
  			cellx -= 1;
  			
  		// fill cell
  		tab[cellx][celly] = cellValue;
  
  		//cout << "av search, n=" << n << endl;
  		vector<int> list_child = search(cellx, celly, t + 1, a, b, false);
  		//cout << "ap search, n=" << n << endl;
  		
  		// reset cell
  		tab[cellx][celly] = 0;
  
      // v = max(v, alphabeta)
  		if (list_child[0] > list_best[0])
  		{
  	    list_best.clear();
  	    list_best[0] = list_child[0];
  	    list_best[1] = celly;
  		}
  		else if (list_child[0] == list_best[0])
  		{
  	    list_best.push_back(celly);
      }
      
      // alpha = max(v, alpha)
      a = max(a, list_best[0]);
      
      // break condition
      if (b <= a)
      {
        break;
      }
  	}
  	return list_best;
	}
	else
	{
	  //int v = 2;	
	  list_best.clear();
	  list_best[0] = 2;
	  
	  for (int celly = 0; celly < nbCol; celly++)
  	{
  	  // find cell to fill
  		if (tab[0][celly] != 0)
  			continue;
  		cellx = nbLig - 1;
  		while (tab[cellx][celly] != 0)
  			cellx -= 1;
  			
  		// fill cell
  		tab[cellx][celly] = cellValue;
  
  		//cout << "av search, n=" << n << endl;
  		vector<int> list_child = search(cellx, celly, t + 1, a, b, true);
  		//cout << "ap search, n=" << n << endl;
  		
  		// reset cell
  		tab[cellx][celly] = 0;
  
      // v = min(v, alphabeta)
  		if (list_child[0] < list_best[0])
  		{
  	    list_best.clear();
  	    list_best[0] = list_child[0];
  	    list_best[1] = celly;
  		}
  		else if (list_child[0] == list_best[0])
  		{
  	    list_best.push_back(celly);
      }
      
      // beta = min(v, beta)
      b = min(b, list_best[0]);
      
      // break condition
      if (b <= a)
      {
        break;
      }
  	}
  	return list_best;
	}
}

int main() {
  // Start the recursive loop
  vector<int> list_best = search(0, 0, 0, -2, 2, playerStarting);
  
  // See who won: res[0] == -1 means playerStarting lost
  int winner = 10;
  if (list_best.size() > 0)
    winner = list_best.at(0);
  
  cout << "winner: " << winner << endl;
  cout << "Number of branches explored: " << n << endl;
  // Print output
  if (playerStarting == 1)
  	cout << "Player 1 start." << endl;
  else if (playerStarting == -1)
  	cout << "Player 2 start." << endl;
  
  if (winner == 0)
  	cout << "It's a draw !" << endl;
  else
  {
  	// winner_number does 1 -> 1 and -1 -> 2
  	int winner_number = winner*-0.5 + 1.5;
  	cout << "Player " << winner_number << " wins !" << endl;
  }
  
  // Where you can play is displayed as numbers corresponding to this:
  //|1|2|3|4|5|6|7|
  
  if (list_best.size() > 1)
  {
    string str_poss = to_string(list_best.at(1) + 1);
    int i = 2;
    while (i < list_best.size())
    {
        str_poss += ", " + to_string(list_best.at(i) + 1);
        i += 1;
    }
    if (winner != -playerStarting)
        cout << "You can play " << str_poss << endl;
  }
}
