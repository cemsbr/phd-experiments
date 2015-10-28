#!/usr/bin/env python3.4
import sys
from experiment import ExperimentUSP
from expyrimenter.plugins.pushbullet import Pushbullet

if len(sys.argv) != 3:
    raise Exception('Inform current slave amount and repetition number. E.g.:\n'
                    '%s 1 0' % sys.argv[0])
else:
    FIRST_SLAVE_AMOUNT = int(sys.argv[1])
    FIRST_REPETITION = int(sys.argv[2])

# Common settings for all input sizes
exp = ExperimentUSP()
exp.set_app('../hibench/hibench/workloads/sort/spark/scala/bin/run.sh')
exp.hdfs_input = '/HiBench/Sort/Input/part-m-00000'
exp.repetitions = 10

# We might have already run some repetitions for the first input file
exp.slave_amount = FIRST_SLAVE_AMOUNT
exp.repetition = FIRST_REPETITION

exp.slave_amounts = [1, 2, 4, 8, 12, 16]
exp.set_input_file('data/sort_huge.bz2')
exp.run()
exp.finish()

pb = Pushbullet()
pb.send_note('Experiment at USP', 'All done!')
