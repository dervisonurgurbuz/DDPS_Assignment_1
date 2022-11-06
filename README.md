# DDPS_Assignment_1


1. To download datasets, run:

```console
python download_datasets.py
```

(optional) you might need to download python libraries (download as --user in ~/ to avoid requiring any special privileges). e.g., by running 

```console
pip install --user pandas
```

2. Run spark (from front-end):

    (optional) uncomment the following lines in deploy_spark.sh to download spark and java on /var/scratch/$USER.
    ```console
    wget -O /var/scratch/$USER/spark-3.1.2-bin-hadoop2.7.tgz https://archive.apache.org/dist/spark/spark-3.1.2/spark-3.1.2-bin-hadoop2.7.tgz && \
    tar -xf /var/scratch/$USER/spark-3.1.2-bin-hadoop2.7.tgz -C /var/scratch/$USER && mv /var/scratch/$USER/spark-3.1.2-bin-hadoop2.7 /var/scratch/$USER/spark
    wget -O /var/scratch/$USER/openjdk-11.0.2_linux-x64_bin.tar.gz https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz && \
    tar -zxf /var/scratch/$USER/openjdk-11.0.2_linux-x64_bin.tar.gz -C /var/scratch/$USER
    rm /var/scratch/$USER/spark-3.1.2-bin-hadoop2.7.tgz
    rm /var/scratch/$USER/openjdk-11.0.2_linux-x64_bin.tar.gz
    ```

	usage: 
    
    ```console
    source deploy_spark.sh [nodes] [dataset] [pagerank iterations]
    ```

    ```console
    source deploy_spark.sh node105,node106,node107 datasets/soc-Epinions1.txt 10
    ```

    (optional) comment out again following commands.
    ```console
    # wget -O /var/scratch/$USER/spark-3.1.2-bin-hadoop2.7.tgz https://archive.apache.org/dist/spark/spark-3.1.2/spark-3.1.2-bin-hadoop2.7.tgz && \
    # tar -xf /var/scratch/$USER/spark-3.1.2-bin-hadoop2.7.tgz -C /var/scratch/$USER && mv /var/scratch/$USER/spark-3.1.2-bin-hadoop2.7 /var/scratch/$USER/spark
    # wget -O /var/scratch/$USER/openjdk-11.0.2_linux-x64_bin.tar.gz https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz && \
    # tar -zxf /var/scratch/$USER/openjdk-11.0.2_linux-x64_bin.tar.gz -C /var/scratch/$USER
    # rm /var/scratch/$USER/spark-3.1.2-bin-hadoop2.7.tgz
    # rm /var/scratch/$USER/openjdk-11.0.2_linux-x64_bin.tar.gz
    ```

    The computing time per iteration will be stored in the npy_files folder

3. Run hadoop (from master node)(only works for soc-Epinions1.txt dataset):

    (optional) uncomment the following lines in deploy_hadoop.sh to: download hadoop; to set environment variables in mapred-env.sh, hadoop-env.sh and yarn-env.sh; create folders for datanode and namenodes; download pagerank for hadoop.
    ```console 
    # Download hadoop
    curl -L -o "/var/scratch/$USER/spark/jars/graphframes-0.8.2-spark3.2-s_2.12.jar" https://repos.spark-packages.org/graphframes/graphframes/0.8.2-spark3.2-s_2.12/graphframes-0.8.2-spark3.2-s_2.12.jar
    wget -O /var/scratch/$USER/hadoop-2.7.0.tar.gz https://archive.apache.org/dist/hadoop/common/hadoop-2.7.0/hadoop-2.7.0.tar.gz && \
    tar -zxf /var/scratch/$USER/hadoop-2.7.0.tar.gz -C /var/scratch/$USER && mv /var/scratch/$USER/hadoop-2.7.0 /var/scratch/$USER/hadoop
    rm /var/scratch/$USER/hadoop-2.7.0.tar.gz

    # Set environment variables
    cd /var/scratch/$USER/hadoop/etc/hadoop
    echo "export JAVA_HOME=/var/scratch/$USER/jdk-11.0.2" >> mapred-env.sh
    echo "export JAVA_HOME=/var/scratch/$USER/jdk-11.0.2" >> hadoop-env.sh
    echo "export JAVA_HOME=/var/scratch/$USER/jdk-11.0.2" >> yarn-env.sh
    cd /var/scratch/$USER/DDPS_Assignment_1

    # Create namenode and datanode directories
    mkdir /var/scratch/$USER/hadoop/dfs
    mkdir /var/scratch/$USER/hadoop/dfs/namenode
    mkdir /var/scratch/$USER/hadoop/dfs/datanode
    mkdir /var/scratch/$USER/hadoop/dfs/temp

    # Download pagerank for hadoop implementation
    cd .. && git clone https://github.com/danielepantaleone/hadoop-pagerank.git || true && cd hadoop-pagerank

    # Compile pagerank code, then turn to jar file.
    javac -classpath ${HADOOP_CLASSPATH} -d ./ src/it/uniroma1/hadoop/pagerank/PageRank.java src/it/uniroma1/hadoop/pagerank/job1/PageRankJob1Mapper.java src/it/uniroma1/hadoop/pagerank/job1/PageRankJob1Reducer.java src/it/uniroma1/hadoop/pagerank/job2/PageRankJob2Mapper.java src/it/uniroma1/hadoop/pagerank/job2/PageRankJob2Reducer.java src/it/uniroma1/hadoop/pagerank/job3/PageRankJob3Mapper.java 
    jar -cf it/pagerank.jar it/
    cd ../DDPS_Assignment_1
    ```

    usage: 

    ```console 
    source deploy_hadoop.sh [nodes] [pagerank iterations]
    ```
    ```console
    source deploy_hadoop.sh node105,node106,node107 10
    ```
    (optional) uncomment commands in deploy_hadoop.sh to format namenode.
    usage: 
    ```console
    hdfs namenode -format
    ```

    when start-dfs.sh does not create a live datanode and live namenode, the clusterID of the namenode might not match the datanode. Check with command:
    ```console 
    jps
    ```
    If clusterID of the namenode does not match the datanode, run:
    
    ```console 
    hdfs namenode -format -clusterID CID-887fb3d7-6840-45c2-8fea-eaa72b82b118
    ```
    or in general:
    ```console 
    hdfs namenode -format -clusterID <clusterID>
    ```

3.3 (optional) 
