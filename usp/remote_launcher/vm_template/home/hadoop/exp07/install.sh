#!/bin/bash

# Part I: Install Hadoop, Spark, Scala. Can be launched from any directory.
# Part II: Save information about the VM in current folder.

## Part I ##

#
#
# ATTENTION: will remove $HOME/hadoop and $HOME/spark before installing!
#
HADOOPV='2.7.1'
HADOOPD="hadoop-$HADOOPV"
HADOOPF="$HADOOPD.tar.gz"
SPARKV='1.5.1'
SPARKD="spark-$SPARKV-bin-hadoop2.6"
SPARKF="$SPARKD.tgz"

# Legacy experiments
cd $HOME
for i in $(seq 1 6); do
    if [ -d exp0$i ]; then
        tar cjf exp0$i.tar.bz2 exp0$i
        rm -rf exp0$i
    fi
done
cd - >/dev/null

#
# Hadoop
#

if [ ! -d $HOME/hadoop/$HADOOPD ]; then
    echo 'Installing Hadoop'
    rm -rf $HOME/hadoop
    mkdir $HOME/hadoop
    cd $HOME/hadoop
    wget -q http://ftp.unicamp.br/pub/apache/hadoop/common/$HADOOPD/$HADOOPF
    tar xzf $HADOOPF
    rm $HADOOPF
    ln -s $HADOOPD hadoop
    cd - >/dev/null
fi

#
# Spark
#

if [ ! -d $HOME/spark/$SPARKD ]; then
    echo 'Installing Spark'
    rm -rf $HOME/spark
    mkdir $HOME/spark
    cd $HOME/spark
    wget -q http://ftp.unicamp.br/pub/apache/spark/spark-$SPARKV/$SPARKF
    tar xzf $SPARKF
    rm $SPARKF
    ln -s $SPARKD spark
    cd - >/dev/null
fi

#
# Scala
#

if [ ! -d $HOME/scala/bin ]; then
    cd $HOME
    echo 'Installing Scala'
    rm -rf $HOME/scala
    wget -q http://downloads.typesafe.com/scala/2.11.7/scala-2.11.7.tgz
    tar xzf scala-2.11.7.tgz
    mv scala-2.11.7 scala
    rm scala-2.11.7.tgz
    cd - >/dev/null
fi

## Part II: Save information about the VM in current folder ##

DIR="outputs/vm-info/$(hostname)"
rm -rf $DIR
mkdir $DIR
cd $DIR
cat /proc/cpuinfo >cpuinfo
uname -a >uname
lsb_release -a >lsb_release 2>&1
java -version >java 2>&1
free -m >free-m
python --version >python 2>&1
scala -version >scala 2>&1
cd - >/dev/null
