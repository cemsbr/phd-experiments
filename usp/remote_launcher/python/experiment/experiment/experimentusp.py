from .experiment import Experiment
from expyrimenter.plugins.cloudstack import Pool


class ExperimentUSP(Experiment):
    """All nodes but slaves must be started before running the experiment."""
    def __init__(self):
        # Hard-coded values
        master = 'hadoop0'
        dir_home = '/home/hadoop'
        input_host = 'hadoop199'

        pool = get_slave_pool(128)
        super().__init__(master, dir_home, input_host, pool)


def get_slave_pool(amount):
    """Return a pool of available workers."""
    slaves = tuple(['hadoop{:d}'.format(i) for i in range(1, amount + 1)])
    return Pool(slaves)
