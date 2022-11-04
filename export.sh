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
export PATH=${JAVA_HOME}/bin;
alias java="$JAVA_HOME/bin/java"

#SPARK & HADOOP
export SPARK_HOME=/var/scratch/$USER/spark;
export HADOOP_HOME=/var/scratch/$USER/hadoop;
export PATH=${SPARK_HOME}/bin:${HADOOP_HOME}/bin;
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9-src.zip;
EOF
source ~/.bashrc
