# weather ting

crontab runs the weather.py script each hour. Logs a dump of the output into a log file at /tmp/weather.log

HARDWARE REPAIRED 29/09/20
Wires finally snapped off after all that abuse of being crushed under windows and between doors.
Resoldered and seems to work.

BME280 -> Arduino wiring for future reference:
VIN -> 5v
GND -> GND
SCK -> A5
SDI -> A4

DEBUGGED 28/08/19
Had multiple lines a day that would either record no data, or miss the first temperature value and put it in air
pressure, then put air pressure in humidity etc. For 27/08, only one row had correct formatting and all values.

Attempt to fix: I think the arduino isnt given enough time to 'boot up' or whatever, before the serial "y" value
is being sent. We are opening the serial port at the start of each time the script is run, because cron is running
it and then closing the script. The port isnt being kept open, so I think this is plausible.

Also quickly put in some functions to manually send and receive data from arduino to see if there were any issues
there, but it was all working normally.

UPDATED 7/01/2021
Long time since I updated this. Have brought it a bit more up to speed as I've learned more python standards. Now utilises HTTP calls to my webserver to POST data.

# Crontab contents
```
@reboot sleep 10 && cd ~/Documents/Samhome/Samhome; ./start.zsh
0 0 * * * cd ~/Documents/weather; python3 weather.py
```