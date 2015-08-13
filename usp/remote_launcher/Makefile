SHELL=/bin/bash

master_ip=hadoop0

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

bootstrap-vm:
	rsync -qrc vm_template/home/hadoop/ $(VM):.
	ssh $(VM) exp03/install.sh
	scp -qr hadoop_config/* $(VM):hadoop/hadoop/
	scp -qr spark_config/* $(VM):spark/spark/

master:
	scp top_contributors.py $(master_ip):exp03/

launch:
	-./exp03.py $(SLAVES) $(REP) 2>experiment.log
#	./mobile_finished.py

log_tail:
	tail -fn +1 experiment.log | grcat conf.expyrimenter

log_watch:
	./mobile_log_watcher.py
