#server_chat.py allows multiple client to connect
#Sushmitha Shridhar
import select, socket, sys, pdb
from util_chat import ChatHall, Room, ChatMember
import util_chat

READ_BUFFER = 1000

listensocket = util_chat.create_socket(('127.0.0.1', 5005))
#return object
serversocket=listensocket
chat_hall_list = ChatHall()
connection_list = []
connection_list.append(listensocket)
#all sockets, server socket, 
#appending client socket

while True:
    
    read_players, write_players, error_sockets = select.select(connection_list, [], [])
   

	    
    for member in read_players:
        #if there are multiple items, add 10 clients, listen sockets, if
        if member is listensocket: 
            #when you recieve a message in connection_list, it will not be there in listensocket,
            #hence it goes to else and adds message from the client socket
            new_socket, add = member.accept()
            #accept client's who is trying to connect, store socket connection of the new client, add client's PORT
            new_member = ChatMember(new_socket)
            #create ChatMember object and initialize all the values, set socket as new socket
            connection_list.append(new_member)
            #append chat member object to the  connection_list
            chat_hall_list.welcome_new(new_member)
            #call the function welcome_new in the class ChatHall()
	
        else: # new message
            msg = member.socket.recv(READ_BUFFER)
	        #particular clients socket message
	    if not msg:
		chat_hall_list.remove_member(member)
            if msg:
                msg = msg.decode().lower()
                chat_hall_list.msg_handler(member, msg)
            else:
                member.socket.close()
                connection_list.remove(member)
            
    
    
    for sock in error_sockets: # close error sockets
        sock.close()
        connection_list.remove(sock)

