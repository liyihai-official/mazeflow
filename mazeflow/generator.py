from random import randint
from numpy import zeros, abs, maximum
from noise import pnoise2 

from .lib.common import load_maze

# from mazeflow.lib import load_maze
# from .lib import load_maze
# from lib import load_maze

# 设计障碍物
# class Shaper2D():
#     def __init__(self, grid, shape) -> None:
#         self.height, self.width = grid.shape
#         self.shape = shape
        
#         if not isinstance(shape, str):
#             raise TypeError("Shape must be a string")
        
#         valid_shapes = ["circle", "square", "rectangle", "ring"]  # 假设这是你认可的形状类型列表
#         if shape.lower() not in valid_shapes:
#             raise ValueError(f"Invalid shape type, Valid types: {valid_shapes}")
        
#     def inside(self, row, col, radius = None, tol = 1e-4):
#         if self.shape == "square" or self.shape == "rectangle":
#             return True
#         elif self.shape == "circle":
#             r2 = (row - self.height/2)**2 + (col - self.width/2)**2
            
#             if r2 <= radius[0]**2 + tol:
#                 return True
#             else:
#                 return False
#             j
#         elif self.shape == "ring":
#             r2 = (row - self.height/2)**2 + (col - self.width/2)**2
            
#             if  r2-radius[0]**2 > tol and r2-radius[1]**2 < tol:
#                 return True
#             else:
#                 return False

class Generator2D():
    def __init__(self, grid_shape, start, goals, maze_shape_info:tuple=None):
        self.height, self.width = grid_shape # [height, width]

        self.start = start
        self.goals = goals

        self.wall_map = zeros((self.height, self.width), dtype=int)

        self.get_big_nums()

        # self.shape, self.radius = maze_shape_info

    def get_big_nums(self):
        big_num = 2 ** 16
        self.x = randint(-big_num, big_num)
        self.y = randint(-big_num, big_num)

    def generate_noise_array(self):
        noise_map = zeros((self.height, self.width))
        for i in range(self.height):
            i1 = i / 10 + self.x
            for j in range(self.width):
                j1 = j / 10 + self.y
                noise_map[i][j] = pnoise2(i1, j1)
        abs(noise_map, out=noise_map)
        return noise_map

    def generate_walls_array(self, threshold=0.5):
        def set_outer_to_one(matrix):
            matrix[0, :] = 1
            matrix[-1, :] = 1
            matrix[:, 0] = 1
            matrix[:, -1] = 1
            return matrix
        
        noise_map = self.generate_noise_array()
        self.wall_map[noise_map < threshold] = 1
        self.wall_map = set_outer_to_one(self.wall_map)

        # 为了生成障碍物
        # Shaper = Shaper2D(self.wall_map, self.shape)
        # for i in range(self.height):
        #     for j in range(self.width):
        #         if Shaper.inside(i, j, self.radius):
        #             self.wall_map[i][j] = 1

        
        
        self.wall_map[self.start] = 0
        for goal in self.goals:
            self.wall_map[goal] = 0

        return self.wall_map


    def MDP_reward_grid(grid, goals, main_reward = -0.04, goal_rewards = [1.00,-1.00]):
        """ Generate a list of list to feed the main GridMDP class.
        
        
        Inputs:
            - grid: list, of length ROW, and length COL for its entities.
                - 1s and 0s where 1 stand for Wall
            - terminals: The list of coordinates of terminals.
                - The entities are the tuple (x, y)s.
            - main_reward: A decimal number in double precision.
                -  For reward in whole grid world.
            - terminal_rewards: A list of decimal numbers.
                - Stand for the reward of terminals.
            
            Output:
            - y: The list of lists, length
                - The length of internal list is the column of grid world
                - The length of list is the row number of grid world.
                - Values are the reward of its position.
                - None stands for the Wall.
            """

        nrows = len(grid)
        ncols = len(grid[0])

        x = [[main_reward] * ncols for i in range(nrows)]

        for row in range(nrows):
            for col in range(ncols):
                if grid[row][col] == "#":
                    x[row][col] = None
        
        for i, t in enumerate(goals):
            x[t[0]][t[1]] = goal_rewards[i]

        return x

    def save(self, filename=None, save=False):
        contents = []
        for i, row in enumerate(self.wall_map):
            row_ = []
            for j, col in enumerate(row):
                if (i, j) in self.goals:
                    row_.append("G")
                elif (i, j) == self.start:
                    row_.append("A")
                elif col:
                    row_.append("#")
                else:
                    row_.append(" ")
            contents.append(row_)
    
        if save:
            with open(filename, 'w') as file:
                for i, row in enumerate(self.wall_map):
                    for j, col in enumerate(row):
                        if (i, j) in self.goals:
                            file.write("G")
                        elif (i, j) == self.start:
                            file.write("A")
                        elif col:
                            file.write(f"#")
                        else:
                            file.write(f" ")
                    file.write('\n')
        return contents
                

    def print(self, grid=None):
        if not grid:
            grid = self.save()

        for row in grid:
            for item in row:
                print(f"{item} ", end="")
            print()
        print()

    def plot(self, filename):
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

        # Load the image you want to use for filling
        fill_image = Image.open("wall.png")  # Replace with the path to your image

        for i, row in enumerate(self.wall_map):
            for j, col in enumerate(row):

                # Walls
                if col:
                    # Paste the fill image for walls
                    img.paste(fill_image, (j * cell_size, i * cell_size))


                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) in self.goals:
                    fill = (0, 171, 28)

                # Empty cell
                else:
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)





class MDP():
    def __init__(self, start, actlist, goals, transitions = {}, reward = None, states = None, gamma = .9) -> None:
        """Initialize the members of Markov Decision Process class.

        Inputs:
            - start: (x, y), The initial position of MDP.
            - actlist: list or dictionary. Stores the actions of each position              ???
            - goals: [(x1, y1), ..., (x2, y2)], A list of valid positions of goals in maze.
            - transitions: A dictionary of dictionaries of states default by {}.
                - Member of transitions: {action: transition matrix}.
                - transition matrix is a matrix store as dictionary.
            - reward: 
            - states: 
            - gamma: A number default as 0.9 which must in (0, 1].

        """
        if not (0 < gamma <= 1.): 
            raise ValueError("Gamma must in (0, 1]")
        
        if transitions == {}:
            print("WARNING: Transition is Empty")

        self.start = start
        self.gamma = gamma
        self.transitions = transitions
        self.goals = goals

        if states:
            self.states = states
        else:
            self.get_states_from_transitions(transitions)
        
        if reward:
            self.reward = reward
        else:
            self.reward = {state: 0 for state in self.states}

        
        if isinstance(actlist, list):
            self.actlist = actlist
        elif isinstance(actlist, dict):
            self.actlist = actlist

    def Reward(self, state):
        return self.reward[state]
    
    def Transition(self, state, action):
        if (self.transitions == {}):
            raise ValueError("Empty Transitions")
        else:
            return self.transitions[state][action]
        
    def Action(self, state):
        if state in self.goals:
            return [None]
        else:
            return self.actlist
        
    def get_state_from_transitions(self, transitions):
        if isinstance(transitions, dict):
            set1 = set(transitions.keys())
            set2 = set([
                tr[1]
                for actions in transitions.values()
                for action in actions.values()
                for tr in action
            ])

            return set1.union(set2)
        else:
            print("No States from Transitions.")
            return None
        

class MDP_Grid(MDP):
    def __init__(self, grid, goals, start=(1, 1), gamma=.9):
        reward = {}
        states = set()


        self.rows = len(grid)
        self.cols = len(grid[0])
        self.grid = grid

        for x in range(self.rows):
            for y in range(self.cols):
                if grid[x][y] is not None:
                    states.add((x, y))
                    reward[(x, y)] = grid[x][y]

        self.states = states

        self.orientations = EAST, NORTH, WEST, SOUTH = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        actlist = self.orientations

        transitions = {}
        for state in states:
            transitions[state] = {}
            for action in actlist:
                transitions[state][action] = self.get_trans_mat(state, action)

        MDP.__init__(self, start, 
                     actlist=actlist,
                     goals=goals,
                     transitions=transitions,
                     reward=reward,
                     states=states,
                     gamma=gamma)
        
    def Transition(self, state, action):
        """ Get the transition Markov Vector of given state and action.

        Inputs:
            - state: (x, y), A coordinates of current position in the Grid.
            - action: (x, y), Stands for the Operation of ONE-step Movement.
        
        Output:
            - A list,                                                                 ??
        """
        if action is None:
            return [(0.0, state)]
        else:
            return self.transitions[state][action]
        

    def get_trans_mat(self, state, action):
        """Get the transition Matrix of MDP for input state & action.

        Inputs:
        - state: (x, y), coordinate of current state.
        - action: (x, y), an member of orientations.
            - orientations: a list of possibly available actions. 

        Output:
        - A list of (probability, state_next).
            - [(0, 0), state], if action is empty.
        """
        turns = LEFT, RIGHT = (+1, -1)
        def turn(head, inc, directions=self.orientations):
            return directions[(
                (directions.index(head) + inc) % len(directions)
            )]

        if action is None:
            return [(0, 0), state]
        else:
            return [(0.8, self.go(state, action)),
                    (0.1, self.go(state, turn(action, RIGHT))),
                    (0.1, self.go(state, turn(action, LEFT)))]
        
        
    def go (self, state, direction):
        """ Operate an action on input state.

        Inputs:
            - state: (x, y), coordinate of current state.
            - direction:  (x, y), Direction of action, the entity of orientations.
                - orientations = EAST, NORTH, WEST, SOUTH = [(1, 0), (0, 1), (-1, 0), (0, -1)].

        Output:
            - state: (x, y), if acted state is valid for the Grid.
        """

        from operator import add
        def vector_add(a,b):
            return tuple(map(add, a, b))
        
        state_0 = vector_add(state, direction)

        return state_0 if state_0 in self.states else state