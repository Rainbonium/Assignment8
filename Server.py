import socket
import ipaddress
import threading
import time
import contextlib
import errno
from dataclasses import dataclass
import random
import sys

exitSignal = False
maxPacketSize = 1024
defaultPort = 25552

def GetFreePort(minPort: int = 1024, maxPort: int = 65535):
    for i in range(minPort, maxPort):
        print("Testing port",i)
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as potentialPort:
            try:
                potentialPort.bind(('localhost', i))
                potentialPort.close()
                print("Server listening on port",i)
                return i
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    print("Port",i,"already in use. Checking next...")
                else:
                    print("An exotic error occurred:",e)

def GetServerData() -> []:
    import MongoDBConnection as mongo
    return mongo.QueryDatabase()

def SortSensors(sensors):
    saved_sensors = {}

    for sensor in sensors:
        if sensor["sensor_name"] not in saved_sensors:
            saved_sensors[sensor["sensor_name"]] = []

        saved_sensors[sensor["sensor_name"]].append(sensor["sensor_value"])

    return saved_sensors

def BestHighway(highways):
    best_highway = None
    lowest_average_value = float('inf')

    for highway, sensor_data in highways.items():
        average_value = sum(sensor_data) / len(sensor_data)

        if average_value < lowest_average_value:
            lowest_average_value = average_value
            best_highway = highway

    return best_highway

def ListenOnTCP(tcpSocket: socket.socket, socketAddress):
    serverResponse = GetServerData()
    print("Received Data!")

    sortedSensors = SortSensors(serverResponse)

    print(sortedSensors)

    best_highway = BestHighway(sortedSensors)
    tcpSocket.send(best_highway.encode())

    tcpSocket.close()
    pass

def CreateTCPSocket() -> socket.socket:
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpPort = defaultPort
    print("TCP Port:",tcpPort)
    tcpSocket.bind(('localhost', tcpPort))
    return tcpSocket

def LaunchTCPThreads():
    tcpSocket = CreateTCPSocket()
    tcpSocket.listen(5)
    while True:
        connectionSocket, connectionAddress = tcpSocket.accept()
        connectionThread = threading.Thread(target=ListenOnTCP, args=[connectionSocket, connectionAddress])
        connectionThread.start()

if __name__ == "__main__":
    tcpThread = threading.Thread(target=LaunchTCPThreads)
    tcpThread.start()
    #
    # while not exitSignal:
    #     time.sleep(1)
    # print("Ending program by exit signal...")
