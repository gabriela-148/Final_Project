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

    def __lt__(self, other):
        return self.f < other.f

class MazeGame:
    def __init__(self, root, maze, algorithms, start_locations, delivery_locations):
        self.root = root
        self.maze = maze

        self.rows = len(maze)
        self.cols = len(maze[0])

        # Store start locations and delivery locations
        self.start_locations, self.delivery_locations = self.extract_ward_locations(start_locations, delivery_locations)

        self.algorithms = algorithms
        print(self.algorithms)

        ward_names_dict = {
            "General Ward": 0,
            "Surgical Ward": 1,
            "Admissions": 2,
            "Emergency": 3,
            "Maternity": 4,
            "Oncology": 5,
            "ICU": 6,
            "Isolation Ward": 7,
            "Pediatric Ward": 8,
            "Burn Ward": 9,
            "Hematology": 10,
            "Medical Ward": 11,
        }

        priorities = {
            (23, 32): 5, (11, 31): 5, (24, 30): 5, (22, 11): 5,
            (23, 26): 4, (8, 6): 4,
            (23, 16): 3, (33, 11): 3,
            (23, 26): 2, (21, 23): 2,
            (23, 11): 1, (10, 28): 1
        }

        sorted_ward_dict = self.sort_ward_locations(delivery_locations, priorities)



        # Organize delivery locations by priority
        self.goal_pos_queue = self.build_queue(sorted_ward_dict)
        self.goal_pos = self.delivery_locations[0]

        self.cells = [[Cell(x, y, maze[x][y] == 14) for y in range(self.cols)] for x in range(self.rows)]
        print("Start location: ", self.start_locations)
        # Initialize the agent position
        self.agent_pos = self.start_locations

        #### Start state's initial values for f(n) = g(n) + h(n)
        self.cells[self.agent_pos[0][0]][self.agent_pos[0][1]].g = 0
        self.cells[self.agent_pos[0][0]][self.agent_pos[0][1]].h = self.heuristic(self.agent_pos[0])
        self.cells[self.agent_pos[0][0]][self.agent_pos[0][1]].f = self.heuristic(self.agent_pos[0])

        self.cell_size = 20
        self.canvas = tk.Canvas(root, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg='white')
        self.canvas.pack()

        self.draw_maze()

        if self.algorithms[0] == "A*":
            self.run_astar()
        else:
            self.run_dij()

    def build_queue(self, sorted_ward_dict):
        priority_queue = PriorityQueue()
        for priority, ward_name, location in sorted_ward_dict:
            priority_queue.put((priority, ward_name, location))
        return priority_queue

    def extract_ward_locations(self, start_locations, delivery_locations):
        start_ward = []
        delivery_wards = []


        # Extract ward locations from start_locations
        for ward, location in start_locations.items():
            start_ward.append(location)

        # Extract ward locations from delivery_locations
        for location in delivery_locations.values():
            delivery_wards.append(location)

        return start_ward, delivery_wards

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
                self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size,
                                             (x + 1) * self.cell_size, fill=color)

    def heuristic(self, pos):
        return (abs(pos[0] - self.goal_pos[0]) + abs(pos[1] - self.goal_pos[1]))

    ############################################################
    #### Greedy Best-First Search Algorithm
    ############################################################
    def run_astar(self):
        open_set = PriorityQueue()
        deliveryNum = 0

        # Add the start state to the queue
        open_set.put((0, self.agent_pos))
        # Continue exploring until the queue is exhausted
        while not open_set.empty():
            #print("Queue:", open_set.queue)
            current_cost, current_pos = open_set.get()
            print("Current pos from queue: ", current_pos)

            # Ensure current_pos is a tuple of integers
            current_pos = (current_pos[0][0]), (current_pos[0][1])

            current_cell = self.cells[current_pos[0]][current_pos[1]]
            #print("Goal pos:", self.goal_pos)

            # Stop if the current position is the first delivery location
            if current_pos == self.goal_pos:
                print("Success! Path found")
                self.reconstruct_path()
                time.sleep(2)
                self.agent_pos = current_pos
                deliveryNum += 1
                if deliveryNum < len(self.delivery_locations):
                    self.goal_pos = self.delivery_locations[deliveryNum]
                    open_set = PriorityQueue()
                    open_set.put((0,self.agent_pos))
                else:
                    break
            # Agent goes E, W, N, and S, whenever possible
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_pos = (current_pos[0] + dx, current_pos[1] + dy)
                # print("Current position: ", current_pos)
                #print("current:", new_pos)
                #print("Cost:", current_cost)

                if 0 <= new_pos[0] < self.rows and 0 <= new_pos[1] < self.cols and not self.cells[new_pos[0]][
                    new_pos[1]].is_wall:
                    # The cost of moving to a new position is 1 unit
                    new_g = current_cell.g + 1
                    #print("Current cell cost", new_g)

                    if new_g < self.cells[new_pos[0]][new_pos[1]].g:
                        # Update the path cost g()
                        self.cells[new_pos[0]][new_pos[1]].g = new_g

                        # Update the heuristic h()
                        self.cells[new_pos[0]][new_pos[1]].h = self.heuristic(new_pos)

                        # Update the evaluation function for the cell n: f(n) = g(n) + h(n)
                        self.cells[new_pos[0]][new_pos[1]].f = 2 * new_g + 1 * self.cells[new_pos[0]][new_pos[1]].h
                        self.cells[new_pos[0]][new_pos[1]].parent = current_cell

                        # Add the new cell to the priority queue
                        open_set.put([self.cells[new_pos[0]][new_pos[1]].f, [new_pos]])  # Wrap the new_pos tuple in a list

    ############################################################
    #### This is for the GUI part. No need to modify this unless
    #### screen changes are needed.
    ############################################################

    def reconstruct_path(self):
        current_cell = self.cells[self.goal_pos[0]][self.goal_pos[1]]

        def draw_path(current_cell):
            if current_cell.parent:
                x, y = current_cell.x, current_cell.y
                self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size,
                                             (x + 1) * self.cell_size, fill='green')
                current_cell = current_cell.parent

                # Redraw cell with updated g() and h() values
                self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size,
                                             (x + 1) * self.cell_size, fill='skyblue')
                text = f'g={self.cells[x][y].g}\nh={self.cells[x][y].h}'
                self.canvas.create_text((y + 0.5) * self.cell_size, (x + 0.5) * self.cell_size, font=("Purisa", 12),
                                        text=text)

                # Schedule the next draw with a delay of 100 milliseconds
                self.root.after(100, draw_path, current_cell)

        # Start drawing the path with the current cell
        draw_path(current_cell)

    '''
    def reconstruct_path(self):
        current_cell = self.cells[self.goal_pos[0]][self.goal_pos[1]]
        path = []

        while current_cell.parent:
            x, y = current_cell.x, current_cell.y
            path.append((x, y))
            current_cell = current_cell.parent

        def draw_path(path):

            amt_goals = len(self.delivery_locations)
            counter = 0
            while counter < amt_goals:
                for x, y in path:
                    if (x, y) == self.delivery_locations[counter]:
                        self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size,
                                                     (x + 1) * self.cell_size, fill='DimGray')
                        time.sleep(1.5)
                        counter = counter + 1
                    else:
                        self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size,
                                                     (x + 1) * self.cell_size, fill='green2')

                        self.root.update_idletasks()
                        self.root.after(200)

        # Start drawing the path with the current cell
        draw_path(path[::-1])
    '''

    def sort_ward_locations(self, ward_dict, priorities):
        sorted_ward_list = []
        for ward_name in ward_dict:
            ward_coords = ward_dict[ward_name]
            priority = priorities.get(ward_coords, 0)
            sorted_ward_list.append((priority, ward_name, ward_coords))

        sorted_ward_list.sort(reverse=True)  # Sort in descending order of priority
        return sorted_ward_list


def main():
    maze = [
        [0, 0, 0, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 14, 4, 4, 4, 4, 4, 4, 4, 4, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 14, 4, 4, 4, 4, 4, 4, 4, 4, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 14, 4, 4, 4, 4, 4, 4, 4, 4, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 14, 4, 4, 4, 4, 4, 4, 4, 4, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 14, 4, 4, 4, 4, 4, 4, 4, 4, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 14, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 14, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 14, 4, 0, 0, 4, 4, 2, 2, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14],
        [14, 14, 14, 14, 14, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 14, 3, 3, 3, 3, 3, 1, 1, 14],
        [14, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 14, 3, 3, 3, 3, 3, 1, 1, 14],
        [14, 0, 0, 0, 14, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 8, 8, 14, 0, 0, 3, 3, 3, 3, 3, 1, 1, 14],
        [14, 0, 0, 0, 14, 8, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 8, 8, 14, 0, 0, 3, 3, 3, 3, 3, 1, 1, 14],
        [14, 0, 0, 0, 14, 8, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 8, 8, 14, 0, 14, 3, 3, 3, 3, 3, 1, 1, 14],
        [14, 0, 0, 0, 0, 14, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 8, 8, 14, 0, 14, 3, 3, 3, 3, 3, 1, 1, 14],
        [14, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 8, 8, 8, 14, 0, 14, 3, 3, 3, 3, 3, 1, 1, 14],
        [14, 0, 0, 0, 0, 14, 6, 6, 6, 6, 2, 2, 2, 2, 2, 2, 2, 10, 2, 2, 2, 2, 2, 2, 3, 3, 8, 8, 8, 14, 0, 14, 7, 7, 1, 1, 1, 1, 1, 14],
        [14, 0, 0, 0, 0, 14, 6, 6, 6, 6, 2, 2, 2, 2, 2, 2, 2, 10, 2, 2, 2, 2, 2, 2, 3, 6, 3, 3, 3, 14, 0, 0, 7, 7, 1, 1, 1, 1, 1, 14],
        [14, 0, 0, 0, 0, 14, 6, 6, 6, 6, 2, 2, 2, 2, 2, 2, 2, 10, 10, 2, 2, 2, 2, 2, 3, 6, 3, 3, 3, 14, 0, 14, 7, 7, 1, 1, 1, 1, 1, 14],
        [14, 0, 0, 0, 0, 14, 6, 6, 6, 6, 10, 10, 10, 10, 10, 10, 10, 10, 10, 2, 2, 2, 2, 2, 3, 6, 6, 3, 3, 14, 0, 14, 7, 7, 7, 7, 7, 7, 7, 14],
        [14, 0, 0, 0, 0, 14, 6, 6, 6, 6, 10, 10, 10, 10, 10, 10, 10, 10, 10, 2, 2, 2, 2, 2, 8, 6, 6, 6, 6, 14, 0, 14, 7, 7, 7, 7, 7, 7, 7, 14],
        [14, 0, 0, 0, 0, 14, 6, 6, 6, 6, 10, 10, 10, 10, 10, 10, 10, 10, 10, 2, 2, 2, 0, 0, 8, 6, 6, 6, 6, 14, 0, 14, 7, 7, 7, 7, 7, 7, 7, 14],
        [14, 0, 0, 0, 0, 14, 14, 14, 14, 14, 0, 14, 14, 14, 14, 14, 14, 0, 14, 14, 14, 14, 0, 0, 0, 0, 14, 14, 14, 0, 0, 0, 14, 7, 7, 7, 7, 7, 7, 14],
        [14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 14],
        [14, 14, 14, 0, 0, 0, 0, 8, 6, 6, 6, 1, 1, 1, 1, 1, 11, 11, 11, 11, 11, 11, 11, 0, 0, 5, 5, 5, 5, 6, 0, 0, 6, 6, 6, 6, 6, 14, 14, 14],
        [0, 0, 14, 0, 0, 0, 0, 6, 6, 6, 6, 1, 1, 1, 1, 1, 11, 11, 11, 11, 11, 11, 11, 0, 14, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 14, 0, 0],
        [0, 0, 14, 0, 0, 0, 14, 6, 6, 6, 6, 6, 6, 1, 1, 1, 11, 11, 11, 11, 11, 11, 11, 0, 14, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 14, 0, 0],
        [0, 0, 14, 0, 0, 0, 14, 6, 6, 6, 6, 6, 6, 9, 9, 11, 11, 11, 11, 11, 11, 9, 9, 0, 0, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 14, 0, 0],
        [0, 0, 14, 0, 0, 0, 14, 6, 6, 6, 6, 6, 6, 9, 9, 11, 11, 11, 11, 11, 11, 9, 9, 0, 0, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 14, 0, 0],
        [0, 0, 14, 0, 0, 0, 14, 6, 6, 6, 6, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 14, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 14, 0, 0],
        [0, 0, 14, 0, 0, 0, 14, 6, 6, 6, 6, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 14, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 14, 0, 0],
        [0, 0, 14, 0, 0, 0, 14, 6, 6, 6, 6, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 14, 5, 5, 5, 5, 6, 6, 6, 5, 5, 5, 5, 5, 14, 0, 0],
        [0, 0, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 14, 0, 0],
        [0, 0, 14, 0, 0, 14, 0, 14, 14, 14, 14, 0, 0, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 14, 0, 0],
        [0, 0, 14, 0, 0, 6, 6, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 4, 4, 4, 12, 5, 12, 12, 4, 4, 4, 4, 4, 14, 0, 0],
        [0, 0, 14, 0, 0, 6, 6, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 4, 4, 4, 12, 12, 12, 12, 4, 4, 4, 4, 4, 14, 0, 0],
        [0, 0, 14, 14, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 4, 4, 4, 12, 12, 12, 12, 4, 4, 4, 4, 4, 14, 0, 0],
        [0, 0, 14, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 4, 4, 4, 12, 12, 12, 12, 4, 4, 4, 4, 4, 14, 0, 0],
        [0, 0, 14, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 4, 4, 4, 12, 12, 12, 12, 4, 4, 4, 4, 4, 14, 0, 0],
        [0, 0, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 0, 0],
    ]

    def read_input_file(filename):
        algorithms = []
        start_locations = {}
        delivery_locations = {}

        ward_locations = {
            "General Ward": (21, 23),
            "Surgical Ward": (23, 26),
            "Admissions": (23, 11),
            "Emergency": (11, 31),
            "Maternity": (8, 6),
            "Oncology": (24, 30),
            "ICU": (23, 32),
            "Isolation Ward": (10, 28),
            "Pediatric Ward": (33, 11),
            "Burn Ward": (22, 11),
            "Hematogology": (23, 16),
            "Medical Ward": (23, 26),
        }

        with open(filename, 'r') as file:
            while True:
                line = file.readline()
                if not line:
                    break
                line_data = line.split(":")[1].rstrip('\n').split(",")
                if "Delivery algorithm" in line:
                    algorithms.extend(line_data)
                elif "Start location" in line:
                    for ward_name in line_data:
                        start_locations[ward_name] = ward_locations[ward_name]
                elif "Delivery locations" in line:
                    for ward_name in line_data:
                        delivery_locations[ward_name] = ward_locations[ward_name]

        return algorithms, start_locations, delivery_locations





    # Read input file
    algorithms, start_locations, delivery_locations = read_input_file("/Users/ghuegel/Downloads/aifinalprojectfiles/astar_input_file.txt")
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
