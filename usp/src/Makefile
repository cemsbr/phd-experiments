rsync:
	rsync -vrzcL --delete \
	    --exclude '.*.swp' \
	    --exclude '.git/' \
	    --exclude '__pycache__/' \
	    --exclude '*.log' \
	    remote_launcher nuvemusp:exp03/

unison:
	unison -auto remote_launcher
