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
            (11, 31): 5, (11, 31): 5, (24, 30): 5, (22, 11): 5,
            (24, 25): 4, (8, 6): 4,
            (24, 15): 3, (33, 11): 3,
            (34, 30): 2, (21, 23): 2,
            (23, 11): 1, (10, 27): 1
        }

        sorted_ward_dict = self.sort_ward_locations(delivery_locations, priorities)

        # Organize delivery locations by priority
        self.goal_pos_queue = self.build_queue(sorted_ward_dict)
        self.goal_pos = self.delivery_locations[len(self.delivery_locations)-1]

        self.cells = [[Cell(x, y, maze[x][y] == 1) for y in range(self.cols)] for x in range(self.rows)]
        print("Start location: ", self.start_locations)

        # Initialize the agent position
        self.agent_pos = self.start_locations

        #### Start state's initial values for f(n) = g(n) 
        self.cells[self.agent_pos[0][0]][self.agent_pos[0][1]].g = 0
        self.cells[self.agent_pos[0][0]][self.agent_pos[0][1]].h = self.heuristic(self.agent_pos[0])
        self.cells[self.agent_pos[0][0]][self.agent_pos[0][1]].f = self.heuristic(self.agent_pos[0])

        self.cell_size = 20
        self.canvas = tk.Canvas(root, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg='white')
        self.canvas.pack()

        self.draw_maze()

        if self.algorithms[0]=="A*":
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

        print(start_ward)
        print(delivery_wards)
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
            14: 'black'
        }

        for x in range(self.rows):
            for y in range(self.cols):
                color = color_map[self.maze[x][y]]
                self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size,
                                             (x + 1) * self.cell_size, fill=color)

    def heuristic(self, pos):
        return (abs(pos[0] - self.goal_pos[0]) + abs(pos[1] - self.goal_pos[1]))

    ############################################################
    #### Dijsktra's Search Algorithm
    ############################################################
    def run_dij(self):
        open_set = PriorityQueue()


        # Add the start state to the queue
        open_set.put((0, self.agent_pos))

        visited_goals = set()
        
        # Continue exploring until the queue is exhausted
        while not open_set.empty() and len(visited_goals) < len(self.delivery_locations):
            #print("Queue:", open_set.queue)
            current_cost, current_pos = open_set.get()

            # Ensure current_pos is a tuple of integers
            current_pos = (current_pos[0]), (current_pos[1])

            current_cell = self.cells[current_pos[0]][current_pos[1]]
            #print("Goal pos:", self.goal_pos)

            # Stop if the current position is the first delivery location
            if current_pos in self.delivery_locations and current_pos not in visited_goals:
                visited_goals.add(current_pos)
                self.reconstruct_path()
                print("Success! Path found")

                open_set = PriorityQueue()
                open_set.put((0,self.current_pos))

                

            # Agent goes E, W, N, and S, whenever possible
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_pos = (current_pos[0] + dx, current_pos[1] + dy)
                #print("Current position: ", current_pos)
                #print("current:", new_pos)
                #print("Cost:", current_cost)

                if 0 <= new_pos[0] < self.rows and 0 <= new_pos[1] < self.cols and self.maze[new_pos[0]][
                    new_pos[1]] != 14:
                    # The cost of moving to a new position is 1 unit
                    new_g = current_cell.g + 1
                    #print("Current cell cost", new_g)

                    if new_g < self.cells[new_pos[0]][new_pos[1]].g:
                        # Update the path cost g()
                        self.cells[new_pos[0]][new_pos[1]].g = new_g


                        # Update the evaluation function for the cell n: f(n) = g(n) 
                        self.cells[new_pos[0]][new_pos[1]].f = 2 * new_g
                        self.cells[new_pos[0]][new_pos[1]].parent = current_cell

                        # Add the new cell to the priority queue
                        open_set.put((self.cells[new_pos[0]][new_pos[1]].f, new_pos))

    ############################################################
    #### A* Search Algorithm
    ############################################################


    def run_astar(self):
            open_set = PriorityQueue()

        # Add the start state to the queue
            open_set.put((0, self.agent_pos))
        # Continue exploring until the queue is exhausted
            while not open_set.empty():
                print("Queue:", open_set.queue)
                current_cost, current_pos = open_set.get()

            # Ensure current_pos is a tuple of integers
                current_pos = (current_pos[0][0]), (current_pos[0][1])

                current_cell = self.cells[current_pos[0]][current_pos[1]]
                print("Goal pos:", self.goal_pos)

            # Stop if the current position is the first delivery location
                if current_pos == self.goal_pos:
                    self.reconstruct_path()
                    print("Success! Path found")
                    break

            # Agent goes E, W, N, and S, whenever possible
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    new_pos = (current_pos[0] + dx, current_pos[1] + dy)
                # print("Current position: ", current_pos)
                    #print("current:", new_pos)
                    #print("Cost:", current_cost)

                if 0 <= new_pos[0] < self.rows and 0 <= new_pos[1] < self.cols and not self.maze[new_pos[0]][
                    new_pos[1]] != 14:
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
                        open_set.put((self.cells[new_pos[0]][new_pos[1]].f, new_pos))


    ############################################################
    #### This is for the GUI part. No need to modify this unless
    #### screen changes are needed.
    ############################################################
    def reconstruct_path(self):
        current_cell = self.cells[self.goal_pos[0]][self.goal_pos[1]]
        path = []

        while current_cell.parent:
            x,y = current_cell.x, current_cell.y
            path.append((x,y))
            current_cell = current_cell.parent

        def draw_path(path):
            for delivery_location in self.delivery_locations:
                print("drawing path to: ", delivery_location)
                print("Going to: ", delivery_location)
                for x,y in path:
                    print("current position: ", (x,y))
                    if (x,y) == delivery_location:
                         print("Match found for delivery location: ", delivery_location)
                         self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size,
                                         (x + 1) * self.cell_size, fill='DimGray')
                         print("Found path to: ", delivery_location)
                         time.sleep(1)
                         
                    else:
                         print("no match for delivery location: ", delivery_location)
                         self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size,
                                         (x + 1) * self.cell_size, fill='green2')
                         self.root.update_idletasks()
                         self.root.after(100)



        # Start drawing the path with the current cell
        draw_path(path[::-1])


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
        [0, 0, 0, 14, 4, 4, 4, 4, 4, 4, 4, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 14, 4, 4, 4, 4, 4, 4, 4, 14, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 14, 4, 4, 4, 4, 4, 14, 14, 14, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 14, 4, 0, 0, 14, 14, 14, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14],
        [14, 14, 14, 14, 14, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 14, 3, 3, 3, 3, 14, 1, 1, 14],
        [14, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 14, 0, 0, 0, 14, 3, 3, 3, 3, 14, 1, 1, 14],
        [14, 0, 0, 0, 14, 8, 14, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 8, 8, 14, 0, 0, 3, 3, 3, 3, 14, 1, 1, 14],
        [14, 0, 0, 0, 14, 8, 8, 14, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 8, 8, 14, 0, 0, 3, 3, 3, 3, 14, 1, 1, 14],
        [14, 0, 0, 0, 14, 8, 8, 14, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 8, 8, 14, 0, 14, 3, 3, 3, 3, 14, 1, 1, 14],
        [14, 0, 0, 0, 0, 14, 0, 0, 14, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 14, 14, 14, 14, 8, 8, 14, 0, 14, 3, 3, 3, 3, 14, 1, 1, 14],
        [14, 0, 0, 0, 0, 0, 0, 0, 14, 2, 2, 2, 2, 2, 2, 2, 14, 14, 14, 2, 2, 2, 2, 14, 3, 3, 8, 8, 8, 14, 0, 14, 3, 3, 3, 3, 14, 1, 1, 14],
        [14, 0, 0, 0, 0, 14, 6, 6, 14, 14, 2, 2, 2, 2, 2, 2, 14, 10, 14, 2, 2, 2, 2, 14, 3, 3, 8, 8, 8, 14, 0, 14, 14, 14, 1, 1, 1, 1, 1, 14],
        [14, 0, 0, 0, 0, 14, 6, 6, 6, 14, 2, 2, 2, 2, 2, 2, 14, 10, 14, 14, 2, 2, 2, 14, 3, 14, 3, 3, 3, 14, 0, 0, 7, 7, 1, 1, 1, 1, 1, 14],
        [14, 0, 0, 0, 0, 14, 6, 6, 6, 14, 2, 2, 2, 2, 2, 2, 14, 10, 10, 14, 2, 2, 2, 14, 14, 6, 3, 3, 3, 14, 0, 14, 7, 7, 14, 14, 14, 14, 14, 14],
        [14, 0, 0, 0, 0, 14, 6, 6, 6, 14, 14, 14, 14, 14, 14, 14, 10, 10, 10, 14, 2, 2, 2, 2, 14, 6, 6, 3, 3, 14, 0, 14, 7, 7, 7, 7, 7, 7, 7, 14],
        [14, 0, 0, 0, 0, 14, 6, 6, 6, 14, 10, 10, 10, 10, 10, 10, 10, 10, 10, 14, 2, 2, 2, 2, 8, 6, 6, 6, 6, 14, 0, 14, 7, 7, 7, 7, 7, 7, 7, 14],
        [14, 0, 0, 0, 0, 14, 6, 6, 6, 14, 10, 10, 10, 10, 10, 10, 10, 10, 10, 14, 2, 2, 0, 0, 8, 6, 6, 6, 6, 14, 0, 14, 7, 7, 7, 7, 7, 7, 7, 14],
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
        [0, 0, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 0, 0],    ]

    def read_input_file(filename):
        algorithms = []
        start_locations = {}
        delivery_locations = {}

        ward_locations = {
            "General Ward": (21, 23),
            "Surgical Ward": (24, 25),
            "Admissions": (23, 11),
            "Emergency": (11, 31),
            "Maternity": (8, 6),
            "Oncology": (24, 30),
            "ICU": (17, 31),
            "Isolation Ward": (10, 27),
            "Pediatric Ward": (33, 11),
            "Burn Ward": (22, 11),
            "Hematogology": (24, 15),
            "Medical Ward": (34, 30),
        }

        with open(filename, 'r') as file:
            while True:
                line = file.readline()
                if not line:
                    break
                line_data = [item.strip() for item in line.split(":")[1].rstrip('\n').split(",")]
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
    algorithms, start_locations, delivery_locations = read_input_file("/Users/sarahgroark/final_proj/dijkstra_input_file.txt")
    print(start_locations)
    print(delivery_locations)



    # Create maze game instance
    root = tk.Tk()
    root.title("A* Star Final Project")

    game = MazeGame(root, maze, algorithms, start_locations, delivery_locations)

    root.mainloop()




if __name__ == "__main__":
    main()
