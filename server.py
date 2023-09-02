import socket
import select
from _thread import *
import sys
# List to record all the connected clients
clients = []
clientNames = []
# Method that handle multiple clients
f = open("server.log", "w")
def threaded(c):
    f = open("server.log", "a")
    # infinite loop to receive messages
    try:
        while True:
            f = open("server.log", "a")            
            # Receive messsage from clients
            data = c.recv(2048)            
            # Print message on server screen as log
            print(data.decode('utf-8'))
            f.write(data.decode('utf-8'))
            f.close()
            # Loop to iterate over clients List
            for client in clients:   
                if client != c:
                    # Send message to all other clients
                    #take out if statement if you want to also print username to the client who is messaging
                    client.send(data)
    #when a client has left print a message to all clients
    except socket.error as e:
        for i in range(len(clients)):
            try:
                if clients[i] == c:
                    print(clientNames[i], " has left.")
                    f.write(clientNames[i] + " has left.\n")
                    left = clientNames[i]
                    clients.remove(clients[i])
                    clientNames.remove(clientNames[i])
                    f.close()
                    for j in range(len(clients)):
                        clients[j].send((left + " has left.").encode('ascii'))
            except:
                continue
# Main method
def Main():
    
    # Define localhost
    host = "127.0.0.1"
     
    # takes first argument from command prompt as port number
    try:
        port = int(sys.argv[1])
    except:
        print("username,hostname or port is missing")
    
    # Set TCP socket for connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind with IP and Port
    s.bind((host, port))
    print("socket binded to port", port)

    # Start listening at the same IP and port
    s.listen(5)
    print("socket is listening")
    while True:
        try:
            while True:
                # Accept connection from client
                c, addr = s.accept()
                f = open("server.log", "a")
                # Print connected client IP and port
                print('Connected to :', host, ':', port)
                f.write('Connected to :' + str(host) + ':' + str(port) + "\n")
                # Push the connected client to list
                clients.append(c)
                # Received connected client name
                clientName = c.recv(2048)
                print(clientName.decode('utf-8') + " has joined.")
                f.write(clientName.decode('utf-8') + " has joined.\n")
                f.close()
                #prints it to all clients
                for client in clients:
                    if client != c:
                        client.send(clientName + " has joined.".encode('ascii'))
                # Push the names in list
                clientNames.append(clientName.decode('utf-8'))                        
                # Start new thread for new client
                start_new_thread(threaded, (c,))
        except socket.error as e:
            print("Server Crashed: " + e)
            f.write("Server malfunction")
            f.close()
        finally:
            s.close()



if __name__ == '__main__':
    Main()
