from mazepy import mazeflow as mf

from time import time
from joblib import Parallel, delayed

################################################################################
#                              Load parameters                                 #
#                                                                              #
def read_parameters(file_path):
    parameters = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 2):
            parameter = lines[i].strip()
            value = lines[i + 1].strip()
            parameters[parameter] = int(value) if value.isdigit() or (value[0] == '-' and value[1:].isdigit()) else value

    return parameters

def read_param_file(file_path):
    param_array = []

    with open(file_path, 'r') as file:
        for line in file:
            param_array.append(int(line.strip()))

    return param_array
#                                                                              #
#                                                                              #
################################################################################

def expected_value(action, state, Value, MDP:mf.generator.MDP_Grid):
    return sum([prob*Value[state_1] for (prob, state_1) in MDP.Transition(state, action)])

def benchmark(Grid_World:mf.generator.MDP_Grid, metric="value", n_run = 1000, eps = 1e-2):
    """Benchmark function for MDP methods."""      

    if metric == "value":
        VI = mf.search.Value_Iteration(Grid_World)
        t1 = time()
        for _ in range(n_run):
            VI.value_iteration(eps=eps)
        t2 = time()
        return (t2-t1) / n_run * 1000

    else:
        PI = mf.search.Policy_iteration(Grid_World)
        t1 = time()
        for _ in range(n_run):
            PI.policy_iteration()
        t2 = time()
        return (t2-t1) / n_run * 1000
    

def epoch(idx:int, size:int, param):
    """Benchmark for each maze.
    
    Inputs:
        - idx: int, the index of maze.txt
        - size: int, the size of maze.
        - param: the param of this maze.
    Output:
        - contents: The results store in benchmark.dat file.
    
    """

    maze_path = f"{param['location']}/mazes/{param['size']}/Maze{idx}.txt"
    print(maze_path)  

    Grid_World = mf.generator.load_maze(maze_path)

    Explorer = mf.search.Maze(Grid_World)

    t0 = time()
    Explorer.solve(mf.frontier.StackFrontier()) # DFS
    t1 = time()
    Explorer.solve(mf.frontier.QueueFrontier()) # BFS
    t2 = time()
    Explorer.solve(mf.frontier.AStar(Explorer.start, Explorer.goals)) # A Star
    t3 = time()
    Explorer.solve(mf.frontier.RandomFrontier()) # Baseline
    t4 = time()

    main_reward = - 0.04
    goal_rewards = [10.00] * len(Explorer.goals) + [-10.00]

    # MDP Grids with gamma 0.05, 0.5, 0.95
    RewardWorld = mf.generator.Generator2D.MDP_reward_grid(
        grid=Grid_World, 
        goals=Explorer.goals + [Explorer.start],
        main_reward=main_reward, 
        goal_rewards=goal_rewards
    )

    Grid_World_05 = mf.generator.MDP_Grid(
        grid=RewardWorld,
        goals=Explorer.goals + [Explorer.start],
        start=Explorer.start, 
        gamma=0.5
    )

    Grid_World_095 = mf.generator.MDP_Grid(
        grid=RewardWorld,
        goals=Explorer.goals + [Explorer.start],
        start=Explorer.start, 
        gamma=0.95
    )
    
    Grid_World_005 = mf.generator.MDP_Grid(
        grid=RewardWorld,
        goals=Explorer.goals + [Explorer.start],
        start=Explorer.start, 
        gamma=0.05
    )


    marks = {}
    n_run = 1

    # MDP Iterations
    Grid_World_list = [Grid_World_005, Grid_World_05, Grid_World_095]
    for metric in ["value", "policy"]:
        marks[metric] = [benchmark(GW, metric=metric, n_run=n_run, eps=1e-3) for GW in Grid_World_list]
    

    contents = f"{size} {idx} {1000*(t1-t0)} {1000*(t2-t1)} {1000*(t3-t2)} {1000*(t4-t3)} {marks['value'][0]} {marks['value'][1]} {marks['value'][2]} {marks['policy'][0]} {marks['policy'][1]} {marks['policy'][2]}\n"
    
    return contents


def evaluation(size:int, file):
    """Evaluation with parallelization"""

    file_path = f'params/param{size}'
    param = read_parameters(file_path)
    for i in param.keys():
        print(f"{i}: {param[i]}")
    print()
    
    results = Parallel(n_jobs=-1)(delayed(epoch)(idx, size, param) for idx in range(param['number']))
    for result in results:
        file.write(result)
    
    return 0


def main():
    """Main function of benchmark"""

    list_size = read_param_file("param")
    with open("benchmark.dat",'w') as file:
        file.write("size index DFS BFS AStar Baseline VI0.05 VI0.5 VI0.95 PI0.05 PI0.5 PI0.95\n")
        for size in list_size:
            evaluation(size, file)


if __name__ == "__main__":
    main()