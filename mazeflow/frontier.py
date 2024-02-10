import mazeflow.lib as lib

class StackFrontier():
    """
    The stack frontier which stands for the depth first search (DFS)
    """
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
    

class GreedyFrontier(StackFrontier):
    def __init__(self, start, goal):
        self.frontier = []
        self.goal = goal 
        self.start = start 

        self.cost = []

    def add(self, node):
        self.frontier.append(node)

        cost_path = lib.norm_2(self.start, node.state)
        cost_goal = lib.norm_2(self.goal, node.state)
        self.cost.append(cost_goal + cost_path)
        
    
    def remove(self):
        if len(self.frontier) == 0:
            raise Exception("empty frontier")
        else:
            min_cost = min(self.cost)
            min_index = self.cost.index(min_cost)

            node = self.frontier[min_index]

            del self.cost[min_index]
            del self.frontier[min_index]

            return node
            
            




    





