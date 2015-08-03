# ~/.bashrc's _first line_
test -f ~/env.sh && . ~/env.sh

# gateway's ~/.ssh/config
StrictHostKeyChecking no
# create ssh keys, copy to master and to authorized keys of every node
# copy grc config from expy-core to ~/.grc
# expyrimenter config.ini
# USP: python-requests

# packages (all):
- htop (optional)
- tree (optional)

# packages (workers)
- openjdk-7-jre-headless

# package (gateway)
- python3-requests
- ipython3
- grc
- make
