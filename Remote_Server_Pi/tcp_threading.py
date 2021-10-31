import socket
import io
import PIL.Image as Image
import os
from _thread import *
from datetime import datetime

#IP address, port and buffersize
localIP     = ""
localPort   = 12345
bufferSize  = 4096

Dict = {'192.168.0.148':1,'192.168.0.101':2}

#Create TCP socket of type stream and bind
TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPServerSocket.bind((localIP, localPort))
TCPServerSocket.listen(5)

print("UDP server up and listening")
ThreadCount = 0
count = 0

def threaded_server(con,addr):
    global Dict
    global count

    #bytearray type variable to store pixel data
    arr_client = bytearray()
    chunk = 0
    while(True):

        #read data from socket recieved
        data = con.recv(bufferSize)

        #read new socket if recieved socket is empty or tx complete acknowledgement
        if not data or data == b'tx_complete':
            break

        else:
            chunk += 1
            arr_client.extend(data)
            
            
    print("chunks_received {}. Number of bytes {}".format(chunk, len(arr_client)))
    
    image = Image.open(io.BytesIO(arr_client))
    image.save('esp'+str(Dict[addr[0]]).zfill(2)+'_chn_1_'+str(datetime.now().strftime("%H.%M.%S"))+'.jpeg')

    con.close()



while(True):

    #accept connection from incoming socket
    con , addr = TCPServerSocket.accept()
    print("connected to : " +str(addr))

    #Number of chunks of data recieved per image
    start_new_thread(threaded_server, (con,addr, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))