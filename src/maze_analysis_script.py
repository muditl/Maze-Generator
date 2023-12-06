import time
import matplotlib.pyplot as plt
import numpy as np

from src.Analysis import Analysis
from src.Generator import Generator

generator = Generator(1, 1)
algos = [generator.binary_tree, generator.sidewinder, generator.aldous_broder, generator.aldous_broder,
         generator.hunt_and_kill, generator.recursive_backtracker]

algorithms = ["Binary Tree", "Sidewinder", "Aldous-Broder", "Wilson's", "Hunt and Kill", "Recursive Backtracker"]

metrics = ["Dead Ends", "Total Branch Points", "Triple Branch Points", "Quadruple Branch Points", "Straights", "Turns",
           "Turn Straight Ratio", "Longest Path Length", "Longest Path Total Branches",
           "Longest Path Triple Branch Points", "Longest Path Quad Branch Points", "Longest Path Straights",
           "Longest Path Turns", "Longest Path Turn Straight Ratio", "Time to Generate"]
file_names = ["dead_ends", "branch", "tbp", "qbp", "str", "turn", "ratio", "lpl", "lptb", "lptbp", "lpqbp", "lps",
              "lpt", "lptsr", "time"]

start_size = 5
end_size = 100

analysis = np.zeros(shape=(len(algos), end_size - start_size, 16))

run = True
runs = 100
if run:
    for n in range(runs):
        for i in range(start_size, end_size):
            generator.resize_grid(i, i)
            for j, algo in enumerate(algos):
                gen_start_time = time.time()
                maze = algo()
                gen_end_time = time.time()

                analysis_array = np.array(Analysis(maze).get_metrics_array()) / runs
                analysis[j, i - start_size, 0:15] += analysis_array
                analysis[j, i - start_size, 15] += (gen_end_time - gen_start_time) / runs

        print("done with run " + str(n))

plots_dir = "../../analysis_plots/"
print("Done with analysis. Now plotting graphs")
for metric_idx in range(len(metrics)):
    plt.clf()
    for algo_idx in range(len(algos)):
        values_to_plot = analysis[algo_idx, :, metric_idx]
        # Generate x-axis values
        grid_sizes = np.arange(start_size, end_size)
        # Plot the graph
        plt.plot(grid_sizes, values_to_plot, label=algorithms[algo_idx])
    plt.xlabel('Grid Size')
    plt.ylabel(f'{metrics[metric_idx]}')
    plt.legend()
    plt.title(f'{metrics[metric_idx]}')
    plt.savefig(plots_dir + "cumulative/" + f'{file_names[metric_idx]}' + '.png')

for metric_idx in range(len(metrics)):
    for algo_idx in range(len(algos)):
        values_to_plot = analysis[algo_idx, :, metric_idx]
        # Generate x-axis values
        grid_sizes = np.arange(start_size, end_size)
        # Plot the graph
        plt.clf()
        plt.plot(grid_sizes, values_to_plot)
        plt.xlabel('Grid Size')
        plt.ylabel(f'{metrics[metric_idx]}')
        plt.title(f'{algorithms[algo_idx]} - {metrics[metric_idx]}')
        plt.savefig(plots_dir + "individual/" + f'{algorithms[algo_idx]}_{metrics[metric_idx]}' + '.png')
