import socket
import struct
import time
import threading

senderIP = "10.0.0.1"
senderPort   = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize  = 1024 #Message Buffer Size
# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

start_time = time.time()
file_name = open("testFile.jpg", 'rb')
seq = 0
win_st = 1
win_size = 256
curr_st = 1
data_list = {}
data_lt = 1
data = 1
data_list[0] = 1
while (data):
    data = file_name.read(1021)
    data_list[data_lt] = data
    data_lt+=1

def check_ack(msg,seq):
    if(msg>=seq):
        return 1
    else:
        return 0

def fun_recv():
    global win_st
    global curr_st
    global data_lt
    socket_udp.settimeout(0.5)
    while (win_st<data_lt):
        try:
            msgFromServer = socket_udp.recvfrom(bufferSize)
            recievedMessage = msgFromServer[0]
            senderAddress = msgFromServer[1]
            msg,eobf = struct.unpack("!H?",recievedMessage)
            # print("recd ",msg," number")
            if(check_ack(msg,win_st)):
                win_st=msg+1
                # print("change of win_st ",win_st)
        except:
            curr_st = win_st


thread_t = threading.Thread(target=fun_recv,args=())
thread_t.start()

while True:
    if(curr_st<win_st+win_size and curr_st<data_lt):
        mreq = struct.pack("!H?",curr_st,True)
        # print(curr_st,"sending")
        pckt =mreq + data_list[curr_st]
        socket_udp.sendto(pckt,recieverAddressPort)
        curr_st+=1
    if(win_st==data_lt):
        break


mreq = struct.pack("!H?",seq,False)
socket_udp.sendto(mreq, recieverAddressPort)
thread_t.join()
socket_udp.close()
file_name.close()
end_time = time.time()
print("Throughput is",(1172.316)/(end_time-start_time))
