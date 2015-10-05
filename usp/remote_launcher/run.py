#!/usr/bin/env python3.4
from experiment import ExperimentUSP
from expyrimenter.plugins.pushbullet import Pushbullet
import sys

inputs = [
    'data/enwiki-*M.spl.json.bz2 data/enwiki-01G.spl.json.bz2'
]

if len(sys.argv) != 3:
    raise Exception('Inform current slave amount and repetition number. E.g.:\n'
                    '%s 1 0' % sys.argv[0])
else:
    FIRST_SLAVE_AMOUNT = int(sys.argv[1])
    FIRST_REPETITION = int(sys.argv[2])

# Common settings for all input sizes
exp = ExperimentUSP()
exp.set_app('top_contributors.py')
exp.hdfs_input = '/enwiki.json'
exp.slave_amounts = [1, 2, 3]
exp.dfs_replications = {1: 1, 2: 2, 3: 3}
exp.repetitions = 10

pb = Pushbullet()

# We might have already run some repetitions for the first input file
for input in inputs:
    exp.set_input_file(input)
    exp.slave_amount = FIRST_SLAVE_AMOUNT
    exp.repetition = FIRST_REPETITION
    exp.run()

    exp.slave_amount = 1
    exp.repetition = 0

    msg = '{:d} reps with {} done.'.format(exp.repetitions, input)
    pb.send_note('Experiment at USP', msg)

exp.finish()
pb.send_note('Experiment at USP', 'All done!')
