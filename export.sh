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

#SPARK
export SPARK_HOME=/var/scratch/$USER/spark;
export PATH=${SPARK_HOME}/bin:${PATH};
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/lib;
EOF
source ~/.bashrc
