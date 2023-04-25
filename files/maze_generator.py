import random
import sys

if len(sys.argv) != 3:
    sys.exit("Usage: python filename.py length width")

maze_len = int(sys.argv[1])
maze_width = int(sys.argv[2])

def rand_generator():
    n = random.randint(0,2)
    if(n == 0):
        return True
    else:
        return False

maze = []
temp_row = []
for i in range(0,maze_width):
    temp_row.append("#")
maze.append(temp_row)
for i in range (1,maze_len-1):
    maze_row = []
    maze_row.append("#")
    for j in range (1,maze_width-1):
        if(rand_generator()):
            maze_row.append("#")
        else:


            
            maze_row.append(" ")
    maze_row.append("#")
    maze.append(maze_row)
temp_row = []
for i in range(0,maze_width):
    temp_row.append("#")
    
maze.append(temp_row)

quadrants = []
q1 = [[1,maze_len//2],[1,maze_width//2]]
q2 = [[1,maze_len//2],[maze_width//2+1,maze_width-1]]
q3 = [[maze_len//2+1, maze_len-1],[1,maze_width]]
q4 = [[maze_len//2+1,maze_len-1],[maze_width//2+1,maze_width-1]]

quadrants.append(q1)
quadrants.append(q2)
quadrants.append(q3)
quadrants.append(q4)

rand_st_index = random.randint(0,3)
rand_start = quadrants[rand_st_index]

rand_end_index = random.randint(0,3)
rand_end = quadrants[rand_end_index]


start_x,start_y = random.randint(rand_start[0][0],rand_start[0][1]),random.randint(rand_start[1][0],rand_start[1][1])
goal_x,goal_y = random.randint(rand_end[0][0],rand_end[0][1]),random.randint(rand_end[1][0],rand_end[1][1])

while(goal_x != start_x and goal_y != start_y):
    goal_x,goal_y = random.randint(rand_end[0][0],rand_end[0][1]),random.randint(rand_end[1][0],rand_end[1][1])

maze[start_x][start_y] = "A"
maze[goal_x][goal_y] = "B"

maze_file = open("maze/random_maze.txt","w+")
for i in range(0,maze_len):
    str = ""
    for j in range(0,maze_width):
        str += maze[i][j]
    maze_file.write(str)
    maze_file.write("\n")