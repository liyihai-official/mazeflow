# Search and MDP iteration Algorithms
This program including three parts majorly: Generator, Benchmark, Visualization.

## Module Requirements: 
General requirement:
- mazeflow, I coded a package that include all necessary classes and functions for this program.
- numpy, array operations
```
Generator.py
```
- time, markring time stamps.
- joblib, parallelizing for making fully use of all threads.
- noise, generating relative continues random 2d-array.
- argparse, for analysis command line arguments.
- os, for system operations.

```
visualization.py
```
- pandas: loading and doing operations on datasets.
- matplotlib, plotting figures

## ```mazeflow```
Installation:
```
pip install mazeflow
```

```mazeflow``` is a python library which I coded for this assignment,
the older version is available on python official open source pypi 
<a herf="https://pypi.org/project/mazeflow/" >website</a>, and the 
file tree is
```
mazeflow
├── LICENSE.md
├── README.md
├── mazeflow
│   ├── __init__.py
│   ├── frontier.py
│   ├── generator.py
│   ├── lib
│   │   ├── __init__.py
│   │   └── common.py
│   └── search.py
└── setup.py

3 directories, 9 files
```



## Generate Solvable Mazes (```generate_mazes.sh```)
```
source generate_mazes.sh
```
### Sample Maze ```demo.py```
![](/outputs_demo/figures/Maze0.png)

Calling program ```demo.py```, the usage if 
```
usage: demo.py [-h] -s SIZE [-t THREAD] -n NUMBER [-f FILE] [-l LOCATION]

Process information of maze.

optional arguments:
  -h, --help            show this help message and exit

General infos:
  -s SIZE, --size SIZE  size of the Square maze. (default: 10)
  -t THREAD, --thread THREAD
                        number of thread for generate mazes. (default: -1)
  -n NUMBER, --number NUMBER
                        the number of generated maze that has solution. (default: 1)

Save infos:
  -f FILE, --file FILE  file name prefix (default: '10')
  -l LOCATION, --location LOCATION
                        location of outputs (default: 'outputs')
```


### Parameters
```generate_mazes.sh``` will store the parameters into file ```param``` and 
make a copy of old ```param``` file into ```param.save```.
By default, it will generate $50$ mazes for each size and the size list is
```
sizes = (5 10 15 20 25 30 35 40 45 50 55 60 70 80 100 150 200 250 300 500)
```

## Benchmark (```main.py```)
``` 
python main.py
```
Program ```main.py``` includes all necessary tests for the report,
the benchmark of time on all algorithms. 
The outputs will be stored in the file ```benchmark.dat``` as a chart for 
all results with respect to size $s$ and algorithm.

## Visualization (```visualization.py```)
```
python visualization.py
```
This is the program that includes all tables and figures required in report.

![图示](/outputs/figures/report/figure01.png)