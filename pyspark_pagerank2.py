from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import time
import requests
import shutil
import gzip
import numpy as np

r = requests.get("https://snap.stanford.edu/data/soc-Epinions1.txt.gz")
open('soc-Epinions1.txt.gz', 'wb').write(r.content)
with gzip.open('soc-Epinions1.txt.gz', 'rb') as f_in:
    with open('soc-Epinions1.txt', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

# Remove first 4 lines of txt file
with open('./soc-Epinions1.txt') as f:
    lines = f.readlines()

lines = lines[4:]
f = open("./soc-Epinions1.txt", "w")
f.writelines(lines)
f.close()

# Create list of nodes
nodes = set()
for i in lines :
  node1, node2 = i.split('\t')
  if not ('\n' in node1) :
    node1 = node1 + '\n'
  if not ('\n' in node2) :
    node2 = node2 + '\n'
  nodes.add(node1)
  nodes.add(node2)
f = open("./soc-Epinions1_nodes.txt", "w")
f.writelines(nodes)
f.close()

context = SparkContext()
context.addPyFile('/var/scratch/ddps2202/spark/jars/graphframes-0.8.2-spark3.2-s_2.12.jar')

# local[n] defines the number of partitions. Ideally, ``it should be the number of CPU cores you have."" [*] selects maximum
spark = SparkSession(context).builder.master("local[*]").appName('Sparktest').getOrCreate()

from graphframes import *

schema = StructType([ \
    StructField("src",StringType(),True), \
    StructField("dst",StringType(),True), \
  ])

edgelist = spark.read.csv("./soc-Epinions1.txt", sep ='\t', header=False, schema=schema)

schema = StructType([ \
      StructField("id",StringType(),True), \
    ])
nodelist = spark.read.csv("./soc-Epinions1_nodes.txt", sep ='\t', header=False, schema=schema)

# Run PageRank algorithm, record time, and show results.
def repetition_experiment (graphframe, repetitions) :
  times = []
  for i in range (repetitions) :
    start = time.perf_counter()
    results = graphframe.pageRank(resetProbability=0.01, maxIter=10)
    end = time.perf_counter()
    times.append(end-start)
  return times

g = GraphFrame(nodelist, edgelist)
times = repetition_experiment(g, 10)
np.savetxt('/var/scratch/ddps2202/DDPS_Assignment_1/soc-epinions.npy', np.array(times))
