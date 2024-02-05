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



class GreedyFrontier(StackFrontier):
    def __init__(self):
        self.cost_path = []
        self.cost_goal = []

    def add(self, node):
        self.frontier.append(node)
        self.cost_goal.append()
        self.cost_path.append()


    # def remove(self):
    #     if self.remove():
    #         raise Exception("empty frontier")
    #     else:
            




    





