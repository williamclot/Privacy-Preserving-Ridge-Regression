import numpy as np
import socket, pickle
import struct


class members:
    CSP = {"ip": "172.18.0.23", "port": 5000}
    Evaluator = {"ip": "172.18.0.22", "port": 5001}
    Users = {"ip": "172.18.0.24", "port": 5002}

class termcol:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class utils:
    def ParseToFile(self, List, destination):
        """Parses List to destination file (one element per line)"""
        file = open(destination, "w")
        for element in np.nditer(List):
            #file = file / 10^7
            file.write(str(np.round(element, 2))+'\n')
        file.close

    # def recvall(self, sock, count):
    #     buf = b''
    #     while count:
    #         newbuf = sock.recv(count)
    #         if not newbuf: return None
    #         buf += newbuf
    #         count -= len(newbuf)
    #     return buf

    # def send_one_message(self, sock, data):
    #     length = len(data)
    #     sock.sendall(struct.pack('!I', length))
    #     sock.sendall(data)

    # def recv_one_message(self, sock):
    #     lengthbuf = self.recvall(sock, 4)
    #     length, = struct.unpack('!I', lengthbuf)
    #     return self.recvall(self, sock, length)
    
    def sendViaSocket(self, party, object, description=""):
        '''Client side -- Sends pickled object to party'''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Dealing with a client trying to connect to a server that hasn't been initated yet
        connected = False
        while not connected:
            try:
                s.connect((party['ip'], party['port']))
                connected = True
            except Exception as e:
                pass #Do nothing, just try again

        # Pickling the data into a binary object
        pickled = pickle.dumps(object)
        # Send the pickled object
        s.send(pickled)
        print(termcol.OKBLUE+description+termcol.ENDC)
        s.close()

    def receiveViaSocket(self, party, description=""):
        '''Server side -- Waits and receives pickled object'''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((party['ip'], party['port']))
        s.listen(1)
        conn, addr = s.accept()
        data = []

        while True:
            packet = conn.recv(4096)
            if not packet: break
            data.append(packet)
        
        pickled=b"".join(data)
        object = pickle.loads(pickled)
        print(termcol.OKBLUE+description+termcol.ENDC)
        s.close()
        return object

