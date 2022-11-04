import numpy as np
import matplotlib.pyplot as plt

def plot_repetition_experiment (filename, times) :
  x = range(1,11)
  times_labels = [round(num, 1) for num in times]
  fig, ax = plt.subplots()
  fig = plt.bar(x, times)

  for i in range(len(x)):
    plt.text(i+1, times[i], times_labels[i], ha = 'center', va = 'bottom')
  plt.xticks(x)
  plt.xlabel("Repetition")
  plt.ylabel("Running time (seconds)")
  plt.ylim([0, max(times)*1.3])
  average = sum(times)/len(times)
  average = round(average, 1)
  std = round(np.std(times),1)
  props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
  plt.text(0.05, 0.95, f"Mean ~ {average}s\nStandard deviation ~ {std}s ", transform=ax.transAxes, fontsize=14,
          verticalalignment='top', bbox=props)
  plt.title("Spark PageRank performance (10 iterations)") # Rounded down to 1 decimal
  fig = plt.gcf()
  fig.set_size_inches(11, 5)
  plt.show()
  fig.savefig(f'png_files/{filename}.png')

filename = "npy_files/musae_crocodile_8.npy"
figname = filename.split(".")[0].split("/")[1]
times = np.loadtxt(filename)
plot_repetition_experiment(figname,times)