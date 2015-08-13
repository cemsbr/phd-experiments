#!/bin/bash
PYTHONPATH='python/experiment'
PYTHONPATH="$PYTHONPATH:python/expyrimenter-core"
PYTHONPATH="$PYTHONPATH:python/expyrimenter-hadoop"
PYTHONPATH="$PYTHONPATH:python/expyrimenter-pushbullet"
PYTHONPATH="$PYTHONPATH:python/expyrimenter-spark"
PYTHONPATH="$PYTHONPATH:python/expyrimenter-cloudstack"
export PYTHONPATH
