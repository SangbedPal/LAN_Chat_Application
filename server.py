import socket
import threading
from time import sleep

SERVER_ADDRESS = ('localhost', 8080)
client_name_password = {}
client_name_public_key = {}
client_name_client_socket = {}

def get_client_information():
    file = open('client_information.txt')

    for line in file:
        line = line.rstrip('\n')

        client_information = line.split()
        name = client_information[0]
        password = client_information[1]
        public_key = client_information[2] + ',' + client_information[3]

        client_name_password[name] = password
        client_name_public_key[name] = public_key

    file.close()

def serve_client(client_socket, client_address):
    sign_in_or_sign_up = client_socket.recv(1024).decode('utf-8')

    if(sign_in_or_sign_up == 'Sign in'):
        verify_client(client_socket, client_address)
    else:
        register_new_client(client_socket)

def verify_client(client_socket, client_address):
    verification_result = 'Incorrect'

    while(verification_result == 'Incorrect'):
        name = client_socket.recv(1024).decode('utf-8')
        password = client_socket.recv(1024).decode('utf-8')

        print(name, password)
    
        for client_name in client_name_password:
            if(client_name == name):
                if(client_name_password[name] == password):
                    verification_result = 'Correct'

                break
        
        client_socket.send(verification_result.encode('utf-8'))

        print(verification_result)

    receive_and_send_messages(name, client_socket)

def register_new_client(client_socket):
    client_information = client_socket.recv(1024).decode('utf-8')
    client_information = '\n' + client_information

    file = open('client_information.txt', 'a')
    file.write(client_information)
    file.close()

def receive_and_send_messages(client_name, client_socket):
    sleep(5)

    client_name_client_socket[client_name] = client_socket

    information_of_other_clients = ''

    for name in client_name_password:
        if(name != client_name):
            information_of_other_clients += name + ':' + client_name_public_key[name] + ' '

    information_of_other_clients = information_of_other_clients.rstrip(' ')

    client_socket.send(information_of_other_clients.encode('utf-8'))
    
    print(information_of_other_clients)

    while(True):
        receiver_name_and_message = client_socket.recv(1024).decode('utf-8')

        index_of_first_space = receiver_name_and_message.index(' ')
        receiver_name = receiver_name_and_message[:index_of_first_space]
        message = receiver_name_and_message[index_of_first_space+1:]

        if(receiver_name != 'All'):
            receiver_socket = client_name_client_socket[receiver_name]
            receiver_socket.send((client_name + ' ' + 'Private' + ' ' + message).encode('utf-8'))
        else:
            for name in client_name_client_socket:
                if(name != client_name):
                    receiver_socket = client_name_client_socket[name]
                    receiver_socket.send((client_name + ' ' + 'Public' + ' ' + message).encode('utf-8'))

def main():
    global server_socket

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(10)

    get_client_information()

    while(True):
        client_socket, client_address = server_socket.accept()
        print('Connected with', client_socket, client_address)
        threading.Thread(target=serve_client, args=[client_socket, client_address]).start()

if(__name__ == '__main__'):
    main()