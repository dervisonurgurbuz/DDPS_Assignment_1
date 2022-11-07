#!/bin/bash
# Simple script for deploying Spark in standalone mode on DAS-5 for the DDPS course 2022.
# Author: Yuxuan Zhao

set -e # The set command allows you to manage certain flags and characteristics to influence how your bash scripts behave.

if [[ $# -lt 1 ]] ; then
	echo ""
	echo "usage: source deploy_spark.sh [nodes] [dataset] [pagerank iterations]"
	echo "for example: source deploy_spark.sh node105,node106,node107 soc-Epinions1.txt 10"
	echo ""
	exit 1
fi

echo "Deploying spark on ${1}"
nodes=${1}
IFS=',' read -ra node_list <<< "$nodes"; unset IFS
master=${node_list[0]}
worker=${node_list[@]:1}
echo "master is "$master
echo "worker is "$worker

#Comment out these lines if you already downloaded them.
#wget -O /var/scratch/$USER/spark-3.1.2-bin-hadoop2.7.tgz https://archive.apache.org/dist/spark/spark-3.1.2/spark-3.1.2-bin-hadoop2.7.tgz && \
#tar -xf /var/scratch/$USER/spark-3.1.2-bin-hadoop2.7.tgz -C /var/scratch/$USER && mv /var/scratch/$USER/spark-3.1.2-bin-hadoop2.7 /var/scratch/$USER/spark
#wget -O /var/scratch/$USER/openjdk-11.0.2_linux-x64_bin.tar.gz https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz && \
#tar -zxf /var/scratch/$USER/openjdk-11.0.2_linux-x64_bin.tar.gz -C /var/scratch/$USER
#rm /var/scratch/$USER/spark-3.1.2-bin-hadoop2.7.tgz
#rm /var/scratch/$USER/openjdk-11.0.2_linux-x64_bin.tar.gz

source export.sh

cd /var/scratch/$USER/spark/conf && cp spark-env.sh.template spark-env.sh && cp workers.template workers
sleep 3
echo "export JAVA_HOME=/var/scratch/$USER/jdk-11.0.2" >> spark-env.sh
echo "export SPARK_MASTER_HOST=$master" >> spark-env.sh
echo "export SPARK_MASTER_HOST=$master" >> spark-env.sh
echo "$worker" > workers

ssh $master "spark-submit --executor-memory 4g /var/scratch/$USER/DDPS_Assignment_1/pyspark_pagerank.py /var/scratch/$USER/DDPS_Assignment_1/datasets/${2} ${3} ${#node_list[@]}"  