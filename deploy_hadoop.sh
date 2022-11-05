#!/bin/bash

#curl -L -o "/var/scratch/$USER/spark/jars/graphframes-0.8.2-spark3.2-s_2.12.jar" https://repos.spark-packages.org/graphframes/graphframes/0.8.2-spark3.2-s_2.12/graphframes-0.8.2-spark3.2-s_2.12.jar
#wget -O /var/scratch/$USER/hadoop-2.7.0.tar.gz https://archive.apache.org/dist/hadoop/common/hadoop-2.7.0/hadoop-2.7.0.tar.gz && \
#tar -zxf /var/scratch/$USER/hadoop-2.7.0.tar.gz -C /var/scratch/$USER && mv /var/scratch/$USER/hadoop-2.7.0 /var/scratch/$USER/hadoop
#rm /var/scratch/$USER/hadoop-2.7.0.tar.gz

mkdir /var/scratch/$USER/hadoop_hdfs
mkdir /var/scratch/$USER/hadoop_hdfs/namenode
mkdir /var/scratch/$USER/hadoop_hdfs/datanode
mkdir /var/scratch/$USER/hadoop_hdfs/temp
cp /var/scratch/$USER/DDPS_Assignment_1/hadoop_xml_configs/hdfs-site.xml /var/scratch/$USER/hadoop/etc/hadoop/hdfs-site.xml
cp /var/scratch/$USER/DDPS_Assignment_1/hadoop_xml_configs/core-site.xml /var/scratch/$USER/hadoop/etc/hadoop/core-site.xml
cp /var/scratch/$USER/DDPS_Assignment_1/hadoop_xml_configs/yarn-site.xml /var/scratch/$USER/hadoop/etc/hadoop/yarn-site.xml
cp /var/scratch/$USER/DDPS_Assignment_1/hadoop_xml_configs/mapred-site.xml /var/scratch/$USER/hadoop/etc/hadoop/mapred-site.xml

cd .. && git clone https://github.com/xiaojinhe/PageRank.git && java cf pr.jar PageRank/main/java/*.java

echo "export JAVA_HOME=/var/scratch/$USER/jdk-11.0.2" >> mapred-env.sh
echo "export JAVA_HOME=/var/scratch/$USER/jdk-11.0.2" >> hadoop-env.sh
echo "export JAVA_HOME=/var/scratch/$USER/jdk-11.0.2" >> yarn-env.sh