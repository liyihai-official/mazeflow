from mazepy import mazeflow as mf
import os
from joblib import Parallel, delayed

from generate_mazes import command_line_parser
from generate_mazes import gen_val_maze

def main(args):
    """ The main function of demo of generator. """
    width, height = args.size, args.size
    shape = [height, width]

    start = (height // 2, width // 2)
    goals = [(1, 1), (1, width-2), (height-2, 1), (height-2, width-2)]

    path = args.location + "_" + args.file
    figure_path = path + "/figures/"
    maze_path = path + "/mazes/"

    os.makedirs(figure_path, exist_ok=True)
    os.makedirs(maze_path, exist_ok=True)

    plot = True
    show_explored = False
    show_solution = False
    while len(os.listdir(maze_path)) < args.number:
        max_loop = args.number - len(os.listdir(maze_path))

        items = range(max_loop)
        Parallel(n_jobs=args.thread)(delayed(gen_val_maze)(item, shape, start, goals, args.number, figure_path, maze_path, plot=plot, show_explored=show_explored, show_solution=show_solution) for item in items)

        if len(os.listdir(maze_path)) >= args.number:
            break

    print(f"Generate {len(os.listdir(maze_path))} Mazes in ./{path}")



if __name__ == "__main__":
    parser = command_line_parser()
    args = parser.parse_args()

    main(args)