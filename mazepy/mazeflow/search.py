class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class Maze():
    """Search algorithms, DFS, BFS, A*, Baseline."""
    def __init__(self, contents):
        
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Keep track of walls
        self.walls = []
        self.goals = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "G":
                        self.goals.append((i, j))
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True) #If has Wall
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        # self.solution = None
        self.solution = {}

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) in self.goals:
                    print("G", end="")
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


    def solve(self, frontier):
        from .frontier import AStar
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)

        self.explored = {}  
        count = 0
        for goal in self.goals:
            self.explored[goal] = set()

            if type(frontier) == AStar:
                frontier.__init__(self.start, goal)       
            else:  
                frontier.__init__()
            frontier.add(start)

            while True:
                if frontier.empty():
                    raise Exception("No solution")
                
                node = frontier.remove()

                if node.state == goal:
                    count += 1

                    actions = []
                    cells = []
                    while node.parent is not None:
                        actions.append(node.action)
                        cells.append(node.state)
                        node = node.parent
                    actions.reverse()
                    cells.reverse()
                    self.solution[goal] = (actions, cells)
                    
                    break

                self.explored[goal].add(node.state)

                for action, state in self.neighbors(node.state):
                    if not frontier.contains_state(state) and state not in self.explored[goal]:
                        child = Node(state=state, parent=node, action=action)
                        frontier.add(child)
                
        
        if count == len(self.goals):
            explored = set()
            num_explored = []
            for goal in self.goals:
                explored = explored | self.explored[goal]
                num_explored.append(len(self.explored[goal]))


            self.explored = explored
            explored = list(explored)
            
            self.num_explored = sum(num_explored) / len(self.goals)

            return 


    def plot(self, filename, show_solution=True, show_explored=False):
        """Create the figure of mazes and store in file named filename."""
        from PIL import Image, ImageDraw
        cell_size = 3
        cell_border = 1

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = []
        if self.solution is not None:
            for goal in self.goals:
                solution += self.solution[goal][1]
        else:
            solution = None

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Goal
                elif (i, j) in self.goals:
                    fill = (0, 171, 28)

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (10, 10, 255)

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

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



class Value_Iteration():
    """MDP Value Iteration"""
    from .generator import MDP_Grid
    def __init__(self, MDP: MDP_Grid) -> None:
        self.MDP = MDP


    
    def value_iteration(self, eps: float = 1e-3) -> tuple:

        V1 = {state: 0 for state in self.MDP.states}
        R, T, gamma = self.MDP.Reward, self.MDP.Transition, self.MDP.gamma

        epoch = 0
        while True:
            epoch += 1
            V = V1.copy()

            diff = 0
            for state in self.MDP.states:
                V1[state] = R(state) + gamma * max([
                    sum([
                        p * V[state_1] for (p, state_1) in T(state, action)
                    ]) for action in self.MDP.Action(state)
                ])            

                diff = max(diff, abs(V1[state] - V[state]))

            if diff < eps * (1-gamma) / gamma:
                return (V, epoch)
            
    def value_iteration_time(self, epoch: int = 10) -> list:
        V_time = []

        V1 = {state: 0 for state in self.MDP.states}
        R, T, gamma = self.MDP.Reward, self.MDP.Transition, self.MDP.gamma

        for _ in range(epoch):
            V = V1.copy()

            for state in self.MDP.states:
                V1[state] = R(state) + gamma * max([
                    sum([
                        p * V[state_1] for (p, state_1) in T(state, action)
                    ]) for action in self.MDP.Action(state)
                ])


            V_time.append(V)
        
        return V_time
    
    def plot_vu(self, epoch = 10) -> None:
        import matplotlib.pyplot as plt

        x = self.value_iteration_time(epoch=epoch)

        value_states = {k:[] for k in self.MDP.states}

        for i in x:
            for k, v in i.items():
                value_states[k].append(v)

        plt.figure(figsize=(8,5))
        for v in value_states:
            plt.plot(value_states[v])
            plt.legend(list(value_states.keys()),fontsize=14)
        plt.grid(True)
        plt.xlabel("Iterations",fontsize=14)
        plt.ylabel("Utilities of states",fontsize=14)
        plt.show()



    def best_policy(self, Value):
        def expected_value(action, state, Value, MDP):
            return sum([prob*Value[state_1] for (prob, state_1) in MDP.Transition(state, action)])
        
        pi = {}
        for state in self.MDP.states:
            pi[state] = max(
                self.MDP.Action(state),
                key=lambda action: expected_value(action, state, Value, self.MDP)
            )
        return pi
    

class Policy_iteration():
    """MDP Policy Iteration"""
    from .generator import MDP_Grid
    def __init__(self, MDP: MDP_Grid) -> None:
        self.MDP = MDP


    def policy_eval(self, pi, V, k = 20):
        R, T, gamma = self.MDP.Reward, self.MDP.Transition, self.MDP.gamma

        for i in range(k):
            for state in self.MDP.states:
                V[state] = R(state) + gamma * sum([
                    prob * V[state_1]
                    for (prob, state_1) in T(state, pi[state])
                ])

        return V


    def expected_value(self, action, state, Value):
        return sum([prob*Value[state_1] for (prob, state_1) in self.MDP.Transition(state, action)])
    
    
    def policy_iteration(self, verbose=0):        
        from random import choice
        V = {state: 0 for state in self.MDP.states}
        pi = {state: choice(self.MDP.Action(state)) for state in self.MDP.states}

        epoch = 0
        while True:
            epoch += 1
            V = self.policy_eval(pi, V, k = 20)

            Unchange = True

            for state in self.MDP.states:
                action = max(
                    self.MDP.Action(state),
                    key=lambda action: self.expected_value(action, state, V)
                )
                if action != pi[state]:
                    pi[state] = action
                    Unchange = False

                
            if Unchange:
                return (pi, epoch)
            
            if verbose:
                print(f"Policy epoch {epoch}: {pi}")


    def policy_iteration_grid(self, verbose=0):
        from random import choice
        V = {state: 0 for state in self.MDP.states}
        pi = {
            state: choice(self.MDP.Action(state))
            for state in self.MDP.states
        }


        epoch = 0
        while True:
            epoch += 1
            V = self.policy_eval(pi, V, k=20)
            Unchange = True

            for state in self.MDP.states:
                action = max(
                    self.MDP.Action(state),
                    key = lambda action: self.expected_value(action, state, V)
                )

            
            if action != pi[state]:
                pi[state] = action
                Unchange = False
            
            if Unchange:
                return (pi, epoch)