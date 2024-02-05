def load(filename):
    # Read file and set height and width of maze
    with open(filename) as f:
        contents = f.read()

    # Validate start and goal
    if contents.count("A") != 1:
        raise Exception("maze must have exactly one start point")
    if contents.count("B") != 1:
        raise Exception("maze must have exactly one goal")

    # Determine height and width of maze
    contents = contents.splitlines()

    height = len(contents)
    width = max(len(line) for line in contents)
    return contents