################################################################################
"""Imports and stype settings"""
from mazepy import mazeflow as mf
from time import time

import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt

# Set the font to Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'
mpl.rcParams['font.size'] = 10
plt.rcParams['font.weight'] = 'black'
mpl.rcParams['text.usetex'] = True

from main import read_param_file
from main import read_parameters
################################################################################


df = pd.read_csv("benchmark.dat", delimiter=" ")

algs = list(df.columns)[2:]
sizes = read_param_file("param")
gammas = [float(gamma[2:]) for gamma in (algs[-3:])]


means = {}
stdvs = {}
for alg in algs:
    for i in range(3):
################################################################################
#                print for store as table in latex format                      #
#
#       if i == 0:
#           print("$\mu$ ", end="")
#       elif i == 1:
#           print("$t_{0.5}$ ", end="")
#       elif i == 2:
#           print("$\sigma$ ", end="")
################################################################################
                    
        list_mean = []
        list_stdv = []
        list_median = []
        for size in sizes:
            temp = np.array(df[df['size'] == size][alg])
    
            list_mean.append(np.mean(temp))
            list_stdv.append(np.std(temp))


################################################################################
#                 print for store as table in latex format                     #
#            
#             if i == 0:
#                 print(" & {:6.2f}".format(np.mean(temp)), end="")
#             elif i == 1:
#                 print(" & {:6.2f}".format(np.std(temp)), end="")
#             elif i == 2:
#                 print(" & {:6.2f}".format(np.median(temp)), end="")
# 
#         print(" \\\\")
#     print()
################################################################################
            
    means[alg] = list_mean
    stdvs[alg] = list_stdv


mean_stdv = {}
for alg in algs:
    list_mean = []
    list_stdv = []
    list_median = []

    for size in sizes:
        temp = np.array(df[df['size'] == size][alg])

        list_mean.append(np.mean(temp))
        list_stdv.append(np.std(temp))
        list_median.append(np.median(temp))
        
    mean_stdv[alg] = {"mean": list_mean, "stdv": list_stdv, "mid": list_median}



################################################################################
#                                                                              # 
#                                   Figure 1                                   #
#                                                                              # 
################################################################################


fig, ax = plt.subplots(1, 2,figsize=(10,4.5), dpi=300)
colors = ["black", "brown", "red", "blue", (0.2, 0.8, 0.6), (0.2, 0.4, 0.8), (0.8, 0.4, 0.6)]
fig.suptitle('Time (ms) spend Comparisons of the Mean $\mu$, Standard Deviation $\sigma$ and Median $t_{0.5}$ for Different Sizes $s$')
fig.text(0.5, 0.04, 'Size of maze (log)', ha='center')

temp = algs[3:]
for idx, alg in enumerate(temp):
    if alg == "Baseline":
        linestyle = "-."
    else:
        linestyle = "-"
    ax[0].errorbar(sizes, mean_stdv[alg]["mean"], yerr=mean_stdv[alg]["stdv"], color=colors[idx], marker='s', markersize=3, label = alg, linestyle=linestyle, linewidth=1)
    ax[0].scatter(sizes, mean_stdv[alg]["mid"], color=colors[idx], marker='s', s=1)


ax[0].set_ylabel("Time (ms) of Solving Mazes (log)")
ax[0].set_xscale('log')
ax[0].set_yscale('log')

ax[0].legend(loc = "lower right")

ax[0].set_xticks([5, 10,20, 50,100,200, 500], ["5", "10", "20", "50", "100","200", "500"])
ax[0].grid()


temp = algs[:4]
temp.reverse()
for idx, alg in enumerate(temp):
    if alg == "Baseline":
        linestyle = "-."
    else:
        linestyle = "-"
    ax[1].errorbar(sizes, mean_stdv[alg]["mean"] , yerr=mean_stdv[alg]["stdv"], label=alg, marker='s', markersize=3, color=colors[idx], linestyle=linestyle)
    ax[1].scatter(sizes, mean_stdv[alg]["mid"], color=colors[idx], marker='s', s=1)
    
ax[1].set_xscale('log')
ax[1].set_yscale('log')

ax[1].legend(loc='lower right')
ax[1].grid()

ax[1].set_xticks([5, 10,20, 50,100,200, 500], ["5", "10", "20", "50", "100","200", "500"])

plt.savefig("outputs/figures/report/figure01.png")
# plt.show()



################################################################################
#                                                                              # 
#                                   Figure 3                                   #
#                                                                              # 
################################################################################
MDPs = [algs[0]] + algs[-6:]
fig, ax = plt.subplots(1, 1,figsize=(4.5,4.5), dpi=300)
colors = ["black", "brown", "red", "blue", (0.2, 0.8, 0.6), (0.2, 0.4, 0.8), (0.8, 0.4, 0.6)]
fig.suptitle('Comparisons of the Standard Deviation $\sigma$ for Different Sizes $s$')
fig.text(0.5, 0.04, 'Size of maze ($log$)', ha='center')

temp = MDPs
for idx, alg in enumerate(temp):
    if alg == "Baseline":
        linestyle = "-."
    else:
        linestyle = "-"

    ax.plot(sizes, mean_stdv[alg]["stdv"], label=alg, marker='s', markersize=3, color=colors[idx], linestyle=linestyle)
    

ax.set_ylabel("Variance of Time (ms) of Solving Mazes ($log$)")
ax.set_xscale('log')
ax.set_yscale('log')

ax.legend(loc = "lower right")

ax.set_xticks([5, 10,20, 50,100,200, 500], ["5", "10", "20", "50", "100","200", "500"])
ax.grid()

plt.savefig("outputs/figures/report/figure03.png")
# plt.show()



def least_squares_estimation(xlist, ylist):
    """ Least Square Estimation """
    n = len(xlist)
    x = np.array(xlist)
    y = np.array(ylist)
    X = np.vstack([np.ones_like(x), x]).T
    beta_hat = beta_0, beta_1 = np.linalg.lstsq(X, y, rcond=None)[0]
    
    ltt = np.sum(np.array(tlist)*np.array(tlist)) - sum(tlist)**2 / n
    lss = np.sum(np.array(slist)*np.array(slist)) - sum(slist)**2 / n
    lst = np.sum(np.array(slist)*np.array(tlist)) - sum(slist)*sum(tlist) / n
    
    Se = ltt - beta_1**2 * lss

    sig_hat = np.sqrt(Se / (n-2))
    
    t = beta_1 / (sig_hat / np.sqrt(lss))
    
    r = lst / (np.sqrt(lss)*np.sqrt(ltt))
    return beta_hat, r

################################################################################
#                                                                              # 
#                                   Table 1                                    #
#                                                                              # 
################################################################################
print("#"*80)
temp = "Regression\n"
print("#"+" "*(39-len(temp)//2)+temp)

n = len(sizes)
beta = {}
print("& beta 0  & beta 1 & r \\\\")
for alg in algs:
    tlist = np.log10(mean_stdv[alg]['mean'])
    slist = np.log10(sizes)
    [beta_0, beta_1], r = least_squares_estimation(slist, tlist)
    beta[alg] = [beta_0, beta_1]

    print("{:8} & {:6.4f} & {:6.4f} & {:6.4f} \\\\".format(alg, beta_0, beta_1, r))

print("#"*80)

################################################################################
#                                                                              # 
#                          Two-Way Analysis of Variance                        #
#                                                                              # 
################################################################################

temp = "Two-Way Analysis of Variance\n"
print("#"+" "*(39-len(temp)//2)+temp)

algs = [algs[3]] + algs[:3] + algs[4:]
n = len(sizes)
time_array = []
for alg in algs:
    time_array.append(means[alg])
time_array = np.array(time_array)

data = np.log10(time_array)
mean_total = np.mean(data)
sst = np.sum((data - mean_total) ** 2)

# SSR
mean_by_factor = np.mean(data, axis=0)
ssr = np.sum(len(data) * (mean_by_factor - mean_total) ** 2)

# SSC
mean_by_level = np.mean(data, axis=1)
ssc = np.sum(len(data[0]) * (mean_by_level - mean_total) ** 2)
sse = sst - ssr - ssc

msr, msc, mse = ssr / 9, ssc / 19, sse / 171

fr = (ssr / 9) / (sse / 171)
fc = (ssc / 19) / (sse / 171)


from scipy.stats import f
alpha = 2e-16

for df1 in [9, 19]:
    # df1 = 19
    df2 = 19*9
    f_crit = f.ppf(1 - alpha/2, df1, df2)

    print(f"F crit F({df1}, {df2}):", f_crit)

print("#"*80)

################################################################################
#                                                                              # 
#                            Average of Final Paths                            #
#                                                                              # 
################################################################################
temp = "Avg. of Final Path\n"
print("#"+" "*(39-len(temp)//2)+temp)

sizes = read_param_file("param")
size = 10
ID = idx = 10 

file_path = f'params/param{size}'
param = read_parameters(file_path)
maze_path = f"{param['location']}/mazes/{param['size']}/Maze{idx}.txt"

Grid_World = mf.generator.load_maze(maze_path)

Explorer = mf.search.Maze(Grid_World)


sizes = read_param_file("param")

list_explored = {"Baseline":[], "A*":[] , "DFS":[], "BFS":[]}
list_path_len = {"Baseline":[], "A*":[] , "DFS":[], "BFS":[]}

list_alg = ["Baseline","A*" , "DFS", "BFS"]
print("size & Baseline &  A* & DFS & BFS")

for ids, size in enumerate(sizes):
    file_path = f'params/param{size}'
    param = read_parameters(file_path)
    maze_path = f"{param['location']}/mazes/{param['size']}/Maze{ID}.txt"

    Grid_World = mf.generator.load_maze(maze_path)

    Explorer = mf.search.Maze(Grid_World)

    list_frontier = [
        mf.frontier.RandomFrontier(), 
        mf.frontier.AStar(start=Explorer.start, goal=Explorer.goals), 
        mf.frontier.StackFrontier(), 
        mf.frontier.QueueFrontier()
    ]
    
    print(f"{size}", end=" ")
    for idx, frontier in enumerate(list_frontier):
        Explorer.solve(list_frontier[idx])
        
        
        if ids % 10 == 0:
            filename = f"outputs/figures/report/{size}_{list_alg[idx]}.png"
            Explorer.plot(filename=filename, show_solution=True, show_explored=True)
        
        list_explored[list_alg[idx]].append(Explorer.num_explored)
        
        
        path_len = []
        for goal in Explorer.goals:
            path_len.append(len(Explorer.solution[goal][1]))
            
        path_len = sum(path_len) / len(Explorer.goals)
        list_path_len[list_alg[idx]].append(path_len)
        
        print("& {}".format(path_len), end=" ")
    print("\\\\")


################################################################################
#                                                                              # 
#                                   Figure 2                                   #
#                                                                              # 
################################################################################
fig = plt.figure(figsize=(4.5, 3.5), dpi = 300)

colors = ["black", "brown", "red", "blue", (0.2, 0.8, 0.6), (0.2, 0.4, 0.8), (0.8, 0.4, 0.6)]

for idx, alg in enumerate(list_alg):
    
    if alg == "Baseline":
        linestyle = "-."
    else:
        linestyle = "-"
        
    plt.plot(sizes, list_path_len[alg], linestyle=linestyle, marker='s', markersize=3, color=colors[idx], label = alg, alpha=0.6)
plt.yscale("log")
plt.xscale("log")
plt.grid()
plt.legend(loc='lower right')
plt.xticks([5, 10,20, 50,100,200, 500], ["5", "10", "20", "50", "100","200", "500"])
plt.ylabel("Path Length ($log$)")
plt.xlabel("Size of maze ($log$)")
plt.title("Comparisons of path length for different sizes ($s$)")

plt.savefig("outputs/figures/report/figure02.png")
# plt.show()