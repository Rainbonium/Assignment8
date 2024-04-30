from pymongo import MongoClient, database
import subprocess
import threading
import pymongo
from datetime import datetime, timedelta
import time

DBName = "test" #Use this to change which Database we're accessing
connectionURL = "mongodb+srv://admin:admin@cluster0.yxwjeml.mongodb.net/?retryWrites=true&w=majority" #Put your database URL here
sensorTable = "Sensor Data" #Change this to the name of your sensor data table

def QueryToList(query):
	result = []
	for document in query:
		result.append(document)
	return result

def QueryDatabase() -> []:
	global DBName
	global connectionURL
	global currentDBName
	global running
	global filterTime
	global sensorTable
	cluster = None
	client = None
	db = None
	try:
		cluster = connectionURL
		client = MongoClient(cluster)
		db = client[DBName]
		#print("Database collections: ", db.list_collection_names())

		#We first ask the user which collection they'd like to draw from.
		sensorTable = db[sensorTable]
		#print("Table:", sensorTable)
		#We convert the cursor that mongo gives us to a list for easier iteration.
		timeCutOff = datetime.now() - timedelta(minutes=5)

		documents = QueryToList(sensorTable.find({"time":{"$gte":timeCutOff}}))

		if len(documents) == 0:
			print("No recent data found, switching to general data.")
			documents = QueryToList(sensorTable.find({"time":{"$lte":timeCutOff}}))

		sensor_data = []
		for doc in documents:
			sensor_payload = doc.get("payload", {})

			sensor_name = list(sensor_payload.keys())[3]
			sensor_value = list(sensor_payload.values())[3]

			sensor_data.append({"sensor_name": sensor_name, "sensor_value": int(sensor_value)})

		print("Finished")
		return sensor_data

	except Exception as e:
		print("Please make sure that this machine's IP has access to MongoDB.")
		print("Error:",e)
		exit(0)