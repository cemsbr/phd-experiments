#!/usr/bin/env python3.4
from experiment import Experiment


with open('master_ips') as f:
    exp = Experiment(master=f.read().rstrip())
with open('slave_ips') as f:
    exp.slaves = f.read().split()

exp.add_barriers()
exp.stop()
exp.add_barriers()
exp.clean_logs()
exp.wait()
