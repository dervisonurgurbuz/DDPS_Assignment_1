from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import time
import requests
import io
import zipfile
import numpy as np

r = requests.get("https://snap.stanford.edu/data/wikipedia.zip")
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall("./")

context = SparkContext()
context.addPyFile('/var/scratch/ddps2202/spark/jars/graphframes-0.8.2-spark3.2-s_2.12.jar')

# local[n] defines the number of partitions. Ideally, ``it should be the number of CPU cores you have."" [*] selects maximum
spark = SparkSession(context).builder.master("local[*]").appName('Sparktest').getOrCreate()

from graphframes import *

# Create edgelist
def getEdgelist (filename, spark, sep = ',') :
  schema = StructType([ \
      StructField("src",StringType(),True), \
      StructField("dst",StringType(),True), \
    ])
  edges = spark.read.csv(filename, schema=schema, sep=sep, header=True)
  return edges

# Create list of nodes
def getNodes (filename, spark, sep = ',') :
  schema = StructType([ \
      StructField("id",StringType(),True), \
      StructField("temp",StringType(),True), \
    ])
  nodes = spark.read.csv(filename, schema=schema, sep = sep, header=True)

  # Only keep column with node indices
  nodes = nodes.drop("temp")
  return nodes

# Run PageRank algorithm, record time, and show results.
def repetition_experiment (graphframe, repetitions) :
  times = []
  for i in range (repetitions) :
    start = time.perf_counter()
    results = graphframe.pageRank(resetProbability=0.01, maxIter=10)
    end = time.perf_counter()
    times.append(end-start)
  return times

edgelist = getEdgelist("./wikipedia/crocodile/musae_crocodile_edges.csv", spark)
nodelist = getNodes("./wikipedia/crocodile/musae_crocodile_target.csv", spark)
g = GraphFrame(nodelist, edgelist)
times = repetition_experiment(g, 10)
np.savetxt('/var/scratch/ddps2202/DDPS_Assignment_1/repetition_array.npy', np.array(times))