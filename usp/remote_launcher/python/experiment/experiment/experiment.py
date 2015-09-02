from expyrimenter.plugins.yarn import HDFS
from expyrimenter.plugins.spark import Spark
from expyrimenter.core import ExpyLogger, Executor, Shell
from expyrimenter.plugins.pushbullet import Pushbullet
import time


class Experiment:
    def __init__(self, master, dir_home, input_host, pool):
        # Hard-coded values
        input_file = dir_home + '/data/enwiki-01G.spl.json.bz2'  # @input_host
        dir_exp = dir_home + '/exp04'
        dir_output = dir_exp + '/outputs'
        self._output_file = dir_output + \
            '/spark-submit/slaves{:02d}_rep{:02d}_{}.txt'
        self._blocks_file = dir_output + \
            '/hdfs-blocks/slaves{:02d}_rep{:02d}.txt'

        # User defined
        self._app = None  # use self.set_app()
        self.hdfs_input = None  # app input, e.g. /enwiki.json
        self.slave_amounts = []
        self.dfs_replications = {}
        self.repetitions = 0
        # Resuming experiment:
        self.slave_amount = 0  # current slave amount
        self.repetition = 0  # current repetition (from 0)

        self.dir_exp = dir_exp
        self._input_host = input_host
        self._input_file = input_file
        self._pool = pool

        self._slaves = []
        self._logger = ExpyLogger.getLogger('experiment')

        # Spark
        dir_spark = dir_home + '/spark/spark'
        self._spark = Spark(home=dir_spark, master=master)
        self._spark_ex = self._spark.executor

        # HDFS
        dir_hadoop = dir_home + '/hadoop/hadoop'
        self._hdfs = HDFS(home=dir_hadoop, name_node=master)
        self._hdfs_ex = self._hdfs.executor
        self._dir_hadoop_tmp = dir_home + '/hadoop-tmp'

    def set_app(self, basename):
        self._app = '{}/{}'.format(self.dir_exp, basename)

    def _set_slaves(self, slaves):
        self._slaves = slaves
        self._systems_do(lambda s: s.set_slaves(slaves))

    def run(self):
        self._stop()
        self._restart_history_server()
        slave_amounts = [n for n in self.slave_amounts
                         if n >= self.slave_amount]
        for self.slave_amount in slave_amounts:
            self._get_slaves()
            for self.repetition in range(self.repetition, self.repetitions):
                self._hdfs_ex.add_barrier()
                self._spark_ex.add_barrier()
                self._run_once()
            self.repetition = 0
            self._mobile()

    def _restart_history_server(self):
        self._spark.stop_history_server()
        self._spark_ex.add_barrier()
        self._spark.start_history_server()

    def _mobile(self):
        body = 'Slave amount {:d} finished.'.format(self.slave_amount)
        Pushbullet().send_note('Experiment USP', body)

    def _run_once(self):
        self._start()
        self._hdfs_ex.add_barrier()
        self._save_blocks_info()
        self._submit_app()
        self._stop()

    def _submit_app(self):
        """Block while app is running."""
        stdout = self._output_file.format(self.slave_amount, self.repetition,
                                          'stdout')
        stderr = self._output_file.format(self.slave_amount, self.repetition,
                                          'stderr')
        self._wait()
        self._spark.submit(self._app, stdout, stderr)
        self._spark_ex.wait()

    def _stop(self):
        """Stop systems and clean temporary files."""
        self._systems_do(lambda s: s.stop())
        self._spark_ex.add_barrier()
        self._spark.clean_tmp()

    def finish(self):
        self._systems_do(lambda s: s.executor.add_barrier())
        self._spark.stop()
        self._spark_ex.add_barrier()
        self._spark.clean_tmp()
        self._hdfs.stop()
        self._pool.stop()
        self._pool.wait()
        self._wait()

    def _get_slaves(self):
        """When a VM is started, its logs are deleted."""
        # Hostname resolutions fail while starting VMs, so we wait.
        self._wait()
        slaves = self._pool.get(self.slave_amount)

        self._set_slaves(slaves)
        if self.repetition == 0:
            # Bootstrap recently started nodes
            self._bootstrap_hosts(self._pool.last_started)

    def _start(self):
        self._spark.start()
        # Format namenode
        if self.repetition == 0:
            self._clean_hdfs()
        else:
            self._hdfs.start()
        self._wait()
        time.sleep(60)

    def _clean_hdfs(self):
        self._hdfs.format(self._dir_hadoop_tmp)
        self._hdfs_ex.add_barrier()
        self._hdfs.start()
        self._hdfs_ex.wait()
        time.sleep(60)
        self._upload_input()

    def _save_blocks_info(self):
        output = self._blocks_file.format(len(self._slaves), self.repetition)
        self._hdfs.save_block_locations(self.hdfs_input, output)

    def _upload_input(self):
        self._logger.info('%d slaves, repetition %d.', self.slave_amount,
                          self.repetition)
        pipe = 'pbzip2 -dc ' + self._input_file
        repl = self.dfs_replications[self.slave_amount]
        self._hdfs.put_from_pipe(self._input_host, pipe, self.hdfs_input, repl)

    def _bootstrap_hosts(self, hosts):
        self._systems_do(lambda s: s.clean_logs(hosts))
        cmd = 'VM={} make --quiet bootstrap-vm'
        executor = Executor()
        for host in hosts:
            executor.run(Shell(cmd.format(host), 'bootstrap ' + host))
        executor.shutdown()  # blocking

    def _wait(self):
        self._systems_do(lambda s: s.executor.wait())

    def _systems_do(self, func):
        func(self._spark)
        func(self._hdfs)
