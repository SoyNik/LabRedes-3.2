import socket
import hashlib
import threading
import time
import datetime
import os

lock = threading.Lock()


def pedirDatos():
    fileName = ""
    fileT = ""
    entr = int(input("Ingrese archivo que quiere enviar 1 (100 MB) o 2 (250MB)"))
    if (entr == 1):
        fileName = "../Doc/Prueba4.mp4"
        fileT = ".mp4"
    elif (entr == 2):
        fileName = "../Doc/Prueba5.mp4"
        fileT = ".mp4"
    elif (entr == 3):
        print("Archivo de 11MB")
        fileName = "../Doc/Prueba3.pdf"
        fileT = ".pdf"
    entr = int(input("Ingrese el numero de clientes en simultaneo a enviar el archivo"))
    numClientes = entr
    return fileName, fileT, numClientes


tup = pedirDatos()
fileName = tup[0]
numClientes = tup[2]
fileT = tup[1]
numClientesC = 0
atender = False

host = ""
BUFF = 1024
port1=20001
# TCP ------> socket.AF_INET, socket.SOCK_STREAM
# UDP ------> socket.AF_INET, socket.SOCK_DGRAM
s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
s.bind((host, port1))

def servidor(dir):
    global numClientesC
    global atender

    numClientesC += 1
    print("Numero Clientes Conectados: ", numClientesC)
    sha1 = hashlib.sha1()
    while True:
        if (numClientesC >= numClientes or atender):
            print("Starting to send")
            break
    atender = True
    i = 0

    time.sleep(0.01)

    with open(fileName, 'rb') as f:
        # print("Starting to send")
        while True:
            i += 1
            data = f.read(BUFF)
            if not data:
                break
            sha1.update(data)

            s.sendto(data, dir)
        print("Archivo Enviado")

        # Envio de Hash
        has = str(sha1.hexdigest())
        s.sendto(("FINM" + has).encode(), dir)
        f.close()



while True:
    data = s.recvfrom(BUFF)
    dir = data[1]
    t = threading.Thread(target=servidor, args=(dir,))
    t.start()