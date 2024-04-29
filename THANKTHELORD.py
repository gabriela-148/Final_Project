from queue import PriorityQueue
import tkinter as tk
import time
import sys

class Cell:
    def __init__(self, x, y, is_wall=False):
        self.x = x
        self.y = y
        self.is_wall = is_wall
        self.g = float("inf")
        self.h = 0
        self.f = float("inf")
        self.parent = None
        self.visited = False
        self.ward = ""

    def __lt__(self, other):
        return self.f < other.f

class MazeGame:
    def __init__(self, root, maze, algorithms, start_locations, delivery_locations):
        self.root = root
        self.maze = maze

        self.rows = len(maze)
        self.cols = len(maze[0])

        # Store start locations and delivery locations
        self.start_locations = start_locations
        self.delivery_locations = delivery_locations

        self.algorithms = algorithms
        print(self.algorithms)

        self.color_map = {
            0: 'white',
            1: 'grey',
            2: 'red',
            3: 'yellow',
            4: 'lightskyblue',
            5: 'pink',
            6: 'darkgreen',
            7: 'orange',
            8: 'powderblue',
            9: 'darkseagreen',
            10: 'purple',
            11: 'coral',
            12: 'olive',
            14: 'black',
            15: 'green2'
        }

        priorities = {
            (17, 31): 5, (11, 31): 5, (24, 30): 5, (22, 11): 5,
            (24, 25): 4, (8, 5): 4,
            (24, 15): 3, (33, 11): 3,
            (34, 30): 2, (21, 23): 2,
            (17, 34): 1, (10, 27): 1
        }

        # Organize delivery locations by priority
        self.goal_pos = self.delivery_locations[0]
        self.agent_pos = (self.start_locations)

        self.cells = [[Cell(x, y, maze[x][y] == 14) for y in range(self.cols)] for x in range(self.rows)]

        # Initialize the agent position

        #### Start state's initial values for f(n) = g(n) + h(n)
        self.cells[self.agent_pos[0]][self.agent_pos[1]].g = 0
        self.cells[self.agent_pos[0]][self.agent_pos[1]].h = self.heuristic(self.agent_pos)
        self.cells[self.agent_pos[0]][self.agent_pos[1]].f = self.heuristic(self.agent_pos)

        self.cell_size = 20
        self.canvas = tk.Canvas(root, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg='white')
        self.canvas.pack()

        self.draw_maze()

        if self.algorithms[0] == "A*":
            print("Running A Star")
            starting = self.agent_pos
            for pos in self.delivery_locations:
                self.run_astar(starting, pos)
                starting = pos
                print("End pos:", pos)
        elif self.algorithms[0] == "Dijsktras":
            print("Running Dijkstras")
            starting = self.agent_pos
            for pos in self.delivery_locations:
                self.run_dij(starting, pos)
                starting = pos
                print("End pos: ", pos)
        else:
            print("Ineligible algorithm type. Please specify whether to use A* or Dijsktra's search algorithm.")
            


    def build_queue(self, sorted_ward_list):
        priority_queue = PriorityQueue()
        for priority, ward_name, location in sorted_ward_list:
            priority_queue.put((priority, location))  # Include priority along with location
        locations_list = [item[2] for item in sorted_ward_list]
        print(locations_list)
        return locations_list

    def draw_maze(self):
        color_map = {
            0: 'white',
            1: 'grey',
            2: 'red',
            3: 'yellow',
            4: 'lightskyblue',
            5: 'pink',
            6: 'darkgreen',
            7: 'orange',
            8: 'powderblue',
            9: 'darkseagreen',
            10: 'purple',
            11: 'coral',
            12: 'olive',
            14: 'black',
            15: 'green2'
        }

        for x in range(self.rows):
            for y in range(self.cols):
                color = color_map[self.maze[x][y]]
                if self.maze[x][y] == 1:
                    self.cells[x][y].ward = "Admissions"
                    #print(self.cells[x][y].ward)
                elif self.maze[x][y] == 2:
                    self.cells[x][y].ward = "General Ward"
                    #print(self.cells[x][y].ward)
                elif self.maze[x][y] == 3:
                    self.cells[x][y].ward = "Emergency"
                    #print(self.cells[x][y].ward)
                elif self.maze[x][y] == 4:
                    self.cells[x][y].ward = "Maternity"
                    #print(self.cells[x][y].ward)
                elif self.maze[x][y] == 5:
                    self.cells[x][y].ward = "Surgical Ward"
                    #print(self.cells[x][y].ward)
                elif self.maze[x][y] == 6:
                    self.cells[x][y].ward = "Oncology"
                    #print(self.cells[x][y].ward)
                elif self.maze[x][y] == 7:
                    self.cells[x][y].ward = "ICU"
                    #print(self.cells[x][y].ward)
                elif self.maze[x][y] == 8:
                    self.cells[x][y].ward = "Isolation Ward"
                    #print(self.cells[x][y].ward)
                elif self.maze[x][y] == 9:
                    self.cells[x][y].ward = "Pediatric Ward"
                    #print(self.cells[x][y].ward)
                elif self.maze[x][y] == 10:
                    self.cells[x][y].ward = "Burn Ward"
                    #print(self.cells[x][y].ward)
                elif self.maze[x][y] == 11:
                    self.cells[x][y].ward = "Hematology"
                    #print(self.cells[x][y].ward)
                elif self.maze[x][y] == 12:
                    self.cells[x][y].ward = "Medical Ward"
                    #print(self.cells[x][y].ward)
                elif self.maze[x][y] == 0:
                    self.cells[x][y].ward = "Hallway"
                    #print(self.cells[x][y].ward)
                elif self.maze[x][y] == 14:
                    self.cells[x][y].ward = "Wall"
                    #print(self.cells[x][y].ward)
                self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size,
                                             (x + 1) * self.cell_size, fill=color)


    def heuristic(self, pos):
        return (abs(pos[0] - self.goal_pos[0]) + abs(pos[1] - self.goal_pos[1]))



    ############################################################
    # A Star Search Algorithm 
    ############################################################
    ############################################################
    def run_astar(self, start, end):
        open_set = PriorityQueue()

        #### Add the start state to the queue
        open_set.put((0, start))

        #### Continue exploring until the queue is exhausted
        while not open_set.empty():
            current_cost, current_pos = open_set.get()
            current_cell = self.cells[current_pos[0]][current_pos[1]]

            #### Stop if goal is reached
            if current_pos == end:
                print("Path found!")
                self.reconstruct_path(end)
                break

            #### Agent goes E, W, N, and S, whenever possible
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_pos = (current_pos[0] + dx, current_pos[1] + dy)

                if 0 <= new_pos[0] < self.rows and 0 <= new_pos[1] < self.cols and not self.cells[new_pos[0]][new_pos[1]].is_wall:

                    #### The cost of moving to a new position is 1 unit
                    new_g = current_cell.g + 1

                    if new_g < self.cells[new_pos[0]][new_pos[1]].g:
                        ### Update the path cost g()
                        self.cells[new_pos[0]][new_pos[1]].g = new_g

                        ### Update the heurstic h()
                        self.cells[new_pos[0]][new_pos[1]].h = self.heuristic(new_pos)

                        ### Update the evaluation function for the cell n: f(n) = g(n) + h(n)
                        self.cells[new_pos[0]][new_pos[1]].f = new_g + self.cells[new_pos[0]][new_pos[1]].h
                        self.cells[new_pos[0]][new_pos[1]].parent = current_cell

                        #### Add the new cell to the priority queue
                        open_set.put((self.cells[new_pos[0]][new_pos[1]].f, new_pos))


    ############################################################
    # Dijsktra's Search Algorithm 
    ############################################################
    ############################################################

    def run_dij(self, start, end):
        
        open_set = PriorityQueue()

        #### Add the start state to the queue
        open_set.put((0, start))

        #### Continue exploring until the queue is exhausted
        while not open_set.empty():
            current_cost, current_pos = open_set.get()
            current_cell = self.cells[current_pos[0]][current_pos[1]]

            #### Stop if goal is reached
            if current_pos == end:
                print("Path found!")
                self.reconstruct_path(end)
                break

            #### Agent goes E, W, N, and S, whenever possible
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_pos = (current_pos[0] + dx, current_pos[1] + dy)

                if 0 <= new_pos[0] < self.rows and 0 <= new_pos[1] < self.cols and not self.cells[new_pos[0]][new_pos[1]].is_wall:

                    #### The cost of moving to a new position is 1 unit
                    new_g = current_cell.g + 1

                    if new_g < self.cells[new_pos[0]][new_pos[1]].g:
                        ### Update the path cost g()
                        self.cells[new_pos[0]][new_pos[1]].g = new_g


                        ### Update the evaluation function for the cell n: f(n) = g(n)
                        self.cells[new_pos[0]][new_pos[1]].f = new_g
                        self.cells[new_pos[0]][new_pos[1]].parent = current_cell

                        #### Add the new cell to the priority queue
                        open_set.put((self.cells[new_pos[0]][new_pos[1]].f, new_pos))




        ############################################################
        #### This is for the GUI part. No need to modify this unless
        #### screen changes are needed.
        ############################################################

    def reconstruct_path(self, end):
        current_cell = self.cells[end[0]][end[1]]
        path = []
        while current_cell.parent:
            x, y = current_cell.x, current_cell.y
            path.append((x, y))
            current_cell = current_cell.parent

        path.reverse()

        def draw_next_square():
            nonlocal path_index
            if path_index < len(path):
                pos = path[path_index]
                x, y = pos
                if pos in self.delivery_locations:  # Check if the position is one of the goal locations
                    self.cells[x][y].visited = True
                    self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size,
                                                 (x + 1) * self.cell_size, fill='maroon')
                else:
                    self.cells[x][y].visited = True
                    self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size,
                                                 (x + 1) * self.cell_size, fill='green2')
                path_index += 1
                self.root.after(100, draw_next_square)  # Schedule the next square to be drawn after 100ms

        path_index = 0
        draw_next_square()


def main():
    maze = [
        [0, 0, 0, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 14, 4, 4, 4, 4, 4, 4, 4, 4, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 14, 4, 4, 4, 4, 4, 4, 4, 4, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0],
        [0, 0, 0, 14, 4, 4, 4, 4, 4, 4, 4, 4, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0],
        [0, 0, 0, 14, 4, 4, 4, 4, 4, 4, 4, 4, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0],
        [0, 0, 0, 14, 4, 4, 4, 4, 4, 4, 4, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
         14, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 14, 4, 4, 4, 4, 4, 4, 4, 14, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 0, 0, 0, 0, 0,
         0, 0, 0, 0],
        [0, 0, 0, 14, 4, 4, 4, 4, 4, 14, 14, 14, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 0, 0, 0, 0,
         0, 0, 0, 0, 0],
        [0, 0, 0, 14, 4, 0, 0, 14, 14, 14, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 14, 14, 14,
         14, 14, 14, 14, 14, 14],
        [14, 14, 14, 14, 14, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 14, 3, 3, 3,
         3, 14, 1, 1, 14],
        [14, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 14, 0, 0, 0, 14, 3, 3, 3, 3,
         14, 1, 1, 14],
        [14, 0, 0, 0, 14, 8, 14, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 8, 8, 14, 0, 0, 3, 3, 3,
         3, 14, 1, 1, 14],
        [14, 0, 0, 0, 14, 8, 8, 14, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 8, 8, 14, 0, 0, 3, 3, 3,
         3, 14, 1, 1, 14],
        [14, 0, 0, 0, 14, 8, 8, 14, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 8, 8, 14, 0, 14, 3, 3, 3,
         3, 14, 1, 1, 14],
        [14, 0, 0, 0, 0, 14, 0, 0, 14, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 14, 14, 14, 14, 8, 8, 14, 0, 14, 3, 3,
         3, 3, 14, 1, 1, 14],
        [14, 0, 0, 0, 0, 0, 0, 0, 14, 2, 2, 2, 2, 2, 2, 2, 14, 14, 14, 2, 2, 2, 2, 14, 3, 3, 8, 8, 8, 14, 0, 14, 3, 3,
         3, 3, 14, 1, 1, 14],
        [14, 0, 0, 0, 0, 14, 6, 6, 14, 14, 2, 2, 2, 2, 2, 2, 14, 10, 14, 2, 2, 2, 2, 14, 3, 3, 8, 8, 8, 14, 0, 14, 14,
         14, 1, 1, 1, 1, 1, 14],
        [14, 0, 0, 0, 0, 14, 6, 6, 6, 14, 2, 2, 2, 2, 2, 2, 14, 10, 14, 14, 2, 2, 2, 14, 3, 14, 3, 3, 3, 14, 0, 0, 7, 7,
         1, 1, 1, 1, 1, 14],
        [14, 0, 0, 0, 0, 14, 6, 6, 6, 14, 2, 2, 2, 2, 2, 2, 14, 10, 10, 14, 2, 2, 2, 14, 14, 6, 3, 3, 3, 14, 0, 14, 7,
         7, 14, 14, 14, 14, 14, 14],
        [14, 0, 0, 0, 0, 14, 6, 6, 6, 14, 14, 14, 14, 14, 14, 14, 10, 10, 10, 14, 2, 2, 2, 2, 14, 6, 6, 3, 3, 14, 0, 14,
         7, 7, 7, 7, 7, 7, 7, 14],
        [14, 0, 0, 0, 0, 14, 6, 6, 6, 14, 10, 10, 10, 10, 10, 10, 10, 10, 10, 14, 2, 2, 2, 2, 8, 6, 6, 6, 6, 14, 0, 14,
         7, 7, 7, 7, 7, 7, 7, 14],
        [14, 0, 0, 0, 0, 14, 6, 6, 6, 14, 10, 10, 10, 10, 10, 10, 10, 10, 10, 14, 2, 2, 0, 0, 8, 6, 6, 6, 6, 14, 0, 14,
         7, 7, 7, 7, 7, 7, 7, 14],
        [14, 0, 0, 0, 0, 14, 14, 14, 14, 14, 0, 14, 14, 14, 14, 14, 14, 0, 14, 14, 14, 14, 0, 0, 0, 0, 14, 14, 14, 0, 0, 0, 14, 14, 7, 7, 7, 7, 7, 14],
        [14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 14, 14, 14, 14, 14, 14],
        [14, 14, 14, 0, 0, 0, 0, 8, 6, 6, 14, 1, 1, 14, 14, 14, 11, 11, 11, 11, 11, 11, 14, 0, 0, 5, 5, 5, 5, 14, 0, 0, 6, 6, 6, 6, 6, 14, 14, 14],
        [0, 0, 14, 0, 0, 0, 0, 6, 6, 6, 14, 1, 1, 1, 1, 14, 11, 11, 11, 11, 11, 11, 14, 0, 14, 5, 5, 5, 5, 14, 6, 6, 6, 6, 6, 6, 6, 14, 0, 0],
        [0, 0, 14, 0, 0, 0, 14, 6, 6, 6, 14, 14, 14, 14, 14, 14, 11, 11, 11, 11, 11, 11, 14, 0, 14, 5, 5, 5, 5, 14, 6, 6, 6, 6, 6, 6, 6, 14, 0, 0],
        [0, 0, 14, 0, 0, 0, 14, 6, 6, 6, 6, 6, 14, 9, 9, 11, 11, 11, 11, 11, 14, 14, 14, 0, 0, 5, 5, 5, 5, 14, 6, 6, 6, 6, 6, 6, 6, 14, 0, 0],
        [0, 0, 14, 0, 0, 0, 14, 6, 6, 6, 6, 6, 14, 9, 9, 14, 14, 14, 14, 14, 14, 9, 14, 0, 0, 5, 5, 5, 5, 14, 6, 6, 6, 6, 6, 6, 6, 14, 0, 0],
        [0, 0, 14, 0, 0, 0, 14, 6, 6, 6, 14, 14, 14, 9, 9, 9, 9, 9, 9, 9, 9, 9, 14, 0, 14, 5, 5, 5, 5, 14, 6, 6, 6, 6, 6, 6, 6, 14, 0, 0],
        [0, 0, 14, 0, 0, 0, 14, 6, 6, 6, 14, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 14, 0, 14, 5, 5, 5, 5, 14, 14, 14, 14, 14, 14, 14, 14, 14, 0, 0],
        [0, 0, 14, 0, 0, 0, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 0, 14, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 14, 0, 0],
        [0, 0, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 14, 0, 0],
        [0, 0, 14, 0, 0, 14, 0, 14, 14, 14, 14, 0, 0, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 14, 14, 14, 14, 14, 0, 0],
        [0, 0, 14, 0, 0, 6, 6, 14, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 14, 4, 4, 14, 14, 5, 12, 14, 4, 4, 4, 4, 4, 14, 0, 0],
        [0, 0, 14, 0, 0, 6, 6, 14, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 14, 4, 4, 4, 14, 12, 12, 14, 4, 4, 4, 4, 4, 14, 0, 0],
        [0, 0, 14, 14, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 14, 4, 4, 4, 14, 12, 12, 14, 4, 4, 4, 4, 4, 14, 0, 0],
        [0, 0, 14, 8, 8, 8, 8, 14, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 14, 4, 4, 4, 14, 12, 12, 14, 4, 4, 4, 4, 4, 14, 0, 0],
        [0, 0, 14, 8, 8, 8, 8, 14, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 14, 4, 4, 4, 14, 12, 12, 14, 4, 4, 4, 4, 4, 14, 0, 0],
        [0, 0, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 0, 0],
    ]

    def read_input_file(filename):
        algorithms = []
        start_locations = ()
        delivery_locations = []

        priorities = {
            "ICU": 1, "Emergency": 1, "Oncology": 1, "Burn Ward": 1,
            "Surgical Ward": 2, "Maternity Ward": 2,
            "Hematology": 3, "Pediatric Ward": 3,
            "Medical Ward": 4, "General Ward": 4,
            "Admission": 5, "Isolation Ward": 5  # Corrected spelling
        }

        ward_locations = {
            "General Ward": (21, 23),
            "Surgical Ward": (24, 25),
            "Admissions": (17, 34),
            "Emergency": (11, 31),
            "Maternity": (8, 5),
            "Oncology": (24, 30),
            "ICU": (17, 31),
            "Isolation Ward": (10, 27),
            "Pediatric Ward": (33, 11),
            "Burn Ward": (22, 11),
            "Hematology": (24, 16),
            "Medical Ward": (34, 30),
        }
        '''
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith("Delivery algorithm"):
                    algorithms.extend(line.split(":")[1].rstrip('\n').split(","))
                elif line.startswith("Start location"):
                    start_locations = tuple(map(int, line.split(":")[1].strip()[1:-1].split(",")))
                elif line.startswith("Delivery locations"):
                    loc_str = line.split(":")[1].strip()
                    locations = loc_str[1:-1].split("), (")
                    for loc in locations:
                        x, y = map(int, loc.split(","))
                        delivery_locations.append((x, y))

        print("before sorting:", delivery_locations)
        # Sorting delivery locations based on their priority
        delivery_locations.sort(key=lambda loc: priorities.get(loc, float('inf')))
        print("after sorting:", delivery_locations)
        return algorithms, start_locations, delivery_locations
        '''
        try:
            with open(filename, 'r') as file:
                for line in file:
                    if line.startswith("Delivery algorithm"):
                        try:
                            algo_values = line.split(":")[1].rstrip('\n').split(",")
                            algorithms.extend(algo_values)
                        except IndexError:
                            print(f"Error: Incorrect format in line '{line.strip()}'")

                    elif line.startswith("Start location"):
                        try:
                            coordinates = line.split(":")[1].strip()[1:-1].split(",")
                            start_locations = tuple(map(int, coordinates))
                        except (ValueError, IndexError):
                            print(f"Error: Invalid start location format in line '{line.strip()}'")

                    elif line.startswith("Delivery locations"):
                        try:
                            loc_str = line.split(":")[1].strip()
                            locations = loc_str[1:-1].split("), (")
                            for loc in locations:
                                try:
                                    x, y = map(int, loc.split(","))
                                    delivery_locations.append((x, y))
                                except (ValueError, IndexError):
                                    print(f"Error: Invalid delivery location format in line '{line.strip()}'")
                        except IndexError:
                            print(f"Error: Incorrect format in line '{line.strip()}'")
                return algorithms, start_locations, delivery_locations

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    # Read input file
    if len(sys.argv) != 2:
        print("Usage error")
    else:
        input_file = sys.argv[1]
        algorithms, start_locations, delivery_locations = read_input_file(input_file)


    
    #algorithms, start_locations, delivery_locations = read_input_file("/Users/sarahgroark/Downloads/astar_input_file.txt")
    print(start_locations)
    print(delivery_locations)


    # Create maze game instance
    root = tk.Tk()
    root.title("A* Star Final Project")

    game = MazeGame(root, maze, algorithms, start_locations, delivery_locations)

    root.mainloop()




if __name__ == "__main__":
    main()
