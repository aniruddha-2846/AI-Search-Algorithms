import sys
from AStar import A_star_Search
from BFS import BreadthFirstSearch
from DFS import DepthFirstSearch
from GBFS import GreedyBestFirstSearch

if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt ")
maze = sys.argv[1]

choice = input("Do you wish to see the explored states in the solution?\nEnter Yes or No:")
print(choice.lower())
while(choice.lower() != "yes" and choice.lower() != "no"):
    print("Invalid Choice. Please re enter your choice: ")
    choice = input()
if choice.lower() == "yes":
    choice = True
else:
    choice = False
#bfs
m1 = BreadthFirstSearch(maze)
print("Maze: ")
m1.print()
m1.output_image(empty=True)
m1.solve()
m1.output_image(show_explored = choice)
if(choice):
    print("States Explored in Breadth First Search: ",m1.num_explored)
print("Length of path found in Breadth First Search: ",m1.path_length)
print("%f" % m1.time_taken)

#dfs
m2 = DepthFirstSearch(maze)
m2.solve()
m2.output_image(show_explored = choice)
if(choice):
    print("States Explored in Depth First Search: ",m2.num_explored)
print("Length of path found in Depth First Search: ",m2.path_length)
print("%f" % m2.time_taken)

#gbfs
m3 = GreedyBestFirstSearch(maze)
m3.solve()
m3.output_image(show_explored = choice)
if(choice):
    print("States Explored in Greedy Best First Search: ",m3.num_explored)
print("Length of path found in Greedy Best First Search: ",m3.path_length)
print("%f" % m3.time_taken)

#a*
m4 = A_star_Search(maze)
m4.solve()
m4.output_image(show_explored = choice)
if(choice):
    print("States Explored in A* Search: ",m4.num_explored)
print("Length of path found in A* search: ",m4.path_length)
print("%f" % m4.time_taken)