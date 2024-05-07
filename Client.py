import socket
import  json
import ipaddress
import threading
import time
import contextlib
import errno

maxPacketSize = 1024
defaultPort = 25555
defaultIP = "localhost"

tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
try:
    tcpIP = input("Please enter the IP address of the host: ") or defaultIP
    tcpPort = int(input("Please enter the TCP port of the host: ")) or defaultPort
except:
    tcpIP = defaultIP
    tcpPort = defaultPort

tcpSocket.connect((tcpIP, tcpPort))

clientMessage = ""
while clientMessage != "exit":
    clientMessage = input("Please type the message that you'd like to send (Or type \"exit\" to exit):\n>")

    if clientMessage != "exit":
        tcpSocket.send(clientMessage.encode())
        serverMessage = tcpSocket.recv(maxPacketSize).decode()

        responseMessage = json.loads(serverMessage)

        print("Best Highway: ", responseMessage["best_highway"])
        print("Average Time: ", responseMessage["lowest_average_value"])

tcpSocket.close()

