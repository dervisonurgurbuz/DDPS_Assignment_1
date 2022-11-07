import numpy as np
import matplotlib.pyplot as plt
import os

# # ########################### Hadoop 75k node network ################################# 
def plot_repetition_experiment (filename, times) :
  x = range(1,len(times)+1)
  times_labels = [round(num, 2) for num in times]
  fig, ax = plt.subplots()
  fig = plt.bar(x, times)

  for i in range(len(x)):
    plt.text(i+1, times[i], times_labels[i], ha = 'center', va = 'bottom')
  plt.xticks(x)
  plt.xlabel("Nodes")
  plt.ylabel("Running time (seconds)")
  plt.ylim([0, max(times)*1.3])
  average = sum(times)/len(times)
  average = round(average, 2)
  std = round(np.std(times),2)
  props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
  plt.text(0.05, 0.95, f"Mean ~ {average}s\nStandard deviation ~ {std}s ", transform=ax.transAxes, fontsize=14,
          verticalalignment='top', bbox=props)
  plt.title("Hadoop PageRank performance (10 iterations) - 75k nodes network") # Rounded down to 1 decimal
  fig = plt.gcf()
  fig.set_size_inches(11, 5)
  fig.savefig(f'png_files/{filename}.png')

directory = 'hadoop_results'
times = [None]*(len(os.listdir(directory))-1)
for filename in os.listdir(directory):
    if (filename == ".gitkeep") :
      continue
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        with open(f) as g:
          lines = float(g.readlines()[0])
          iteration = int(filename.split('.')[0].split('_')[-1])
          times[iteration-1] = lines
plot_repetition_experiment("hadoop",times)
# ###############################################################################

############################### SPARK 75k node network ###############################
def plot_repetition_experiment (filename, times) :
  x = range(1,len(times)+1)
  times_labels = [round(num, 2) for num in times]
  fig, ax = plt.subplots()
  fig = plt.bar(x, times)

  for i in range(len(x)):
    plt.text(i+1, times[i], times_labels[i], ha = 'center', va = 'bottom')
  plt.xticks(x)
  plt.xlabel("Nodes")
  plt.ylabel("Running time (seconds)")
  plt.ylim([0, max(times)*1.3])
  average = sum(times)/len(times)
  average = round(average, 2)
  std = round(np.std(times),2)
  props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
  plt.text(0.05, 0.95, f"Mean ~ {average}s\nStandard deviation ~ {std}s ", transform=ax.transAxes, fontsize=14,
          verticalalignment='top', bbox=props)
  plt.title("Spark PageRank performance (10 iterations) - 75k nodes network") # Rounded down to 1 decimal
  fig = plt.gcf()
  fig.set_size_inches(11, 5)
  fig.savefig(f'png_files/{filename}.png')

directory = 'soc-Epinions_spark_results'
times = [None]*(len(os.listdir(directory))-1)
for filename in os.listdir(directory):
    if (filename == ".gitkeep") :
      continue
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        with open(f) as g:
          lines = float(g.readlines()[0])
          iteration = int(filename.split('.')[0].split('_')[-1])
          times[iteration-1] = lines
plot_repetition_experiment("spark",times)
############################################################################################