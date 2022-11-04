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
  z.extractall("/var/scratch/ddps2202/DDPS_Assignment_1/")

  schema = StructType([ \
      StructField("src",StringType(),True), \
      StructField("dst",StringType(),True), \
    ])
  edgelist = getEdgelist("/var/scratch/ddps2202/DDPS_Assignment_1/wikipedia/crocodile/musae_crocodile_edges.csv", spark, ',', True, schema)
  schema = StructType([ \
    StructField("id",StringType(),True), \
    StructField("temp",StringType(),True), \
  ])
  nodelist = getNodes("/var/scratch/ddps2202/DDPS_Assignment_1/wikipedia/crocodile/musae_crocodile_target.csv", spark, ',', True, schema)

elif (sys.argv[2] == "soc-Epinions1") :
  # Get soc-epinions dataset
  r = requests.get("https://snap.stanford.edu/data/soc-Epinions1.txt.gz")
  open('/var/scratch/ddps2202/DDPS_Assignment_1/soc-Epinions1.txt.gz', 'wb').write(r.content)
  with gzip.open('/var/scratch/ddps2202/DDPS_Assignment_1/soc-Epinions1.txt.gz', 'rb') as f_in:
      with open('/var/scratch/ddps2202/DDPS_Assignment_1/soc-Epinions1.txt', 'wb') as f_out:
          shutil.copyfileobj(f_in, f_out)
  with open('/var/scratch/ddps2202/DDPS_Assignment_1/soc-Epinions1.txt') as f:
      lines = f.readlines()
  lines = lines[4:] # Remove first 4 lines of txt file
  f = open("/var/scratch/ddps2202/DDPS_Assignment_1/soc-Epinions1.txt", "w")
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
  f = open("/var/scratch/ddps2202/DDPS_Assignment_1/soc-Epinions1_nodes.txt", "w")
  f.writelines(nodes)
  f.close()

  schema = StructType([ \
    StructField("src",StringType(),True), \
    StructField("dst",StringType(),True), \
  ])
  edgelist = getEdgelist("/var/scratch/ddps2202/DDPS_Assignment_1/soc-Epinions1.txt", spark, '\t', False, schema)
  schema = StructType([ \
      StructField("id",StringType(),True), \
  ])
  nodelist = getNodes("/var/scratch/ddps2202/DDPS_Assignment_1/soc-Epinions1_nodes.txt", spark, '\t', False, schema)

elif (sys.argv[2] == "wiki-topcats") :
  r = requests.get("https://snap.stanford.edu/data/wiki-topcats.txt.gz")
  open('/var/scratch/ddps2202/DDPS_Assignment_1/wiki-topcats.txt.gz', 'wb').write(r.content)
  with gzip.open('/var/scratch/ddps2202/DDPS_Assignment_1/wiki-topcats.txt.gz', 'rb') as f_in:
      with open('/var/scratch/ddps2202/DDPS_Assignment_1/wiki-topcats.txt', 'wb') as f_out:
          shutil.copyfileobj(f_in, f_out)

  # Create list of nodes from edgelist
  with open('/var/scratch/ddps2202/DDPS_Assignment_1/wiki-topcats.txt') as f:
    lines = f.readlines()
  nodes = set()
  for i in lines :
    node1, node2 = i.split(' ')
    if not ('\n' in node1) :
      node1 = node1 + '\n'
    if not ('\n' in node2) :
      node2 = node2 + '\n'
    nodes.add(node1)
    nodes.add(node2)
  f = open('/var/scratch/ddps2202/DDPS_Assignment_1/wiki-topcats_nodes.txt', "w")
  f.writelines(nodes)
  f.close()

  schema = StructType([ \
    StructField("src",StringType(),True), \
    StructField("dst",StringType(),True), \
  ])
  edgelist = getEdgelist("/var/scratch/ddps2202/DDPS_Assignment_1/wiki-topcats.txt", spark, ' ', False, schema)
  schema = StructType([ \
    StructField("id",StringType(),True), \
  ])
  nodelist = getNodes("/var/scratch/ddps2202/DDPS_Assignment_1/wiki-topcats_nodes.txt", spark, ' ', False, schema)

else :
  exit()

g = GraphFrame(nodelist, edgelist)
times = repetition_experiment(g, int(sys.argv[3]))
nodeCount = sys.argv[1]
np.savetxt(f'/var/scratch/ddps2202/DDPS_Assignment_1/npy_files/{sys.argv[2]}_{nodeCount}.npy', np.array(times))
