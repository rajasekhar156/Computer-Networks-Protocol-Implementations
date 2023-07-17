import socket
import struct
import time

senderIP = "10.0.0.1"
senderPort   = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize  = 1024 #Message Buffer Size

# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#filename = input("Please enter data file name to send: ")
start_time = time.time()
file_name = open("testFile.jpg", 'rb')
data = file_name.read(1021)
seq = 1
temp = 0
num_of_retrans = 0

def seq_fun(seq):
    if(seq==1):
        seq = 0
    else:
        seq = 1
    return seq

def check_ack(msg,seq):
    if(msg==seq):
        return 1
    else:
        return 0

seq = seq_fun(seq)
mreq = struct.pack("!H?",seq,True)
data=mreq+data


while True:
    socket_udp.sendto(data, recieverAddressPort)
    socket_udp.settimeout(0.1)
    while True:
        try:
            msgFromServer = socket_udp.recvfrom(bufferSize)
            recievedMessage = msgFromServer[0]
            senderAddress = msgFromServer[1]
            msg,eobf = struct.unpack("!H?",recievedMessage)

            if(check_ack(msg,seq)):
                break
        except:
            num_of_retrans+=1
            socket_udp.sendto(data, recieverAddressPort)

    data = file_name.read(1021)
    if(data):
        seq = seq_fun(seq)
        mreq = struct.pack("!H?",seq,True)
        data=mreq+data
    else:
        break

mreq = struct.pack("!H?",seq,False)
socket_udp.sendto(mreq, recieverAddressPort)
socket_udp.close()
file_name.close()
end_time = time.time()
print("Number of retransmissions happend",num_of_retrans)
print("Throughput is ", (1172.316) / (end_time-start_time))
