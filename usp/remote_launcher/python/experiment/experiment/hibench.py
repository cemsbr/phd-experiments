from expyrimenter.core import SSH, Executor

class HiBench:
    LOGGER = 'hibench'

    def __init__(self, home, hostname, executor=None):
        self._home = home
        self._host = hostname
        if executor is None:
            executor = Executor()
        self.executor = executor

    def clean_logs(self):
        cmd = 'rm -rf {}/report'.format(self._home)
        self._ssh(cmd, 'Delete reports')

    def set_parallelism(self, cores, benchmark):
        """AKA reduce number. Benchmark example: 'sort'."""
        config = '{}/workloads/{}/conf/10-{}-userdefine.conf'.format(self._home,
            benchmark, benchmark)
        cmd = 'echo hibench.default.map.parallelism {:d} >{}'.format(cores,
                                                                     config)
        shuffle = int(cores/2)
        cmd += '; echo hibench.default.shuffle.parallelism {:d} >>{}'.format(
            shuffle, config)
        title = 'Set parallelism'
        self._ssh(cmd, title, stdout=True)

    def _ssh(self, cmd, title, *args, **kwargs):
        ssh = SSH(self._host, cmd, title=title, logger_name=HiBench.LOGGER,
                  *args, **kwargs)
        self.executor.run(ssh)
