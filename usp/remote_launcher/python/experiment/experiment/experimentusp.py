from .experiment import Experiment
from expyrimenter.plugins.cloudstack import Pool


class ExperimentUSP(Experiment):
    """All nodes but slaves must be started before running the experiment."""
    def __init__(self):
        dir_home = '/home/hadoop'
        super().__init__('hadoop0', dir_home)
        self._pool = get_pool()
        self._input_host = 'hadoop200'
        self._input_file = dir_home + '/data/enwiki-01G.spl.json.bz2'


def get_pool():
    """Return a pool of available workers."""
    pool = Pool()
    slaves = tuple(['hadoop{:d}'.format(i) for i in range(1, 5)])
    pool.hostnames = slaves
    return pool
