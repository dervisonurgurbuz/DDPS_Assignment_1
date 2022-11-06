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

	usage: 
    
    ```console
    source deploy_spark.sh [nodes] [dataset] [pagerank iterations]
    ```

    ```console
    source deploy_spark.sh node105,node106,node107 datasets/soc-Epinions1.txt 10
    ```

(optional) uncomment commands in deploy_spark.sh to download spark and java on /var/scratch/$USER
```console
wget -O /var/scratch/$USER/spark-3.1.2-bin-hadoop2.7.tgz https://archive.apache.org/dist/spark/spark-3.1.2/spark-3.1.2-bin-hadoop2.7.tgz && \
tar -xf /var/scratch/$USER/spark-3.1.2-bin-hadoop2.7.tgz -C /var/scratch/$USER && mv /var/scratch/$USER/spark-3.1.2-bin-hadoop2.7 /var/scratch/$USER/spark
wget -O /var/scratch/$USER/openjdk-11.0.2_linux-x64_bin.tar.gz https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz && \
tar -zxf /var/scratch/$USER/openjdk-11.0.2_linux-x64_bin.tar.gz -C /var/scratch/$USER
rm /var/scratch/$USER/spark-3.1.2-bin-hadoop2.7.tgz
rm /var/scratch/$USER/openjdk-11.0.2_linux-x64_bin.tar.gz
```
2. The computing time per iteration will be stored in the npy_files folder

3. Run hadoop (from master node)(only works for soc-Epinions1.txt dataset):

    usage: 

    ```console 
    source deploy_hadoop.sh [nodes] [pagerank iterations]
    ```
    ```console
    source deploy_hadoop.sh node105,node106,node107 10
    ```

3.1 (optional) uncomment commands in deploy_hadoop.sh to: download hadoop; to set environment variables in mapred-env.sh, hadoop-env.sh and yarn-env.sh; create folders for datanode and namenodes; download pagerank for hadoop.

3.2 (optional) uncomment commands in deploy_hadoop.sh to format namenode.
usage: hdfs namenode -format

or if getting bugs later on: hdfs namenode -format -clusterID CID-887fb3d7-6840-45c2-8fea-eaa72b82b118

or if different clusterID: hdfs namenode -format -clusterID <clusterID>

3.3 (optional) 
