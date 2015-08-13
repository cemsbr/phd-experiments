#!/bin/bash
master=hadoop0
ssh -CL 18088:$master:18080 -L 8088:$master:8080 -L 50077:$master:50070 \
    -L 4044:$master:4040 -L 8081:hadoop1:8081 \
    nuvemusp

# 4040  Spark app-specific
# 8080  Spark master
# 18080 Spark History Server
# 50070 HDFS
