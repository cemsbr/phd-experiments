#!/bin/bash
PYTHONPATH="$PWD/python/experiment"
PYTHONPATH="$PYTHONPATH:$PWD/python/expyrimenter-core"
PYTHONPATH="$PYTHONPATH:$PWD/python/expyrimenter-hadoop"
PYTHONPATH="$PYTHONPATH:$PWD/python/expyrimenter-pushbullet"
PYTHONPATH="$PYTHONPATH:$PWD/python/expyrimenter-spark"
PYTHONPATH="$PYTHONPATH:$PWD/python/expyrimenter-cloudstack"
export PYTHONPATH
