from .experiment import Experiment
from expyrimenter.plugins.cloudstack import Pool


class ExperimentUSP(Experiment):
    """All nodes but slaves must be started before running the experiment."""
    def __init__(self):
        # Hard-coded values
        slave_amount = 5
        master = 'hadoop0'
        dir_home = '/home/hadoop'
        input_host = 'hadoop200'

        pool = get_slave_pool(slave_amount)
        super().__init__(master, dir_home, input_host, pool)


def get_slave_pool(amount):
    """Return a pool of available workers."""
    slaves = tuple(['hadoop{:d}'.format(i) for i in range(1, amount)])
    return Pool(slaves)
