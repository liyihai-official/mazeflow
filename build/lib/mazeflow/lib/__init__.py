from numpy import abs
from numpy import sqrt

def max_norm(current, target):
    if len(current) != len(target):
        raise Exception("Incapable Coordinates")
    
    norm = 0
    for i in range(len(current)):
        norm += abs(current[i] - target[i])     
    return norm

def norm_2(current, target):
    if len(current) != len(target):
        raise Exception("Incapable Coordinates")
    
    norm = 0
    for i in range(len(current)):
        norm += (current[i] - target[i])**2
    
    return sqrt(norm) 


def load_maze(filename):
    with open(filename) as f:
        contents = f.read()

    # Validate start and goal
    if contents.count("A") != 1:
        raise Exception("maze must have exactly one start point")
    if contents.count("B") != 1:
        raise Exception("maze must have exactly one goal")

    # Determine height and width of maze
    contents = contents.splitlines()

    return contents