from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import time
import requests
import io
import zipfile
import numpy as np
import shutil
import sys
import gzip

context = SparkContext()
context.addPyFile('/var/scratch/ddps2202/spark/jars/graphframes-0.8.2-spark3.2-s_2.12.jar')

# local[n] defines the number of partitions. Ideally, ``it should be the number of CPU cores you have."" [*] selects maximum
spark = SparkSession(context).builder.master("local[*]").appName('Sparktest').getOrCreate()

from graphframes import *

# Create edgelist
def getEdgelist (filename, spark, sep, headerValue, schema) :
  edges = spark.read.csv(filename, schema=schema, sep=sep, header=headerValue)
  return edges

# Create list of nodes
def getNodes (filename, spark, sep, headerValue, schema) :
  nodes = spark.read.csv(filename, schema=schema, sep = sep, header=headerValue)

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

if (sys.argv[2] == "crocodile") :
  # Get wikipedia dataset
  r = requests.get("https://snap.stanford.edu/data/wikipedia.zip")
  z = zipfile.ZipFile(io.BytesIO(r.content))
  z.extractall("./")

  schema = StructType([ \
      StructField("src",StringType(),True), \
      StructField("dst",StringType(),True), \
    ])
  edgelist = getEdgelist("./wikipedia/crocodile/musae_crocodile_edges.csv", spark, ',', True, schema)
  schema = StructType([ \
    StructField("id",StringType(),True), \
    StructField("temp",StringType(),True), \
  ])
  nodelist = getNodes("./wikipedia/crocodile/musae_crocodile_target.csv", spark, ',', True, schema)
  filename = "musae_crocodile"
elif (sys.argv[2] == "soc-Epinions1") :
  # Get soc-epinions dataset
  r = requests.get("https://snap.stanford.edu/data/soc-Epinions1.txt.gz")
  open('soc-Epinions1.txt.gz', 'wb').write(r.content)
  with gzip.open('soc-Epinions1.txt.gz', 'rb') as f_in:
      with open('soc-Epinions1.txt', 'wb') as f_out:
          shutil.copyfileobj(f_in, f_out)
  with open('./soc-Epinions1.txt') as f:
      lines = f.readlines()
  lines = lines[4:] # Remove first 4 lines of txt file
  f = open("./soc-Epinions1.txt", "w")
  f.writelines(lines)
  f.close()
  schema = StructType([ \
    StructField("src",StringType(),True), \
    StructField("dst",StringType(),True), \
  ])
  edgelist = getEdgelist("./soc-Epinions1.txt", spark, '\t', False, schema)
  schema = StructType([ \
      StructField("id",StringType(),True), \
  ])
  nodelist = getNodes("./soc-Epinions1_nodes.txt", spark, '\t', False, schema)
  filename = "soc-Epinions1"

g = GraphFrame(nodelist, edgelist)
times = repetition_experiment(g, 10)
nodeCount = sys.argv[1]
np.savetxt(f'/var/scratch/ddps2202/DDPS_Assignment_1/Fault_tolerance_{filename}_{nodeCount}.npy', np.array(times))