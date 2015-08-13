#!/usr/bin/env python3.4
from experimentusp import ExperimentUSP
from expyrimenter.plugins.pushbullet import Pushbullet
import sys


if len(sys.argv) != 3:
    raise Exception('Inform current slave amount and repetition number.')
else:
    FIRST_SLAVE_AMOUNT = int(sys.argv[1])
    FIRST_REPETITION = int(sys.argv[2])

exp = ExperimentUSP()

exp.set_app('top_contributors.py')
exp.hdfs_file = '/enwiki.json'
exp.slave_amounts = [4, 8, 16, 32, 64]
exp.dfs_replications = {4: 1, 8: 2, 16: 3, 32: 3, 64: 3}
exp.repetitions = 2
exp.slave_amount = FIRST_SLAVE_AMOUNT
exp.repetition = FIRST_REPETITION

exp.run()
exp.finish()

Pushbullet().send_note('Experiment USP', 'Repetitions done :D')
