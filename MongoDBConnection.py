from pymongo import MongoClient, database
import traceback
import subprocess
import threading
import pymongo
from datetime import datetime, timedelta, timezone
import time

DBName = "test" #Use this to change which Database we're accessing
connectionURL = "mongodb+srv://admin:admin@cluster0.yxwjeml.mongodb.net/?retryWrites=true&w=majority" #Put your database URL here

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
		sensorTable = db["Sensor Data"]
		sensorTable_meta = db["Sensor Data_metadata"]
		#print("Table:", sensorTable)
		#We convert the cursor that mongo gives us to a list for easier iteration.
		timeCutOff = datetime.now(timezone.utc) - timedelta(minutes=5)

		documents = QueryToList(sensorTable.find({"time":{"$gte":timeCutOff}}))
		documents_meta = QueryToList(sensorTable_meta.find())

		if len(documents) == 0:
			print("No recent data found, switching to general data.")
			documents = QueryToList(sensorTable.find({"time":{"$lte":timeCutOff}}))

		sensor_data = []
		for doc in documents:
			sensor_payload = doc.get("payload", {})

			if not len(list(sensor_payload.values())) == 4: break

			sensor_value = list(sensor_payload.values())[3]
			sensor_id = list(sensor_payload.values())[2]

			highway_name = "Error Retrieving Name"
			for doc_meta in documents_meta:
				doc_meta_id = doc_meta.get("assetUid")
				if doc_meta_id == sensor_id:
					eventTypes = doc_meta.get("eventTypes", [])
					device = eventTypes[0][0].get("device")
					if device:
						highway_name = device.get("name")
						if highway_name:
							highway_name = highway_name.replace(" Device", "")
							break

			sensor_data.append({"highway_name": highway_name, "sensor_value": int(sensor_value)})

		print("Finished")
		return sensor_data

	except Exception as e:
		print("Please make sure that this machine's IP has access to MongoDB.")
		print("Error:",e)
		print(traceback.format_exc())
		exit(0)