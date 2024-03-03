from mazepy import mazeflow as mf

import argparse
import os

from joblib import Parallel, delayed

argumens = ["size", "thread", "number", "file", "location"]

def command_line_parser():
    """Command line arguments.
    
    -s : size, the size of maze
    -n : number, the number of generating mazes.
    -t : thread, the number of threads of this generator

    -f : file, the name of saving file.
    -l : location, the location of saving file.
    """


    parser = argparse.ArgumentParser(description="Process information of maze.")
    
    group_maze = parser.add_argument_group("General infos")
    group_maze.add_argument("-s", f"--{argumens[0]}", type=int, default=10, required=True, help="size of the Square maze. (default: %(default)s)")
    group_maze.add_argument("-t", f"--{argumens[1]}", type=int, default=-1, help="number of thread for generate mazes. (default: %(default)s)")
    group_maze.add_argument("-n", f"--{argumens[2]}", type=int, default=1, required=True, help="the number of generated maze that has solution. (default: %(default)s)")
    
    group_save = parser.add_argument_group("Save infos")
    group_save.add_argument("-f", f"--{argumens[3]}", type=str, default="10", help="file name prefix (default: '%(default)s')")
    group_save.add_argument("-l", f"--{argumens[4]}", type=str, default="outputs", help="location of outputs (default: '%(default)s')")

    return parser


def gen_val_maze(epoch, shape, start, goals, number, figure_path, maze_path, plot=False, show_explored=True, show_solution=True):
    '''Generate Validate mazes using AStar search
    
    Inputs:
        - epoch: the id of iteration for loops
        - shape: the shape of mazes.
        - start: the start position of mazes.
        - goals: the goals of mazes.
        - number: the number of generate mazes.
        - figure_path: the relative path of saving figure.
        = maze_path: the relative path of saving mazes.
        - plot: generate the figure of mazes.
        - show_explored: shows the explored nodes in the maze if it plots.
        - show_solution: shows the solution path in the maze if it plots.

    Output:
        - return 0 if the maze has no solutions, 1 if the maze has solutions.    
    '''
    Generator = mf.generator.Generator2D(grid_shape=shape, start=start, goals=goals)
    Generator.generate_walls_array(threshold=0.05)

    Grid_World = Generator.save(save=False)
    Explorer = mf.search.Maze(Grid_World)

    num_files = len(os.listdir(maze_path))

    if num_files >= number:
        return 0
    else:
        try:
            Explorer.solve(mf.frontier.AStar(start=start, goal=goals))

            if plot:
                Explorer.plot(figure_path+f"/Maze{len(os.listdir(maze_path))}.png", show_explored=show_explored, show_solution=show_solution)
            Generator.save(maze_path+f"/Maze{len(os.listdir(maze_path))}.txt", save=True)
            Explorer.print()
            return 1
        
        except:
            return 0


def main(args):
    """Main function of generate mazes."""

    width, height = args.size, args.size
    shape = [height, width]

    start = (height // 2, width // 2)
    goals = [(1, 1), (1, width-2), (height-2, 1), (height-2, width-2)]

    figure_path = args.location + "/figures/" + args.file
    maze_path = args.location + "/mazes/" + args.file

    os.makedirs(figure_path, exist_ok=True)
    os.makedirs(maze_path, exist_ok=True)

    plot = False
    show_explored = True
    show_solution = True
    while len(os.listdir(maze_path)) < args.number:
        max_loop = args.number - len(os.listdir(maze_path))
        items = range(max_loop)
        
        # Parallelizing 
        Parallel(n_jobs=args.thread)(delayed(gen_val_maze)(item, shape, start, goals, args.number, figure_path, maze_path, plot=plot, show_explored=show_explored, show_solution=show_solution) for item in items)
        if len(os.listdir(maze_path)) >= args.number:
            break

    print(f"Generate {len(os.listdir(maze_path))} Mazes.")


if __name__ == "__main__":
    parser = command_line_parser()
    args = parser.parse_args()

    main(args)

    os.makedirs("params", exist_ok=True)
    with open(f'params/param{args.size}', 'w') as file:
        # Write into file
        for i, param in enumerate(argumens):
            contents = f"\t{param}\n{getattr(args, argumens[i])}\n"
            file.write(contents)


