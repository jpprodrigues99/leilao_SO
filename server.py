from concurrent.futures import thread
from http import client
import socket
import threading
import time
from traceback import print_tb

HEADER = 64 #TAMANHO DE BYTES
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

Clients=[]
Nomes=[] 

nome_prod=""
valor_prod=''
leilao_ativa=False
ultimo_licitador = ""
nmr_util = 0
estado_licitacao = False


def broadcast(msg):
    for client in Clients:
        client.send(msg.encode(FORMAT))


def handle_client(conn,addr):
    global leilao_ativa
    global nmr_util
    global ultimo_licitador
    try:
        
        while True:
            
            nome = conn.recv(2048).decode(FORMAT) #receber nome

            estado_nome = True
            for nome_u in Nomes:
                if nome == nome_u:
                    conn.send("jaexiste".encode(FORMAT))
                    estado_nome = False
                    break
            if estado_nome == True:
                
                break
       
           
        Nomes.append(nome)
        Clients.append(conn)
        
        
        print(f"[NOVA CONECCAO] {addr} {nome} conectou-se!")
        conn.send("conectado ao sv".encode(FORMAT))
        broadcast(f"\n{nome} conectou-se!")
        #enviar mensagem para o cliente se o leilao foi aberto antes de ele introduzir o nome
        if leilao_ativa == True:
            conn.send(f"\nlicitacao de {nome_prod} no valor inical de {valor_prod} € digite a sua: ".encode(FORMAT))
        

    except:        
        conn.close()
        return
    
    while True:
        
        try:
            msg = conn.recv(2048).decode(FORMAT)#converte para bytes de quantos ira receber da mensagem       
            if leilao_ativa==False:    
                conn.send("Nenhum leilão ativo".encode(FORMAT))
            if leilao_ativa==True:                
                licitacao(conn,msg)
                
        except:
            index=Clients.index(conn)
            nome = Nomes[index]

            Clients.remove(conn)
            conn.close()
            broadcast(f"{nome} saiu!")
            print(f"{nome} saiu!")
            Nomes.remove(nome)
            nmr_util -= 1 
            ultimo_licitador=""
            break




def start():
    
    global nmr_util
    server.listen()

    while nmr_util <20:
        
        conn, addr = server.accept()#addr é o endereço da pessoa

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[coneccoes ativas - ]{threading.active_count()-2}")
        nmr_util += 1 
        print(nmr_util) 
        


def menu():
    global leilao_ativa
    global nome_prod 
    global valor_prod
    

    nome_prod = input("indique o nome do produto: ")
    
    valor_prod = int(input("indique o valor de inicio da licitacao: "))
    leilao_ativa=True
    broadcast(f"licitacao de {nome_prod} no valor inical de {valor_prod} € digite a sua: ")
    
    while True:

        if estado_licitacao== True:
            finalizar()   
            if leilao_ativa == True:
                continue
            else: 
                break
        else:
            continue 

#print("[A iniciar...]")

def licitacao(conn,msg):
    index = Clients.index(conn)
    nome = Nomes[index]
    global valor_prod
    global ultimo_licitador
    global estado_licitacao

    try:
        int(msg)
        if int(msg) <= valor_prod:
            conn.send("valor invalido".encode(FORMAT))
        else:
            if ultimo_licitador == nome:
                conn.send("nao pode licitar 2x seguidas".encode(FORMAT))
            else:
                valor_prod= int(msg)
                ultimo_licitador = nome
                estado_licitacao = True
                broadcast(f"{nome} licitou {valor_prod} para {nome_prod}")   
    except:
        conn.send("nao e um numero".encode(FORMAT))    

def ficheiroexterno(ultimo_licitador, nome_prod, valor_prod):
    f = open("historico.txt", "a")
    f.write (f"{ultimo_licitador} ganhou a licitacao de: {nome_prod} no valor de: {valor_prod}\n")
    f.close()
    

def finalizar():
    global ultimo_licitador
    global estado_licitacao
    global leilao_ativa

    if estado_licitacao == True:
        estado_licitacao = False
        if estado_licitacao == False:
            time.sleep(5)
            if estado_licitacao==False:
                time.sleep(7)
                if estado_licitacao==False:
                    broadcast("Vai um...")
                    time.sleep(3)
                    if estado_licitacao==False:
                        broadcast("E vão duas...")
                        time.sleep(3)
                        if estado_licitacao==False:
                            broadcast("E vão tres...")
                            broadcast(f"{nome_prod} vendido(a) a {ultimo_licitador} por {valor_prod} €")
                            ficheiroexterno(ultimo_licitador,nome_prod,valor_prod)
                            leilao_ativa=False
                            menu()
                            ultimo_licitador = ""

thread_start = threading.Thread(target=start)
thread_start.start()

menu()
