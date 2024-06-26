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

        self.cells = [[Cell(x, y, maze[x][y] == 1) for y in range(self.cols)] for x in range(self.rows)]

        # Initialize the agent position
        self.agent_pos = (self.start_locations)
        print("Start location: ", self.agent_pos)

        #### Start state's initial values for f(n) = g(n) + h(n)
        self.cells[self.agent_pos[0]][self.agent_pos[1]].g = 0
        self.cells[self.agent_pos[0]][self.agent_pos[1]].h = self.heuristic(self.agent_pos)
        self.cells[self.agent_pos[0]][self.agent_pos[1]].f = self.heuristic(self.agent_pos)

        self.cell_size = 20
        self.canvas = tk.Canvas(root, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg='white')
        self.canvas.pack()

        self.draw_maze()

        for pos in self.delivery_locations:
            print(pos)

        if self.algorithms[0] == "A*":
            for pos in self.delivery_locations:
                path = self.run_astar(self.agent_pos, pos)
                self.draw_path(path)
                self.agent_pos = pos




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
                if self.maze[x][y] == 14:
                    self.cells[x][y].is_wall = True  # Set is_wall to True for cells with value 14
                self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size,
                                             (x + 1) * self.cell_size, fill=color)

    def heuristic(self, pos):
        return (abs(pos[0] - self.goal_pos[0]) + abs(pos[1] - self.goal_pos[1]))



    ############################################################
    #### This is for the GUI part. No need to modify this unless
    #### screen changes are needed.
    ############################################################
    ############################################################
    def run_astar(self, start_pos, goal_pos):
        open_set = PriorityQueue()
        overall_path = []
        temp_path = []
        index = 0  # Initialize index here
        open_set.put((0, start_pos))


        while not open_set.empty():
            current_cost, current_pos = open_set.get()
            current_cell = self.cells[current_pos[0]][current_pos[1]]

            if current_pos == goal_pos:
                temp_path.append(current_pos)
                while current_cell.parent:
                    temp_path.append((current_cell.parent.x, current_cell.parent.y))
                    current_cell = current_cell.parent
                for item in reversed(temp_path):
                    overall_path.append(item)
                open_set.put((0, current_pos))
                print("Path found!")
                #self.draw_path(temp_path)
                temp_path = []
                break

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_pos = (current_pos[0] + dx, current_pos[1] + dy)

                if 0 <= new_pos[0] < self.rows and 0 <= new_pos[1] < self.cols and not self.maze[new_pos[0]][new_pos[1]] == 14:
                    new_g = current_cell.g + 1

                    if new_g < self.cells[new_pos[0]][new_pos[1]].g:
                        self.cells[new_pos[0]][new_pos[1]].g = new_g
                        self.cells[new_pos[0]][new_pos[1]].h = self.heuristic(new_pos)
                        self.cells[new_pos[0]][new_pos[1]].f = new_g + self.cells[new_pos[0]][new_pos[1]].h
                        self.cells[new_pos[0]][new_pos[1]].parent = current_cell
                        open_set.put((self.cells[new_pos[0]][new_pos[1]].f, new_pos))

        return overall_path

        ############################################################
        #### This is for the GUI part. No need to modify this unless
        #### screen changes are needed.
        ############################################################

    def draw_path(self, path):
        # rest of the code

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
        [0, 0, 0, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0],
        [0, 0, 0, 14, 4, 4, 4, 4, 4, 4, 4, 4, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0],
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
            (17, 31): 1, (11, 31): 1, (24, 30): 1, (22, 11): 1,
            (24, 25): 2, (8, 5): 2,
            (24, 15): 3, (33, 11): 3,
            (34, 30): 4, (21, 23): 4,
            (17, 34): 5, (10, 27): 5
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
            "Hematology": (24, 15),
            "Medical Ward": (34, 30),
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
                        x, y = ward_locations[ward_name]
                        start_locations = (x, y)
                elif "Delivery locations" in line:
                    for ward_name in line_data:
                        delivery_locations.append(ward_locations[ward_name])
        print("before sorting: ", delivery_locations)
        # Sorting delivery locations based on their priority
        delivery_locations.sort(key=lambda loc: priorities[loc], reverse=False)
        #print("after sorting: ", delivery_locations)
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
