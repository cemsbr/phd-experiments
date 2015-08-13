#!/bin/bash
#
# ATTENTION: will remove $HOME/hadoop and $HOME/spark before installing!
#

#
# Hadoop
#

if [ ! -d $HOME/hadoop/hadoop-2.6.0 ]; then
    echo 'Installing Hadoop'
    rm -rf $HOME/hadoop
    mkdir $HOME/hadoop
    cd $HOME/hadoop
    wget -q http://ftp.unicamp.br/pub/apache/hadoop/common/hadoop-2.6.0/hadoop-2.6.0.tar.gz
    tar xzf hadoop-2.6.0.tar.gz
    rm hadoop-2.6.0.tar.gz
    ln -s hadoop-2.6.0 hadoop
    cd -
fi

#
# Spark
#

if [ ! -d $HOME/spark/spark-1.3.1-bin-hadoop2.6 ]; then
    echo 'Installing Spark'
    rm -rf $HOME/spark
    mkdir $HOME/spark
    cd $HOME/spark
    wget -q http://ftp.unicamp.br/pub/apache/spark/spark-1.3.1/spark-1.3.1-bin-hadoop2.6.tgz
    tar xzf spark-1.3.1-bin-hadoop2.6.tgz
    rm spark-1.3.1-bin-hadoop2.6.tgz
    ln -s spark-1.3.1-bin-hadoop2.6 spark
    cd -
fi
