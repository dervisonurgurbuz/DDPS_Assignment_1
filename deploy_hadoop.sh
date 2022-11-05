#!/bin/bash

set -e

if [[ $# -lt 1 ]] ; then
	echo ""
	echo "usage: sh deploy_hadoop.sh [iterations"
	echo "for example: sh deploy_hadoop.sh 10"
	echo ""
	exit 1
fi

#curl -L -o "/var/scratch/$USER/spark/jars/graphframes-0.8.2-spark3.2-s_2.12.jar" https://repos.spark-packages.org/graphframes/graphframes/0.8.2-spark3.2-s_2.12/graphframes-0.8.2-spark3.2-s_2.12.jar
#wget -O /var/scratch/$USER/hadoop-2.7.0.tar.gz https://archive.apache.org/dist/hadoop/common/hadoop-2.7.0/hadoop-2.7.0.tar.gz && \
#tar -zxf /var/scratch/$USER/hadoop-2.7.0.tar.gz -C /var/scratch/$USER && mv /var/scratch/$USER/hadoop-2.7.0 /var/scratch/$USER/hadoop
#rm /var/scratch/$USER/hadoop-2.7.0.tar.gz

mkdir -p /var/scratch/$USER/hadoop_hdfs
mkdir -p /var/scratch/$USER/hadoop_hdfs/namenode
mkdir -p /var/scratch/$USER/hadoop_hdfs/datanode
mkdir -p /var/scratch/$USER/hadoop_hdfs/temp
cp /var/scratch/$USER/DDPS_Assignment_1/hadoop_xml_configs/hdfs-site.xml /var/scratch/$USER/hadoop/etc/hadoop/hdfs-site.xml
cp /var/scratch/$USER/DDPS_Assignment_1/hadoop_xml_configs/core-site.xml /var/scratch/$USER/hadoop/etc/hadoop/core-site.xml
cp /var/scratch/$USER/DDPS_Assignment_1/hadoop_xml_configs/yarn-site.xml /var/scratch/$USER/hadoop/etc/hadoop/yarn-site.xml
cp /var/scratch/$USER/DDPS_Assignment_1/hadoop_xml_configs/mapred-site.xml /var/scratch/$USER/hadoop/etc/hadoop/mapred-site.xml

echo "export JAVA_HOME=/var/scratch/$USER/jdk-11.0.2" >> mapred-env.sh
echo "export JAVA_HOME=/var/scratch/$USER/jdk-11.0.2" >> hadoop-env.sh
echo "export JAVA_HOME=/var/scratch/$USER/jdk-11.0.2" >> yarn-env.sh

# # Optional?
# hdfs namenode -format
# start-dfs.sh

# Create input and output directories on hdfs
hadoop fs -mkdir /input
hadoop fs -mkdir /output
hadoop fs -put datasets/soc-Epinions1.txt /input

# Download pagerank for hadoop implementation
cd .. && git clone https://github.com/danielepantaleone/hadoop-pagerank.git && cd hadoop-pagerank

# Inspiration: https://stackoverflow.com/questions/49951114/java-class-not-found-for-pagerank-algorithm-in-apache-hadoop
javac -classpath ${HADOOP_CLASSPATH} -d ./ src/it/uniroma1/hadoop/pagerank/PageRank.java src/it/uniroma1/hadoop/pagerank/job1/PageRankJob1Mapper.java src/it/uniroma1/hadoop/pagerank/job1/PageRankJob1Reducer.java src/it/uniroma1/hadoop/pagerank/job2/PageRankJob2Mapper.java src/it/uniroma1/hadoop/pagerank/job2/PageRankJob2Reducer.java src/it/uniroma1/hadoop/pagerank/job3/PageRankJob3Mapper.java 
jar -cf it/pagerank.jar it/
cd ..
hadoop jar hadoop-pagerank/it/pagerank.jar it.uniroma1.hadoop.pagerank.PageRank --input /input/soc-Epinions1.txt --output /output --count {}