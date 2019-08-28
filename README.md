crontab runs the weather.py script each hour. Logs a dump of the output into a log file at /tmp/weather.log

DEBUGGED 28/08
Had multiple lines a day that would either record no data, or miss the first temperature value and put it in air
pressure, then put air pressure in humidity etc. For 27/08, only one row had correct formatting and all values.

Attempt to fix: I think the arduino isnt given enough time to 'boot up' or whatever, before the serial "y" value
is being sent. We are opening the serial port at the start of each time the script is run, because cron is running
it and then closing the script. The port isnt being kept open, so I think this is plausible.

Also quickly put in some functions to manually send and receive data from arduino to see if there were any issues
there, but it was all working normally.
