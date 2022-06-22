# NOTES ----->
# Now working with python 3 xx


from __future__ import print_function
import gspread
import os
import json
import serial
import logging
import time
import mysql.connector
import yaml
import requests
from datetime import datetime
from datetime import date
from datetime import timedelta

import exceptions as ex

#Import config
config = yaml.safe_load(open("config.yml"))

#GLOBAL VARIABLES
TEMP_COL = 2
PRESSURE_COL = 3
HUMIDITY_COL = 4
ser = None

#custom print function that is nicely formatted
def printt(someString):
	someString = str(datetime.now()) + " | " +  someString
	print(someString)
	return;
#same as above, with no newline char, so can write on the same line again
def writet(someString):
	someString = str(datetime.now()) + " | " +  someString
	print(someString, end='')
	return;

#write data using the webapp API (/api/weatherdata)
def writeData(ser):
	theDate = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

	dataCollected = []
	#For some reason the arduino code wasn't working in my testing environment without checking for a newline.
	#So now we send newlines with at the ends of our requests for data.
	ser.write("y\n".encode())
	for index, column in enumerate([TEMP_COL, PRESSURE_COL, HUMIDITY_COL]):
		time.sleep(1)
		data = ser.readline().strip().decode('utf8')
		writet("data" + str(index+1) + ": ")
		print(data)
		dataCollected.append(data)
		time.sleep(1)

	if not len(dataCollected) == 3:
		#Didn't collect enough data
		s = ""
		for d in dataCollected:
			s += str(d) + ", "
		s = s[:-2]
		raise ex.serialError("Only collected " + s)

	r = requests.post('http://' + config["webserver-ip"] + '/api/weatherdata', data = {
			"date": theDate[:theDate.index(" ")].replace("/", "-"),
			"time": theDate[theDate.index(" ")+1:],
			"temperature": dataCollected[0],
			"pressure": dataCollected[1],
			"humidity": dataCollected[2]
		})
	
	response = r.json()
	if r.status_code == 201:
		#prints "Logged data in MySQL database at id 138", OR
		#"Logged data in Google Spreadsheet at row 3982"
		idORrow = str(list(response["data"])[-1])
		value = str(list(response["data"].values())[-1])
		printt("201 CREATED - Logged data in " + response["data"]["database"] + " at " + idORrow + " " + value)
	elif r.status_code == 404:
		printt("404 NOT FOUND - " + response["data"]["errorMessage"])
	elif r.status_code == 400:
		printt("400 BAD REQUEST - " + response["data"]["errorMessage"])

#debugging command. To enable calling of takeData and send "yes"
def debug():
	while True:
		userinput = input("TYPE s FOR SEND A \"YES\", TYPE t FOR TAKE DATA")
		if userinput=="s":
			ser.write("y\n".encode())
		elif userinput=="t":
			printt(ser.readline().strip().decode('utf8'))
		else:
			printt("invalid command") 

#debugging command
def userInput():
	while True:
		writet("")
		input("Press any key to take a one-off data collection... ")
		printt("Taking one-off data collection")
		mainFunc()


def mainFunc():
	#clean up
	os.system('clear')
	printt("STARTING... ")

	#Preparing the arduino
	ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
	time.sleep(5)
	
	#check if the serial port is open, if not, reopen
	if not ser.isOpen():
		ser.open()
		printt("Re-opened serial port.")
	else:
		printt("Serial port was still open, using it.")

	logging.basicConfig()
	printt("Making a data collection. Waiting... ")

	try:
		writeData(ser)
	except (ex.serialError) as e:
		printt("Unable to collect a full dataset!")
		printt(str(e))

	printt("Sheet write completed")
	printt("-------------------")

mainFunc()
#userInput()
#debug()
