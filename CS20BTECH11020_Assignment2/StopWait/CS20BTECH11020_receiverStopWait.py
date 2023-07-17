import socket
import struct

recieverIP = "10.0.0.2"
recieverPort   = 20002
bufferSize  = 1024 #Message Buffer Size

# bytesToSend = str.encode(msgFromServer)

# Create a UDP socket
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind socket to localIP and localPort
socket_udp.bind((recieverIP, recieverPort))

print("UDP socket created successfully....." )
seq_num=0
f = open("output.jpg",'wb')

while True:
    bytesAddressPair = socket_udp.recvfrom(bufferSize)
    recievedMessage = bytesAddressPair[0]
    senderAddress = bytesAddressPair[1]
    header = recievedMessage[:3]
    seq,eobf = struct.unpack("!H?",header)
    if(eobf==False):
        print("data transmitted successfully")
        break
    elif(seq == seq_num):
        data = recievedMessage[3:]
        f.write(data)
        seq_num = (seq_num + 1)%2
        mreq = struct.pack("!H?",seq,True)
        socket_udp.sendto(mreq,senderAddress)
    else:
        mreq = struct.pack("!H?",seq,True)
        socket_udp.sendto(mreq,senderAddress)


socket_udp.close()
f.close()
