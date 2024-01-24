from concurrent.futures import thread
from email import message
import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)




client =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


# Enviar e receber nome para o servidor
while True:
    while True :
        try:
            nome = input("nome utilizador sem espaçamentos: ")
            if (' ' in nome)== False:
                break
        except:
            print("Erro")
            break
        else:
            continue

    client.send(nome.encode(FORMAT))
    
    m = client.recv(2048).decode(FORMAT)
    if m == "jaexiste":
        print("nome de utilizador ja em uso, introduza outro: ")   
    else:
        print(m)
        break
    
    
#enviar inputs para o sv
def enviar():
    while True:

        message =  input() 
        client.send(message.encode(FORMAT))

#receber mensagens do sv
def receber():
    while True:
        try:
            msg = client.recv(2048).decode(FORMAT)   
            print(msg)
        except:
            print("erro")
            client.close()
            break

receber_t = threading.Thread(target=receber)
receber_t.start()


enviar()

