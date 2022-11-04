#!/bin/bash

mkdir -p $HADOOP_HOME/dfs
mkdir -p $HADOOP_HOME/dfs/name
mkdir -p $HADOOP_HOME/dfs/name/data
cp /var/scratch/$USER/DDPS_Assignment_1/hadoop_test/xml/hdfs-site.xml /var/scratch/$USER/hadoop/etc/hadoop/hdfs-site.xml
cp /var/scratch/$USER/DDPS_Assignment_1/hadoop_test/xml/core-site.xml /var/scratch/$USER/hadoop/etc/hadoop/core-site.xml
cp /var/scratch/$USER/DDPS_Assignment_1/hadoop_test/xml/yarn-site.xml /var/scratch/$USER/hadoop/etc/hadoop/yarn-site.xml
cp /var/scratch/$USER/DDPS_Assignment_1/hadoop_test/xml/mapred-site.xml /var/scratch/$USER/hadoop/etc/hadoop/mapred-site.xml