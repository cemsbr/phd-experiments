#!/usr/bin/env python3.4
import sys
from experiment import ExperimentUSP
from expyrimenter.plugins.pushbullet import Pushbullet

SLAVES_INPUTS = {
    1: [32, 64, 128, 256, 512, 1024, 2048, 4096],
    2: [32, 64, 128, 256, 512, 1024, 2048, 4096],
    3: [32, 64, 128, 256, 512, 1024, 2048, 4096],
    4: [32, 64, 128, 256, 512, 1024, 2048, 4096],
    5: [32, 64, 128, 256, 512, 1024, 2048, 4096],
    6: [32, 64, 128, 256, 512, 1024, 2048, 4096],
    7: [32, 64, 128, 256, 512, 1024, 2048, 4096],
    8: [32, 64, 128, 256, 512, 1024, 2048, 4096]
}

eg_slave_amount = sorted(SLAVES_INPUTS.keys())[0]
eg_input = SLAVES_INPUTS[eg_slave_amount][0]

if len(sys.argv) != 4:
    raise Exception('Inform current slave, input size and repetition number.'
                    'E.g.:\n{} {:d} {} 0'.format(sys.argv[0], eg_slave_amount,
                                                 eg_input))
else:
    FIRST_SLAVE_AMOUNT = int(sys.argv[1])
    FIRST_SIZE = sys.argv[2]
    FIRST_REPETITION = int(sys.argv[3])

# Common settings for all input sizes
exp = ExperimentUSP()
exp.set_app('../hibench/hibench/workloads/kmeans/spark/scala/bin/run.sh')
exp.hdfs_input = '/'
exp.repetitions = 5

# We might have already run some repetitions for the first input file
exp.slave_amount = FIRST_SLAVE_AMOUNT
exp.repetition = FIRST_REPETITION

pb = Pushbullet()

exp_done = True
for slave_amount in sorted(SLAVES_INPUTS.keys()):
    if slave_amount < FIRST_SLAVE_AMOUNT:
        continue
    exp.slave_amounts = [slave_amount]
    exp.slave_amount = slave_amount
    for size in SLAVES_INPUTS[slave_amount]:
        if exp_done and str(size) == FIRST_SIZE:
            exp_done = False
            exp.repetition = FIRST_REPETITION
        if not exp_done:
            exp.set_input_file('data/{:d}K/HiBench'.format(size))
            exp.run()
            msg = '{:d} slaves, {} size finished'.format(slave_amount, size)
            pb.send_note('Experiment at USP', msg)
            exp.repetiton = 0

exp.finish()
cs.stop('hadoop0 hadoop200'.split())
cs.executor.wait()
pb.send_note('Experiment at USP', 'All done!')
