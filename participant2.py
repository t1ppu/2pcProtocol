import socket
import sys
from threading import Thread
import time
import logging
import traceback

host= '127.0.0.1'
port= 8003
last_transaction= None
timeout= 7
state= None

logging.basicConfig(filename="C://Users\kolli\OneDrive\Desktop/assignments\DS Project- 3/client2.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def startListening():
    sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host,port))
    sock.settimeout(10)
    state= "prepare"
    while True:
        try:
            #print(sock)
            msg, addr= sock.recvfrom(1024)
            msg= msg.decode()
            print(msg," req from ", addr)
            if msg=='vote':
                logger.info("VOTE REQUEST RECIEVED!")
                msg="no"
                if state=="prepare":
                    msg="yes"
                print("sent ", msg)
                sock.sendto(msg.encode(), tuple(addr))
                logger.info("VOTE SENT!")
            elif msg=='commit' or msg=='abort':
                logger.info(msg.upper()+" RECIEVED!")
                state= msg
                msg='ack'
                sock.sendto(msg.encode(), tuple(addr))
                print("ack sent")
                if state=='commit':
                    logger.info("COMMITTED THE OPERATION.")
                elif state=="abort":
                    logger.info("ABORTED THE OPERATION.")
                sys.exit(0)
        except socket.timeout:
            logger.info("TIMED OUT!")
            print("timeout")
            #sock= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #sock.bind((host,port))
            state= 'abort'
            #sock.close()

        time.sleep(2)

startListening()

