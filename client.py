import socket
import customtkinter
import tkinter
import threading
import rsa

SERVER_ADDRESS = ('localhost', 8080)
list_of_other_clients = []
client_name_public_key = {}

def connect_with_server():
    global client_socket 

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDRESS)

def open_sign_in_and_sign_up_window():
    global sign_in_and_sign_up_window

    sign_in_and_sign_up_window = customtkinter.CTk()
    sign_in_and_sign_up_window.geometry('500x300')
    sign_in_and_sign_up_window.title('Chat Application')

    sign_in_button = customtkinter.CTkButton(
        master=sign_in_and_sign_up_window,
        text='Sign in',
        command=open_sign_in_window
    )

    sign_in_button.pack(side=customtkinter.LEFT, anchor='e', padx=50)

    sign_up_button = customtkinter.CTkButton(
        master=sign_in_and_sign_up_window,
        text='Sign up',
        command=open_sign_up_window
    )

    sign_up_button.pack(side=customtkinter.LEFT, anchor='e', padx=50)

    sign_in_and_sign_up_window.mainloop()

def open_sign_in_window():
    global sign_in_window, sign_in_name, sign_in_password, number_of_sign_in_attempts

    sign_in_and_sign_up_window.destroy()
    number_of_sign_in_attempts = 0

    sign_in_window = customtkinter.CTk()
    sign_in_window.geometry('400x400')
    sign_in_window.title('Sign In Window')

    sign_in_name = customtkinter.CTkEntry(
        master=sign_in_window,
        width=250,
        placeholder_text='Enter your user name'
    )

    sign_in_name.pack(pady=50)

    sign_in_password = customtkinter.CTkEntry(
        master=sign_in_window,
        width=250,
        placeholder_text='Enter your Password'
    )

    sign_in_password.pack(pady=50)

    sign_in_button = customtkinter.CTkButton(
        master=sign_in_window,
        text='Sign in',
        command=verify
    )

    sign_in_button.pack(pady=50)

    client_socket.send('Sign in'.encode('utf-8'))

    sign_in_window.mainloop()

def open_sign_up_window():
    global sign_up_window, sign_up_name, sign_up_password

    sign_in_and_sign_up_window.destroy()

    sign_up_window = customtkinter.CTk()
    sign_up_window.geometry('400x400')
    sign_up_window.title('Sign Up Window')

    sign_up_name = customtkinter.CTkEntry(
        master=sign_up_window,
        width=250,
        placeholder_text='Enter your user name'
    )

    sign_up_name.pack(pady=50)

    sign_up_password = customtkinter.CTkEntry(
        master=sign_up_window,
        width=250,
        placeholder_text='Enter your Password'
    )

    sign_up_password.pack(pady=50)

    sign_up_button = customtkinter.CTkButton(
        master=sign_up_window,
        text='Sign up',
        command=register
    )

    sign_up_button.pack(pady=50)

    sign_up_window.mainloop()

def verify():
    global number_of_sign_in_attempts

    number_of_sign_in_attempts += 1

    name = sign_in_name.get()
    password = sign_in_password.get()

    client_socket.send(name.encode('utf-8'))
    client_socket.send(password.encode('utf-8'))

    print(name, password)
    
    verification_result = client_socket.recv(1024).decode('utf-8')

    print(verification_result)

    if(verification_result == 'Correct'):
        tkinter.messagebox.showinfo(message='Verification successful')
        sign_in_window.destroy()

        get_information_of_other_clients()
        create_chat_window(name)

        threading.Thread(target=receive_messages).start()

        chat_window.mainloop()
    else:
        if(number_of_sign_in_attempts < 5):
            tkinter.messagebox.showerror(message='Incorrect user name or password\n\n     Try again')

            sign_in_name.delete(0, 'end')
            sign_in_password.delete(0, 'end')
        else:
            tkinter.messagebox.showerror(message='Incorrect user name or password\n\nToo many sign in attempts')
            sign_in_window.destroy()

def register():
    client_socket.send('Sign up'.encode('utf-8'))

    name = sign_up_name.get()
    password = sign_up_password.get()
    e, n = generate_public_and_private_keys()

    information_to_be_sent_to_server = name + ' ' + password + ' ' + str(e) + ' ' + str(n)
    client_socket.send(information_to_be_sent_to_server.encode('utf-8'))

    tkinter.messagebox.showinfo(message='Your account has been created successfully')
    sign_up_window.destroy()

def generate_public_and_private_keys():
    p = rsa.choose_prime_number(10000000, 99999999)

    while(True):
        q = rsa.choose_prime_number(10000000, 99999999)

        if(q!=p):
            break

    n=p*q
    phi_n = rsa.phi(p, q)
    e = rsa.choose_e(phi_n)
    d = rsa.modular_multiplicative_inverse(e, phi_n)

    file = open('public_and_private_keys.txt', 'w')

    file.write(str(n) + '\n')
    file.write(str(e) + '\n')
    file.write(str(d))

    file.close()

    return e, n

def get_information_of_other_clients():
    information_of_other_clients = client_socket.recv(1024).decode('utf-8')
    list_of_information_of_other_clients = information_of_other_clients.split()

    for client_information in list_of_information_of_other_clients:
        name_public_key = client_information.split(':')

        name = name_public_key[0]
        public_key = name_public_key[1]

        client_name_public_key[name] = public_key
        list_of_other_clients.append(name)

    list_of_other_clients.append('All')

    print(client_name_public_key)
    print(list_of_other_clients)

def create_chat_window(client_name):
    global chat_window, private_chat_section, public_chat_section, type_message

    customtkinter.set_appearance_mode('dark')

    chat_window = customtkinter.CTk()

    screen_width = chat_window.winfo_screenwidth()
    screen_height = chat_window.winfo_screenheight()
    chat_window.geometry(f'{screen_width}x{screen_height}')

    chat_window.title('Chat Window')

    user_name = customtkinter.CTkLabel(
        master=chat_window,
        width=screen_width*0.12,
        height=screen_height*0.07,
        fg_color='transparent',
        text=client_name,
        text_color='white',
        font=('velvatica', 25)
    )

    user_name.place(relx=0.03, rely=0.28)

    public_chat_section = customtkinter.CTkScrollableFrame(
        master=chat_window,
        width=screen_width*0.3,
        height=screen_height*0.6,
        fg_color='#32a89d',
        label_text='Public Chats',
        label_font=('velvatica', 25)
    )

    public_chat_section.place(relx=0.21, rely=0.04)

    private_chat_section = customtkinter.CTkScrollableFrame(
        master=chat_window,
        width=screen_width*0.3,
        height=screen_height*0.6,
        fg_color='#32a89d',
        label_text='Private Chats',
        label_font=('velvatica', 25)
    )

    private_chat_section.place(relx=0.6, rely=0.04)

    type_message = customtkinter.CTkTextbox(
        master=chat_window,
        width=screen_width*0.5,
        height=screen_height*0.07,
        fg_color='white',
        text_color='black',
        font=('velvatica', 20)
    )

    type_message.place(relx=0.25, rely=0.75)

    send_to = customtkinter.CTkComboBox(
        master=chat_window,
        width=screen_width*0.1,
        height=screen_height*0.05,
        font=('velvatica', 25),
        values = list_of_other_clients,
        dropdown_font=('velvatica', 25),
        command=send_messages
    )

    send_to.place(relx=0.78, rely=0.75)

def send_messages(receiver_name):
    message = type_message.get(0.0, 'end')

    if(receiver_name != 'All'):
        e_and_n = client_name_public_key[receiver_name].split(',')
        e = int(e_and_n[0])
        n = int(e_and_n[1])

        encrypted_message = rsa.encrypt(message, e, n)
        client_socket.send((receiver_name + ' ' + encrypted_message).encode('utf-8'))

        label = customtkinter.CTkLabel(
            master=private_chat_section,
            corner_radius=15,
            text=f'You (to {receiver_name})\n\n{message}',
            justify='left',
            fg_color='white',
            text_color='black',
            font=('velvatica', 20)
        )

        label.pack(anchor='ne', pady=15)
    else:
        client_socket.send((receiver_name + ' ' + message).encode('utf-8'))

        label = customtkinter.CTkLabel(
            master=public_chat_section,
            corner_radius=15,
            text=f'You\n\n{message}',
            justify='left',
            fg_color='white',
            text_color='black',
            font=('velvatica', 20)
        )

        label.pack(anchor='ne', pady=15)

    type_message.delete(0.0, 'end')

def receive_messages():
    file = open('public_and_private_keys.txt')
    n_e_and_d = file.readlines()
    file.close()

    n = int(n_e_and_d[0].rstrip('\n'))
    d = int(n_e_and_d[2])

    while(True):
        sender_name_and_message = client_socket.recv(1024).decode('utf-8')

        index_of_first_space = sender_name_and_message.find(' ')
        sender_name = sender_name_and_message[:index_of_first_space]

        index_of_second_space = sender_name_and_message.find(' ', index_of_first_space+1)
        public_or_private = sender_name_and_message[index_of_first_space+1 : index_of_second_space]

        message = sender_name_and_message[index_of_second_space+1:]
        
        if(public_or_private == 'Private'):
            decrypted_message = rsa.decrypt(message, d, n)

            label = customtkinter.CTkLabel(
                master=private_chat_section,
                corner_radius=15,
                text=f'{sender_name}\n\n{decrypted_message}',
                justify='left',
                fg_color='white',
                text_color='black',
                font=('velvatica', 20),
            )

            label.pack(anchor='nw', pady=15)
        else:
            label = customtkinter.CTkLabel(
                master=public_chat_section,
                corner_radius=15,
                text=f'{sender_name}\n\n{message}',
                justify='left',
                fg_color='white',
                text_color='black',
                font=('velvatica', 20),
            )

            label.pack(anchor='nw', pady=15)

def main():
    connect_with_server()
    open_sign_in_and_sign_up_window()

if(__name__ == '__main__'):
    main()
