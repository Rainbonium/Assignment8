import socket
import  json
import ipaddress
import threading
import time
import contextlib
import errno

maxPacketSize = 1024
defaultPort = 25552
serverIP = '127.0.0.1'

tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
try:
    tcpPort = int(input("Please enter the TCP port of the host..."))
except:
    tcpPort = 0
if tcpPort == 0:
    tcpPort = defaultPort
tcpSocket.connect((serverIP, tcpPort))

clientMessage = ""
while clientMessage != "exit":
    clientMessage = input("Please type the message that you'd like to send (Or type \"exit\" to exit):\n>")

    tcpSocket.send(clientMessage.encode())
    serverMessage = tcpSocket.recv(maxPacketSize).decode()

    responseMessage = json.loads(serverMessage)

    print("Best Highway: ", responseMessage["best_highway"])
    print("Average Time: ", responseMessage["lowest_average_value"])

tcpSocket.close()

