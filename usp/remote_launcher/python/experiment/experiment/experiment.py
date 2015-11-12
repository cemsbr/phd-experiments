import time
from shlex import quote

from expyrimenter.plugins.yarn import HDFS
from expyrimenter.plugins.spark import Spark
from expyrimenter.core import ExpyLogger, Executor, Shell, SSH
from expyrimenter.plugins.pushbullet import Pushbullet
from .hibench import HiBench


class Experiment:
    def __init__(self, master, dir_home, input_host, pool):
        self._dir_home = dir_home
        self._input_host = input_host
        self.pool = pool

        # Hard-coded values
        self._dir_exp = dir_home + '/exp07'
        dir_output = self._dir_exp + '/outputs'
        self._output_file = dir_output + \
            '/spark-submit/slaves{:02d}_rep{:02d}_{}.txt'
        self._blocks_file = dir_output + '/hdfs-blocks/slaves{:02d}.txt'

        # User defined
        self._app = None  # use self.set_app()
        self._input_file = None  # use self.set_input_file()
        self.hdfs_input = None  # app input, e.g. /enwiki.json
        self.slave_amounts = []
        self.repetitions = 0
        # Resuming experiment:
        self.slave_amount = 0  # current slave amount
        self.repetition = 0  # current repetition (from 0)

        self._slaves = []
        self._logger = ExpyLogger.getLogger('experiment')

        # Spark
        dir_spark = dir_home + '/spark/spark'
        self.spark = Spark(home=dir_spark, master=master)
        self.spark_ex = self.spark.executor

        # HDFS
        dir_hadoop = dir_home + '/hadoop/hadoop'
        self.hdfs = HDFS(home=dir_hadoop, name_node=master)
        self.hdfs_ex = self.hdfs.executor
        self._dir_hadoop_tmp = dir_home + '/hadoop-tmp'

        # HiBench
        dir_hibench = dir_home + '/hibench/hibench'
        self.hibench = HiBench(dir_hibench, master)

        self.master = master

    def set_app(self, basename):
        self._app = '{}/{}'.format(self._dir_exp, basename)

    def set_input_file(self, home_relative_path):
        self._input_file = '{}/{}'.format(self._dir_home, home_relative_path)

    def _set_slaves(self, slaves):
        self._slaves = slaves
        self._systems_do(lambda s: s.set_slaves(slaves))
        self.hibench.set_parallelism(len(slaves) * 2, 'sort')

    def run(self):
        self.stop()
        self._restart_history_server()
        slave_amounts = (n for n in self.slave_amounts
                         if n >= self.slave_amount)
        for self.slave_amount in slave_amounts:
            self._prepare_slaves()
            for self.repetition in range(self.repetition, self.repetitions):
                self.hdfs_ex.add_barrier()
                self.spark_ex.add_barrier()
                self._run_once()
            self.repetition = 0
            #self._mobile()

    def _restart_history_server(self):
        self.spark.stop_history_server()
        self.spark_ex.add_barrier()
        self.spark.start_history_server()

    def _mobile(self):
        body = 'Slave amount {:d} finished.'.format(self.slave_amount)
        Pushbullet().send_note('Experiment USP', body)

    def _run_once(self):
        self._start()
        self._submit_app()
        self.stop()

    def _submit_app(self):
        """Block while app is running."""
        stdout = self._output_file.format(self.slave_amount, self.repetition,
                                          'stdout')
        stderr = self._output_file.format(self.slave_amount, self.repetition,
                                          'stderr')
        cmd = '{} 1>{} 2>{}'.format(quote(self._app), quote(stdout),
                                    quote(stderr))
        ssh = SSH(self.master, cmd, stdout=True, stderr=True)
        self.wait()
        ssh.run()

    def stop(self):
        """Stop systems and clean temporary files."""
        self._systems_do(lambda s: s.executor.add_barrier())
        self._systems_do(lambda s: s.stop())
        self.spark_ex.add_barrier()
        self.spark.clean_tmp()

    def finish(self):
        """(blocking) Stop systems, clean temp files and shutdown pool."""
        self.stop()
        self.wait()
        self.pool.stop()
        self.pool.wait()

    def _prepare_slaves(self):
        """When a VM is started, its logs are deleted."""
        # Hostname resolutions fail while starting VMs, so we wait.
        self.wait()
        slaves = self.pool.get(self.slave_amount)

        self._set_slaves(slaves)
        if self.repetition == 0:
            # Bootstrap recently started nodes
            self._bootstrap_hosts(self.pool.last_started)

    def _start(self):
        self.spark.start()
        # Format namenode
        if self.repetition == 0:
            self._clean_hdfs()
        else:
            self.hdfs.start()
        self.wait()
        time.sleep(60)

    def format_hdfs(self):
        self.hdfs.format(self._dir_hadoop_tmp)

    def _clean_hdfs(self):
        self.format_hdfs()
        self.hdfs_ex.add_barrier()
        self.hdfs.start()
        self.hdfs_ex.wait()
        time.sleep(60)
        self._upload_input()

    def _save_blocks_info(self):
        output = self._blocks_file.format(len(self._slaves))
        self.hdfs.save_block_locations(self.hdfs_input, output)

    def _upload_input(self):
        self._logger.info('%d slaves, repetition %d.', self.slave_amount,
                          self.repetition)
        pipe = 'pbzip2 -dc ' + self._input_file
        repl = min(self.slave_amount, 3)
        self.hdfs.put_from_pipe(self._input_host, pipe, self.hdfs_input, repl)
        self.hdfs_ex.add_barrier()
        self._save_blocks_info()

    def _bootstrap_hosts(self, hosts):
        self._systems_do(lambda s: s.clean_logs(hosts))
        cmd = 'VM={} make --quiet bootstrap-vm'
        executor = Executor()
        for host in hosts:
            executor.run(Shell(cmd.format(host), 'bootstrap ' + host))
        executor.shutdown()  # blocking

    def wait(self):
        self._systems_do(lambda s: s.executor.wait())
        self.hibench.executor.wait()

    def _systems_do(self, func):
        func(self.spark)
        func(self.hdfs)
