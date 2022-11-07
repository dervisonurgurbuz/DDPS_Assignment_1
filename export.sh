cat > ~/.bashrc << EOF
#.bashrc
# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi
# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=
# User specific aliases and functions
module load gcc
module load slurm
module add prun
#JAVA
export JAVA_HOME=/var/scratch/$USER/jdk-11.0.2;
export PATH=${JAVA_HOME}/bin:${PATH};
alias java="$JAVA_HOME/bin/java"
#SPARKHADOOP
export SPARK_HOME=/var/scratch/$USER/spark;
export HADOOP_HOME=/var/scratch/$USER/hadoop;
export PATH=${SPARK_HOME}/bin:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin:${PATH};
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9-src.zip:/home/ddps2202/.local/lib/python2.7/site-packages;
# export HADOOP_MAPRED_HOME=$HADOOP_HOME 
# export HADOOP_COMMON_HOME=$HADOOP_HOME 
# export HADOOP_HDFS_HOME=$HADOOP_HOME 
# export YARN_HOME=$HADOOP_HOME 
# export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native 
# export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin 
# export HADOOP_INSTALL=$HADOOP_HOME 
# export HADOOP_OPTS="-Djava.library.path=$HADOOP_INSTALL/lib/native"
EOF
source ~/.bashrc