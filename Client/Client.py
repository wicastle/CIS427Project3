
import threading
import socket
import sys
import time


class service:
    user = ''
    john = False
    sally = False
    qiang = False
    root = False
    client = None

    def __init__(self):
        self.run()


    def receive(self):
        while True:
            try:
                msg = self.client.recv(1024).decode('utf-8')
                #print(msg)
                #check if message is a shutdown command
                if msg == 'SERVER: 200 OK SHUTDOWN':
                    self.client.close()
                    break
                else:
                    #check if message is a set ID check
                    try:
                        #print('herecheck')
                        check, x = msg.split(':', 1)
                        #print(check)
                        if check == 'ID':
                            #print('hereA')
                            self.user = x
                        else:
                            if check == 'AUSER':
                                #add user to current active
                                #print(x)
                                self.client.send(bytes(('REAUSER: ' + self.user), 'utf-8'))
                                if x == 'root':
                                    self.root = True
                                else:
                                    if x == 'john':
                                        self.john = True
                                    else:
                                        if x == 'sally':
                                            self.sally = True
                                        else:
                                            if x == 'qiang':
                                                self.qiang = True
                                #print(self.root)
                                #print(self.john)
                                #print(self.sally)
                                #print(self.qiang)
                            else:
                                if check == 'REAUSER':
                                    #readd user to current active
                                    #ment to catch existing users that have already logged in
                                    #print(x)
                                    if x == 'root':
                                        self.root = True
                                    else:
                                        if x == 'john':
                                            self.john = True
                                        else:
                                            if x == 'sally':
                                                self.sally = True
                                            else:
                                                if x == 'qiang':
                                                    self.qiang = True
                                else:
                                    if check == 'RUSER':
                                        #remove user from current active
                                        #print('hereC')
                                        if x == 'root':
                                            self.root = False
                                        else:
                                            if x == 'john':
                                                self.john = False
                                            else:
                                                if x == 'sally':
                                                    self.sally = False
                                                else:
                                                    if x == 'qiang':
                                                        self.qiang = False
                                    else:
                                        if check == 'MSG':
                                            #check if message is a confirm ID check
                                            target, str = x.split(':')
                                            #print(target)
                                            #print(str)
                                            #print(user)
                                            if self.user == target:
                                                #print('here')
                                                #send back a confirm
                                                #client.send(bytes('CONFIRM', 'utf-8'))
                                                #print str to client
                                                print('MSG from ' + target + ':')
                                                print(str)
                                        else:
                                            print(msg)
                    except:
                        print(msg)
            except:
                print("An Recevie Error Occurred!")
                print("Server is not responding as expected")
                self.client.close()
                break


    def write(self):
        while True:
            try:
                send = True
                msg = input("")
                try:
                    lhs, rhs = msg.split(' ', 1)
                    if lhs == 'MSG':
                        send = False
                        #check who target is and if they are a valid target / logged in
                        target, str = rhs.split(' ', 1)
                        if target == 'root':
                            if self.root is True:
                                send = True
                                print('SENT')
                            else:
                                print('root is not logged in')
                        else:
                            if target == 'john':
                                if self.john is True:
                                    send = True
                                    print('SENT')
                                else:
                                    print('john is not logged in')
                            else:
                                if target == 'sally':
                                    if self.sally is True:
                                        send = True
                                        print('SENT')
                                    else:
                                        print('sally is not logged in')
                                else:
                                    if target == 'quiang':
                                        if self.quiang is True:
                                            send = True
                                            print('SENT')
                                        else:
                                            print('quiang is not logged in')
                                    else:
                                        if target == '-all':
                                            #check if is the current root
                                            if self.user == 'root':
                                                #broadcast to everyone
                                                send = False
                                                self.client.send(bytes(('MSG root ' + str), 'utf-8'))
                                                time.sleep(0.1)
                                                self.client.send(bytes(('MSG john ' + str), 'utf-8'))
                                                time.sleep(0.1)
                                                self.client.send(bytes(('MSG sally ' + str), 'utf-8'))
                                                time.sleep(0.1)
                                                self.client.send(bytes(('MSG qiang ' + str), 'utf-8'))
                                            else:
                                                send = False
                                                print('Must be root to use -all')
                                        else:
                                            print(target + ' is not a user')
                except:
                    send = True
                        
                if send is True:
                    self.client.send(bytes(msg, 'utf-8'))
                if msg == 'SHUTDOWN':
                    break
            except:
                print("An Write Error Occurred!")
                print("Server is not responding as expected")
                break


    def run(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = '127.0.0.1'
        port = 55555
        self.client.connect((ip, port))
        #client.send("test hello")
        thread_r = threading.Thread(target=self.receive)
        thread_r.start()
        self.write()
        thread_r.join()




c = service()