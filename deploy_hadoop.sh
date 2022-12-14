#!/bin/bash
# Run spark first before running this, so that datasets are set
set -e

if [[ $# -lt 1 ]] ; then
	echo ""
	echo "Run this from masternode (NOT front-end)"
	echo "usage: source deploy_hadoop.sh [nodes] [pagerank iterations]"
	echo "for example: source deploy_hadoop.sh node105,node106,node107 10"
	echo ""
	exit 1
fi

source export.sh

###################### UNCOMMENT AND RUN ONCE #################################################
# Download hadoop
# curl -L -o "/var/scratch/$USER/spark/jars/graphframes-0.8.2-spark3.2-s_2.12.jar" https://repos.spark-packages.org/graphframes/graphframes/0.8.2-spark3.2-s_2.12/graphframes-0.8.2-spark3.2-s_2.12.jar
# wget -O /var/scratch/$USER/hadoop-2.7.0.tar.gz https://archive.apache.org/dist/hadoop/common/hadoop-2.7.0/hadoop-2.7.0.tar.gz && \
# tar -zxf /var/scratch/$USER/hadoop-2.7.0.tar.gz -C /var/scratch/$USER && mv /var/scratch/$USER/hadoop-2.7.0 /var/scratch/$USER/hadoop
# rm /var/scratch/$USER/hadoop-2.7.0.tar.gz

# # Set environment variables
# cd /var/scratch/$USER/hadoop/etc/hadoop
# echo "export JAVA_HOME=/var/scratch/$USER/jdk-11.0.2" >> mapred-env.sh
# echo "export JAVA_HOME=/var/scratch/$USER/jdk-11.0.2" >> hadoop-env.sh
# echo "export JAVA_HOME=/var/scratch/$USER/jdk-11.0.2" >> yarn-env.sh
# cd /var/scratch/$USER/DDPS_Assignment_1

# # Create namenode and datanode directories
# mkdir /var/scratch/$USER/hadoop/dfs
# mkdir /var/scratch/$USER/hadoop/dfs/namenode
# mkdir /var/scratch/$USER/hadoop/dfs/datanode
# mkdir /var/scratch/$USER/hadoop/dfs/temp

# Download pagerank for hadoop implementation
# cd .. && git clone https://github.com/danielepantaleone/hadoop-pagerank.git || true && cd hadoop-pagerank

# # Inspiration: https://stackoverflow.com/questions/49951114/java-class-not-found-for-pagerank-algorithm-in-apache-hadoop
# # Compile pagerank code, then turn to jar file.
# javac -classpath ${HADOOP_CLASSPATH} -d ./ src/it/uniroma1/hadoop/pagerank/PageRank.java src/it/uniroma1/hadoop/pagerank/job1/PageRankJob1Mapper.java src/it/uniroma1/hadoop/pagerank/job1/PageRankJob1Reducer.java src/it/uniroma1/hadoop/pagerank/job2/PageRankJob2Mapper.java src/it/uniroma1/hadoop/pagerank/job2/PageRankJob2Reducer.java src/it/uniroma1/hadoop/pagerank/job3/PageRankJob3Mapper.java 
# jar -cf it/pagerank.jar it/
# cd ../DDPS_Assignment_1
#################################################################################################

echo "Deploying hadoop on ${1}"
nodes=${1}
IFS=',' read -ra node_list <<< "$nodes"; unset IFS
master=${node_list[0]}
worker=${node_list[@]:1}
echo "master is "$master
echo "worker is "$worker

# Copy configuration files to hadoop folder
# Originally, slaves only contains 'localhost'
cp /var/scratch/$USER/DDPS_Assignment_1/hadoop_configs/slaves /var/scratch/$USER/hadoop/etc/hadoop/slaves 
cp /var/scratch/$USER/DDPS_Assignment_1/hadoop_configs/core-site.xml /var/scratch/$USER/hadoop/etc/hadoop/core-site.xml
cp /var/scratch/$USER/DDPS_Assignment_1/hadoop_configs/hdfs-site.xml /var/scratch/$USER/hadoop/etc/hadoop/hdfs-site.xml
cp /var/scratch/$USER/DDPS_Assignment_1/hadoop_configs/yarn-site.xml /var/scratch/$USER/hadoop/etc/hadoop/yarn-site.xml
cp /var/scratch/$USER/DDPS_Assignment_1/hadoop_configs/mapred-site.xml /var/scratch/$USER/hadoop/etc/hadoop/mapred-site.xml

# Set config files based on master node and worker nodes
host="hdfs://${master}:9000"
xml_file="/var/scratch/$USER/hadoop/etc/hadoop/core-site.xml"
xmllint --shell ${xml_file} << EOF
cd /configuration/property[name='fs.defaultFS']/value
set ${host}
save
EOF
xml_file="/var/scratch/$USER/hadoop/etc/hadoop/yarn-site.xml"
xmllint --shell ${xml_file} << EOF
cd /configuration/property[name='yarn.resourcemanager.hostname']/value
set ${master}
save
EOF
xmllint --shell ${xml_file} << EOF
cd /configuration/property[name='yarn.resourcemanager.address']/value
set ${master}:8032
save
EOF
echo "$master" > /var/scratch/$USER/hadoop/etc/hadoop/slaves
for i in $worker 
do
	echo "$i" >> /var/scratch/$USER/hadoop/etc/hadoop/slaves
done

######################## UNCOMMENT AND RUN ONCE ################################################
# # Format namenode 
# hdfs namenode -format # Maybe format with clusterID (hdfs namenode -format -clusterID CID-887fb3d7-6840-45c2-8fea-eaa72b82b118)
#################################################################################################

# Start hadoop DFS daemons and yarn 
start-dfs.sh
start-yarn.sh

# Turn off safemode 
hdfs dfsadmin -safemode leave

# # Create input and output directories on hdfs
hadoop fs -mkdir -p /input
hadoop fs -mkdir -p /output

######################## UNCOMMENT AND RUN ONCE ################################################
# hadoop fs -put -f datasets/soc-Epinions1.txt /input
#################################################################################################

# # Run hadoop and pagerank, and track time.
start_time=$(date +%s.%N)
cd ..
hadoop jar hadoop-pagerank/it/pagerank.jar it.uniroma1.hadoop.pagerank.PageRank --input /input/soc-Epinions1.txt --output /output --count ${2}
end_time=$(date +%s.%N)
DIFF=$(echo "$end_time - $start_time" | bc)

# Stop daemons & yarn
stop-dfs.sh
stop-yarn.sh

# Print results
echo "Elapsed time for ${2} iteration(s): $DIFF seconds"
cd DDPS_Assignment_1
touch hadoop_results/pagerank_iterations_${2}_nodes_${#node_list[@]}.txt
echo $DIFF > hadoop_results/pagerank_iterations_${2}_nodes_${#node_list[@]}.txt