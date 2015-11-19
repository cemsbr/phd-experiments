SHELL=/bin/bash

exp_folder=exp08
master=hadoop0

help:
	@echo -e "VM=host make bootstrap-vm\n\
make master\n\
     launch\n\
     log_tail\n\
     log_watch"

bootstrap-all:
	for host in $$(cat master_ips slave_ips); do \
	    VM=$$host make bootstrap-vm& \
	    done

# FIXME: create folder as needed. Now, non-launcher VMs will have some empty
# folders from template.
bootstrap-vm:
	rsync -qrc vm_template/home/hadoop/ $(VM):.
	ssh $(VM) "cd $(exp_folder); ./install.sh"
	scp -qr hadoop_config/* $(VM):hadoop/hadoop/
	scp -qr spark_config/* $(VM):spark/spark/

master:
	ssh $(master) "test -d $(exp_folder) || mkdir $(exp_folder)"
	rsync -qrc hibench_config/* $(master):hibench/hibench/

launch:
	-./run.py $(SLAVES) $(INPUT) $(REP) 2>>experiment.log
	scripts/mobile_finished.py

log_tail:
	tail -fn +1 experiment.log | grcat conf.expyrimenter

log_watch:
	scripts/mobile_log_watcher.py
