print("hi")
import pyspark
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import Row
import pandas as pd
from datetime import datetime, date
from pyspark.sql.types import *
import time
import gzip
import requests
import shutil
import io
import zipfile
import numpy as np
# import matplotlib.pyplot as plt

# r = requests.get("https://snap.stanford.edu/data/wikipedia.zip")
# z = zipfile.ZipFile(io.BytesIO(r.content))
# z.extractall("./")

# context = SparkContext()
# context.addPyFile('/home/jonathan/miniconda3/lib/python3.9/site-packages/pyspark/jars/graphframes-0.8.2-spark3.2-s_2.12.jar')

# # local[n] defines the number of partitions. Ideally, ``it should be the number of CPU cores you have."" [*] selects maximum
# spark = SparkSession(context).builder.master("local[*]").appName('Sparktest').getOrCreate()

# from graphframes import *

# # Create edgelist
# def getEdgelist (filename, spark, sep = ',') :
#   schema = StructType([ \
#       StructField("src",StringType(),True), \
#       StructField("dst",StringType(),True), \
#     ])
#   edges = spark.read.csv(filename, schema=schema, sep=sep)
#   return edges

# # Create list of nodes
# def getNodes (filename, spark, sep = ',') :
#   schema = StructType([ \
#       StructField("id",StringType(),True), \
#       StructField("temp",StringType(),True), \
#     ])
#   nodes = spark.read.csv(filename, schema=schema, sep = sep)

#   # Only keep column with node indices
#   nodes = nodes.drop("temp")
#   return nodes

# # Run PageRank algorithm, record time, and show results.
# def repetition_experiment (graphframe, repetitions) :
#   times = []
#   for i in range (repetitions) :
#     start = time.perf_counter()
#     results = graphframe.pageRank(resetProbability=0.01, maxIter=10)
#     end = time.perf_counter()
#     times.append(end-start)
#   return times

# def plot_repetition_experiment (times) :
#   x = range(1,11)
#   times_labels = [round(num, 1) for num in times]
#   fig, ax = plt.subplots()
#   fig = plt.bar(x, times)

#   for i in range(len(x)):
#     plt.text(i+1, times[i], times_labels[i], ha = 'center', va = 'bottom')
#   plt.xticks(x)
#   plt.xlabel("Repetition")
#   plt.ylabel("Running time (seconds)")
#   plt.ylim([0, max(times)*1.3])
#   average = sum(times)/len(times)
#   average = round(average, 1)
#   std = round(np.std(times),1)
#   props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
#   plt.text(0.05, 0.95, f"Mean ~ {average}s\nStandard deviation ~ {std}s ", transform=ax.transAxes, fontsize=14,
#           verticalalignment='top', bbox=props)
#   plt.title("Spark PageRank performance (10 iterations)") # Rounded down to 1 decimal
#   fig = plt.gcf()
#   fig.set_size_inches(11, 5)
#   plt.show()
#   fig.savefig('repetition.png')

# edgelist = getEdgelist("./wikipedia/crocodile/musae_crocodile_edges.csv", spark)
# nodelist = getNodes("./wikipedia/crocodile/musae_crocodile_target.csv", spark)
# g = GraphFrame(nodelist, edgelist)
# times = repetition_experiment(g, 10)
# plot_repetition_experiment(times)