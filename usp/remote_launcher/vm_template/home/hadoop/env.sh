#!/bin/bash

#
# Hadoop
#

if [ -z $HADOOP_HOME ]; then
    export JAVA_HOME='/usr/lib/jvm/java-7-openjdk-amd64'
    export HADOOP_HOME="$HOME/hadoop/hadoop"
    export PATH="$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH"
fi

#
# Spark
#

if ! $(echo $PATH | grep -q spark); then
    export PATH="$HOME/spark/spark/bin:$HOME/spark/spark/sbin:$PATH"
fi

# Scala
if ! $(echo $PATH | grep -q scala); then
    export PATH="$HOME/scala/bin:$PATH"
fi
