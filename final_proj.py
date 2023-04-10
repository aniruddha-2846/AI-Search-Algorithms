import sys
from PIL import ImageFont
import numpy as np
import datetime as dt 
import math

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
        
class DepthFirstSearch():
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        # print(contents)
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result


    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0
        self.path_length = 0
        self.time_taken = 0
        startTime = dt.datetime.now()

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:
            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                endTime = dt.datetime.now()
                self.time_taken = endTime - startTime
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
            
    
    def output_image(self, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)
                    self.num_explored += 1

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)
                    self.num_explored += 1

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (249, 97, 103)
                    self.num_explored += 1
                    self.path_length += 1

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (252,252,125)
                    self.num_explored += 1

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        if(show_explored):
            img.save("DFS.png")
        else:
            img.save("DFS-noexplored.png")

class BreadthFirstSearch():
    def __init__(self, filename):

        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        # print(contents)
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result


    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0
        self.time_taken = 0
        startTime = dt.datetime.now()

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = QueueFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:
            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                endTime = dt.datetime.now()
                self.time_taken = endTime - startTime
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def output_image(self, show_solution=True, show_explored=False, empty=False):
        self.num_explored = 0
        self.path_length = 0
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)
                    self.num_explored += 1

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)
                    self.num_explored += 1

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (249, 97, 103)
                    self.num_explored += 1
                    self.path_length += 1

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (252,252,125)
                    self.num_explored += 1

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )
        if(empty):
            img.save("maze.png")
        if(show_explored):
            img.save("BFS.png")
        else:
            img.save("BFS-noexplored.png")

class GreedyBestFirstSearch():
    def __init__(self, filename):

        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        # for line in contents:
            # print(line)
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
        # print(self.height," ",self.width)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None
        x_g,y_g = self.goal
        # print(x_g,y_g)
        self.heuristic = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if not self.walls[i][j]:
                    if self.walls[i][j] == 'B':
                        row.append(0)
                    else:
                        row.append(abs(x_g-i) + abs(y_g-j))
                else:
                    row.append('X')
            self.heuristic.append(row)
                        


    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def print_heuristics(self):
        solution = self.solution[1] if self.solution is not None else None
        # print(self.heuristic)


    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def solve(self):
        # Initialize self.frontier priority queue and explored set
        self.num_explored = 0
        self.time_taken = 0
        self.path_length = 0

        startTime = dt.datetime.now()
        #Initialise the start node
        start_node = Node(state=self.start, parent=None, action=None)
        x_c,y_c = self.start

        
        #initialise the self.frontier dict, keys are nodes, and values are the heuristic at that node
        self.frontier = {}
        self.frontier[start_node] = self.heuristic[x_c][y_c]

        #maintain a track of states and nodes in the maze
        self.nodelist = {}
        self.nodelist[start_node.state] = start_node

        #initialise explored set
        self.explored = set()

        #search till solution found or no more states left to explore
        while True:
            if(len(self.frontier) == 0):
                raise Exception("no solution")
            self.frontier_keys = list(self.frontier.keys())
            self.frontier_vals = list(self.frontier.values())
            sorted_value_index = np.argsort(self.frontier_vals)[::-1]
            # sorted_value_index.reverse()
            self.frontier = {self.frontier_keys[i] : self.frontier_vals[i] for i in sorted_value_index}
            node,node_heuristic = self.frontier.popitem()

            if(node.state == self.goal):
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                endTime = dt.datetime.now()
                self.time_taken = endTime - startTime
                return
            
            self.explored.add(node.state)
            for action,state in self.neighbors(node.state):
                if not self.contains_state(state) and state not in self.explored:
                    child = Node(state = state, parent = node, action = action)
                    x_t,y_t = child.state
                    self.frontier[child] = self.heuristic[x_t][y_t]
    
    def contains_state(self, state):
        try:
            if(self.frontier[self.nodelist[state]] in self.frontier.keys):
                return True
        except KeyError:
            return False

    def output_image(self, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)
                    self.num_explored += 1

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)
                    self.num_explored += 1

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (249, 97, 103)
                    self.num_explored += 1
                    self.path_length += 1

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (252,252,125)
                    self.num_explored += 1

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )
                draw.text((((j * cell_size + cell_border + (j + 1) * cell_size - cell_border)/2,(i * cell_size + cell_border + (i + 1) * cell_size - cell_border)/2)),str(self.heuristic[i][j]),fill = "black")

        if(show_explored):
            img.save("GBFS.png")
        else:
            img.save("GBFS-noexplored.png")


class A_star_Search():
    def __init__(self, filename):

        # Read file and set height and width of maze
        with open(filename) as f:
            contents = f.read()

        # Validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        # Determine height and width of maze
        contents = contents.splitlines()
        # for line in contents:
            # print(line)
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
        # print(self.height," ",self.width)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None
        x_g,y_g = self.goal
        x_s,y_s = self.start
        # print(x_g,y_g)
        self.heuristic = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if not self.walls[i][j]:
                    if self.walls[i][j] == 'B':
                        row.append(0)
                    else:
                        row.append(abs(x_g-i) + abs(y_g-j) + math.sqrt(abs(x_s-i)**2 + abs(y_s-j)**2))
                else:
                    row.append('X')
            self.heuristic.append(row)
                        


    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def print_heuristics(self):
        solution = self.solution[1] if self.solution is not None else None
        # print(self.heuristic)


    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def solve(self):
        # Initialize self.frontier priority queue and explored set
        self.num_explored = 0
        self.time_taken = 0
        self.path_length = 0
        startTime = dt.datetime.now()

        #Initialise the start node
        start_node = Node(state=self.start, parent=None, action=None)
        x_c,y_c = self.start

        
        #initialise the self.frontier dict, keys are nodes, and values are the heuristic at that node
        self.frontier = {}
        self.frontier[start_node] = self.heuristic[x_c][y_c]

        #maintain a track of states and nodes in the maze
        self.nodelist = {}
        self.nodelist[start_node.state] = start_node

        #initialise explored set
        self.explored = set()

        #search till solution found or no more states left to explore
        while True:
            if(len(self.frontier) == 0):
                raise Exception("no solution")
            self.frontier_keys = list(self.frontier.keys())
            self.frontier_vals = list(self.frontier.values())
            sorted_value_index = np.argsort(self.frontier_vals)[::-1]
            # sorted_value_index.reverse()
            self.frontier = {self.frontier_keys[i] : self.frontier_vals[i] for i in sorted_value_index}
            node,node_heuristic = self.frontier.popitem()

            if(node.state == self.goal):
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                endTime = dt.datetime.now()
                self.time_taken = endTime - startTime
                return
            
            self.explored.add(node.state)
            for action,state in self.neighbors(node.state):
                if not self.contains_state(state) and state not in self.explored:
                    child = Node(state = state, parent = node, action = action)
                    x_t,y_t = child.state
                    self.frontier[child] = self.heuristic[x_t][y_t]
    
    def contains_state(self, state):
        try:
            if(self.frontier[self.nodelist[state]] in self.frontier.keys):
                return True
        except KeyError:
            return False

    def output_image(self, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.goal:
                    fill = (255, 0, 0)
                    self.num_explored += 1

                # Goal
                elif (i, j) == self.start:
                    fill = (0, 171, 28)
                    self.num_explored += 1

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (249, 97, 103)
                    self.num_explored += 1
                    self.path_length += 1

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (252,252,125)
                    self.num_explored += 1

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )
                draw.text((((j * cell_size + cell_border + (j + 1) * cell_size - cell_border)/2,(i * cell_size + cell_border + (i + 1) * cell_size - cell_border)/2)),str(self.heuristic[i][j]),fill = "black")
        if(show_explored):
            img.save("A-star.png")
        else:
            img.save("A-star-noexplored.png")

#driver code

if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

maze = sys.argv[1]

#bfs
m1 = BreadthFirstSearch(maze)
print("Maze: ")
m1.print()
m1.output_image(empty=True)
m1.solve()
m1.output_image(show_explored = True)
print("States Explored in Breadth First Search: ",m1.num_explored)
print("Length of path found: ",m1.path_length)
print(m1.time_taken)

#dfs
m2 = DepthFirstSearch(maze)
m2.solve()
m2.output_image(show_explored = True)
print("States Explored in Depth First Search: ",m2.num_explored)
print("Length of path found: ",m2.path_length)
print(m2.time_taken)

#gbfs
m3 = GreedyBestFirstSearch(maze)
m3.solve()
m3.output_image(show_explored = True)
print("States Explored in Greedy Best First Search: ",m3.num_explored)
print("Length of path found: ",m3.path_length)
print(m3.time_taken)

m4 = A_star_Search(maze)
m4.solve()
m4.output_image(show_explored = True)
print("States Explored in A* Search: ",m4.num_explored)
print("Length of path found: ",m4.path_length)
print(m4.time_taken)