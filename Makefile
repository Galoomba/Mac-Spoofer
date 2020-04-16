Register:
	crontab -l > macspoofer 
	# can add paramter here 
	echo "*/10 * * * * "$(shell pwd)"/MacSpoofer.py" >> macspoofer 
	crontab macspoofer
	rm macspoofer