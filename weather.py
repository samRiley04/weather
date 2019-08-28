# NOTES ----->
# running w/ python 2.6+ apparently, not python 3
# requires auth.json in the same directory, containing an service account API key thingo


from __future__ import print_function
import gspread
import os
import json
import serial
import logging
import time
import httplib2
from datetime import datetime
from datetime import date
from datetime import timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from oauth2client.service_account import ServiceAccountCredentials

#GLOBAL VARIABLES
TEMP_COL = 2
PRESSURE_COL = 3
HUMIDITY_COL = 4

#custom print function that is nicely formatted
def printt(string):
	string = str(datetime.now()) + " | " +  string
	print(string)
	return;
#same as above, with no newline char, so can write on the same line again
def writet(string):
	string = str(datetime.now()) + " | " +  string
	print(string, end='')
	return;


#gets next empty row in the google sheet
def next_free_row(worksheet):
	stringlist = filter(None, worksheet.col_values(1))
	return str(len(stringlist)+1)

#write data into the opened spreadsheet
def writeData(row):
	ser.write("y")
	time.sleep(1)
	dataIn = ser.readline().strip()
	writet("data1: ")
	print(dataIn)
	wks.update_cell(row, TEMP_COL, dataIn)
	time.sleep(1)
	dataIn = ser.readline().strip()
	writet("data2: ")
	print(dataIn)
	wks.update_cell(row, PRESSURE_COL, dataIn)
	time.sleep(1)
	dataIn = ser.readline().strip()
	writet("data3: ")
	print(dataIn)
	wks.update_cell(row, HUMIDITY_COL, dataIn)

	return 1;

#debugging command. To be called manually with debug()
def takeData():
	seriousBS = ser.readline().strip()
	return seriousBS
#debugging command. To be called manually with debug()
def sendYes():
	ser.write("y")
	return 1
#debugging command. To enable calling of takeData and send "yes"
def debug():
	while True:
		input = raw_input("TYPE s FOR SEND A \"YES\", TYPE t FOR TAKE DATA")
		if input=="s":
			sendYes()
		elif input=="t":
			printt(takeData())
		else:
			printt("didnt catch that?") 

#reauthorise the google sheet to use
def reauthoriseCreds():
	credentials = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
	gc = gspread.authorize(credentials)
	gc.login()

#function that will be called by the scheduler
def mainFunc():
	reauthoriseCreds()
	currentRow = next_free_row(wks)
	theDate = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
	wks.update_cell(currentRow, 1, theDate)	

	#check if the serial port is open, if not, reopen
	if not ser.isOpen():
		ser.open()
		printt("re-opened serial port")
	else:
		printt("serial port waas gucci")
	writeData(currentRow)

	printt("Sheet write completed")
	printt("-------------------")

def userInput():
	while True:
		writet("")
		raw_input("Press any key to take a one-off data collection... ")
		printt("Taking one-off data collection")
		mainFunc()

# 	CODE START --------------->

#clean up
os.system('clear')
printt("STARTING... ")
writet("Authorising with sheet api... ")

#initialse the google sheet we will write to
scope = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
gc = gspread.authorize(credentials)

wks = gc.open("Weather data").sheet1
print("done authorising")

#preparing the arduino. I think it's fucky because we aren't letting it start up before sending it commands, hence the sleep.
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(5)


dTemp = ""
dPressure = ""
dHumidity = ""

logging.basicConfig()
printt("Making a data collection. Waiting... ")
#userInput()
mainFunc()
#debug()
