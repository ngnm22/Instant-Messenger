import socket
from _thread import *
state = 0
import sys
# Method to receive message at any time
def threaded(c):
    while True:
        
        # Receive messages
        try:
            data = c.recv(2048)
            print(str(data.decode('ascii')))
        # if you cant receive messages anymore:
        except:
            print("server is no longer available")
            f = open("server.log", "a")
            f.write("Server malfunction")
            f.close()
            return(state == False)
def Main():
    try:
        state_2 = True
        try:
            # takes the first argument from command prompt as IP address
            username = str(sys.argv[1])
            # takes the first argument from command prompt as IP address
            host = str(sys.argv[2])
             
            # takes second argument from command prompt as port number
            port = int(sys.argv[3])
        except:
            state_2 = False
        # Set TCP socket for connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect with server on same IP and port
        try:
            s.connect((host, port))
        except:
            #if the issue is mistmatch:
            if state_2 == True:
                print("host name/port number doesnt match server\n")
                print("exiting chat...")
                f = open("server.log", "a")
                f.write("host name didnt match server")
                f.write("exited chat")
                f.close()
            #if issue is missing username:
            else:
                f = open("server.log", "a")
                f.write("username,hostname or port is missing try again")
                f.close()
                print("username,hostname or port is missing try again")
                
            return(state == False)
        
        # Start thread to receive messages
        start_new_thread(threaded, (s,))
        while True:
            # send Username to server
            s.send((username).encode('utf-8'))
            
            # Print welcome message on screen
            print("Welcome to Chat application\n\n")
            while True:
                
                # Prompt for the new message
                message = input()
                
                # Send message with username to server
                s.send((username+": "+message+"\n").encode('ascii'))
    #if user crashes:
    except socket.error:
        if state != False:
            print(username + " has left.")
            s.send((username+":has left\n").encode('ascii'))  
    finally:
        s.close()


if __name__ == '__main__':
    Main()
