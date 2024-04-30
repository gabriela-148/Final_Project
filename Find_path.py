from queue import PriorityQueue
import tkinter as tk
import time

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
        self.priority = 0
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

        self.priorities = {
            "ICU": 1, "Emergency": 1, "Oncology": 1, "Burn Ward": 1,
            "Surgical Ward": 2, "Maternity Ward": 2,
            "Hematology": 3, "Pediatric Ward": 3,
            "Medical Ward": 4, "General Ward": 4,
            "Admission": 5, "Isolation Ward": 5  # Corrected spelling
        }
        self.priorities_all = {
                                1: [],
                                2: [],
                                3: [],
                                4: [],
                                5: []
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
            #print(self.delivery_locations)
            #self.delivery_locations = self.search_and_sort(self.delivery_locations)
            print(self.delivery_locations)
            starting = self.agent_pos
            for pos in self.delivery_locations:
                print("Start pos:", starting)
                self.run_astar(starting, pos)
                starting = pos
                print("End pos:", pos)

    def search_and_sort(self, input_list):
        result = []
        locations = []
        sorted_result = []
        for priority, positions in self.priorities_all.items():
            for position in self.delivery_locations:
                if position in input_list:
                    print(position[0], position[1], self.cells[position[0]][position[1]].priority)
                    cell_priority = self.cells[position[0]][position[1]].priority
                    result.append((self.cells[position[0]][position[1]].priority, position))
            break
        sorted_result = sorted(result, key=lambda x: x[0], reverse=True)  # Sort by priority, higher to lower
        for item in sorted_result:
            locations.append(item[1])
        return locations


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
                    self.cells[x][y].priority = 1
                    self.priorities_all[1].append((x,y))
                    print(self.cells[x][y].ward, self.cells[x][y].priority)
                elif self.maze[x][y] == 2:
                    self.cells[x][y].ward = "General Ward"
                    self.cells[x][y].priority = 2
                    self.priorities_all[2].append((x,y))
                    print((x, y), self.cells[x][y].ward, self.cells[x][y].priority)
                elif self.maze[x][y] == 3:
                    self.cells[x][y].ward = "Emergency"
                    self.cells[x][y].priority = 5
                    self.priorities_all[5].append((x,y))
                    print(self.cells[x][y].ward, self.cells[x][y].priority)
                elif self.maze[x][y] == 4:
                    self.cells[x][y].ward = "Maternity"
                    self.cells[x][y].priority = 4
                    self.priorities_all[4].append((x,y))
                    print(self.cells[x][y].ward, self.cells[x][y].priority)
                elif self.maze[x][y] == 5:
                    self.cells[x][y].ward = "Surgical Ward"
                    self.cells[x][y].priority = 4
                    self.priorities_all[4].append((x,y))
                    print(self.cells[x][y].ward, self.cells[x][y].priority)
                elif self.maze[x][y] == 6:
                    self.cells[x][y].ward = "Oncology"
                    self.cells[x][y].priority = 5
                    self.priorities_all[5].append((x,y))
                    print(self.cells[x][y].ward, self.cells[x][y].priority)
                elif self.maze[x][y] == 7:
                    self.cells[x][y].ward = "ICU"
                    self.cells[x][y].priority = 5
                    self.priorities_all[5].append((x,y))
                    print(self.cells[x][y].ward, self.cells[x][y].priority)
                elif self.maze[x][y] == 8:
                    self.cells[x][y].ward = "Isolation Ward"
                    self.cells[x][y].priority = 1
                    self.priorities_all[1].append((x,y))
                    print(self.cells[x][y].ward, self.cells[x][y].priority)
                elif self.maze[x][y] == 9:
                    self.cells[x][y].ward = "Pediatric Ward"
                    self.cells[x][y].priority = 3
                    self.priorities_all[3].append((x,y))
                    print((x,y), self.cells[x][y].ward, self.cells[x][y].priority)
                elif self.maze[x][y] == 10:
                    self.cells[x][y].ward = "Burn Ward"
                    self.cells[x][y].priority = 5
                    self.priorities_all[5].append((x,y))
                    print((x,y), self.cells[x][y].ward, self.cells[x][y].priority)
                elif self.maze[x][y] == 11:
                    self.cells[x][y].ward = "Hematology"
                    self.cells[x][y].priority = 3
                    self.priorities_all[3].append((x,y))
                    print((x, y), self.cells[x][y].ward, self.cells[x][y].priority)
                elif self.maze[x][y] == 12:
                    self.cells[x][y].ward = "Medical Ward"
                    self.cells[x][y].priority = 2
                    self.priorities_all[2].append((x,y))
                    print(self.cells[x][y].ward, self.cells[x][y].priority)
                elif self.maze[x][y] == 0:
                    self.cells[x][y].ward = "Hallway"
                    self.cells[x][y].priority = 0
                    print(self.cells[x][y].ward, self.cells[x][y].priority)
                elif self.maze[x][y] == 14:
                    self.cells[x][y].ward = "Wall"
                    self.cells[x][y].priority = 0
                    print(self.cells[x][y].ward, self.cells[x][y].priority)
                self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size,
                                             (x + 1) * self.cell_size, fill=color)


    def heuristic(self, pos):
        return (abs(pos[0] - self.goal_pos[0]) + abs(pos[1] - self.goal_pos[1]))

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

                if 0 <= new_pos[0] < self.rows and 0 <= new_pos[1] < self.cols and not self.cells[new_pos[0]][
                    new_pos[1]].is_wall:

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
    ############################################################
    def run_astar(self, start, end):
        open_set = PriorityQueue()

        #### Add the start state to the queue
        open_set.put((0, start))

        #### Continue exploring until the queue is exhausted
        while not open_set.empty():
            print("Queue size", open_set.qsize())
            if open_set.qsize() > 200:
                print("Queue is too long")
                self.run_astar(start, end)
            current_cost, current_pos = open_set.get()
            current_cell = self.cells[current_pos[0]][current_pos[1]]

            #### Stop if goal is reached
            if current_pos == end:
                print("Path found!")
                open_set.put((0, end))
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
        start_location = ()
        delivery_locations = []
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

        return algorithms, start_locations, delivery_locations

    # Read input file
    algorithms, start_locations, delivery_locations = read_input_file(
        "/Users/ghuegel/Downloads/aifinalprojectfiles/astar_input_file.txt")
    print(start_locations)
    print(delivery_locations)

    # Example usage:

    # Create maze game instance
    root = tk.Tk()
    root.title("A* Star Final Project")

    game = MazeGame(root, maze, algorithms, start_locations, delivery_locations)

    root.mainloop()




if __name__ == "__main__":
    main()