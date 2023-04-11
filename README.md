# AI-Search-Algorithms
This program deals with the comparison of four search algorithms in Artificial Intelligence
  *	Breadth First Search
  *	Depth First Search
  *	Greedy Best First Search 
  *	A* Search.
  
To run these files, make sure that python is installed on your system, along with NumPy and Pillow libraries installed.
Install the folder as a zip, unzip the files and then follow these steps:
To run the program, follow these steps (for Windows):
1.	To run the random maze generator file, open the command prompt from the folder and type:

          py files/mazegenerator.py <rowlen> <collen>

	where ***rowlen*** is the no. of rows of the maze, and ***collen*** is the no. of columns of the maze.
	For example
	
		py mazegenerator.py 50 50
		
	generates a random maze of size 50x50.
	Alternatively, you could skip using the maze generator file and simply use one of the 10 different mazes provided in the maze folder.

2.	To run the program, open the command prompt from the folder and type:

          py files/project.py <filename.txt>
	where filename.txt is the name of the file which contains the maze. On running the command, you will be asked whether or not you wish to see the states explored by the algorithm while searching for the path. Enter “Yes” if you wish to see the explored states, or type in “No” if you do not wish to do so.
The maze will pe stored into the maze.png file, whereas the paths found by each of the algorithms will be converted into .png files as well. 
