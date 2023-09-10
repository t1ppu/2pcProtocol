import socket
from threading import Thread
import time
import logging
import traceback
import sys

host= '127.0.0.1'
port= 8000
NO_OF_PARTICIPANTS= 2
participant_list= [8002,8003]
timeout= 10


logging.basicConfig(filename="C://Users\kolli\OneDrive\Desktop/assignments\DS Project- 3/coordinator.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class coord():
    def __init__(self):
        self.vote_yes= 0
        self.ack= 0
        self.err= 0
        self.timeout= 30
        self.state= None

    def start(self):
        self.state= "voting"
        print("voting started")
        logger.info("VOTING STARTED.")
        try:
            sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
            sock.bind((host,port))
            sock.settimeout(10)
            for p in participant_list:
                #sock.connect((host,p))
                
                print("sending to ",host,p)
                msg= 'vote'
                sock.sendto(msg.encode(),(host,p))
        except socket.timeout:
            print("timeout")
            #sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #sock.bind((host,port))
        #sock.close()
        votes= 0
        #t_end = time.time() + self.timeout
        try:
            while votes!=NO_OF_PARTICIPANTS:  #and time.time()<t_end:
                msg, addr= sock.recvfrom(1024)
                #print("gg")
                self.handle_req(msg.decode())
                print(addr)
                votes+=1
            sock.close()
        except socket.timeout:
            print("timeout")
            self.abort(sock)
        logger.info("VOTES RECIEVED.")
        if votes==NO_OF_PARTICIPANTS and self.vote_yes==NO_OF_PARTICIPANTS:
                print("commit")
                logger.info("COMMIT REQUEST SENT!")
                sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.bind((host,port))
                sock.settimeout(10)
                msg="commit"
                for p in participant_list:
                    print("sending to ",host,p)
                    sock.sendto(msg.encode(),(host,p))
                    #sock.close()
                print("sent commit reqs")
                self.state= "commit"
                votes= 0
                #t_end = time.time() + self.timeout
                while votes!=NO_OF_PARTICIPANTS:  #and time.time()<t_end:
                    #client, addr= self.sock1.accept()
                    try:
                        msg, addr= sock.recvfrom(1024)
                        self.handle_req(msg.decode())
                        print(addr)
                        votes+=1
                    except socket.timeout:
                        print("timeout")
                        print("Did not recieve sufficient votes")
                        sock.close()
                        self.abort(sock)
                if votes==NO_OF_PARTICIPANTS and self.ack==votes:
                    print("all ack recieved -> committed.")
                    logger.info("ALL ACK RECIEVED. ACTION COMMITTED!")
                    sys.exit(0)
        else:
            sock.close()
            self.abort(sock)
    
        
    def abort(self,sock):
        self.vote_yes=0
        self.ack=0
        print("abort")
        logger.info("ABORTED!")
        #if self.state=='commit':
        sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host,port))
        for p in participant_list:
            print("sending to ",host,p)
            sock.sendto('abort'.encode(),(host,p))
        sock.close()
        #self.state= "abort"
        sys.exit()

    def handle_req(self, msg):
        print(msg,"from",end=' ')
        if msg.split()[0]=='yes':
            self.vote_yes+=1
        if msg.split()[0]=='ack':
            self.ack+=1

c= coord()
c.start()