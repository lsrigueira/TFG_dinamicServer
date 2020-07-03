import function
import socket
import constant
import time

class usuario:
    def __init__(self ,remoto = False):
        print("Novo usuario")
        print(print([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]))
        self.mydb = function.basededatos()
        self.filtro = "nada"
        self.remoto = remoto
        if remoto == True:
            HOST = "192.168.0.5"
            PORT = 8888
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Socket created')
            try:
                s.bind((HOST, PORT))
            except socket.error as err:
                print("Bind failed. Error Code : ".format(err))
            s.listen(10)#Maximo 10 peticions
            print("Esperando conexion")
            self.conn, self.addr = s.accept()
            
        
    def setName(self,NameX):
        self.name = NameX

    def esperar(self ,donde = ""):
        if self.remoto:
            if donde == "login":
                data = self.conn.recv(1024).decode(encoding="UTF-8")
                print("RECIBIDO: "+data)
                return data
            else:    
                data = self.conn.recv(1024).decode(encoding="UTF-8")
                print("RECIBIDO: "+data)
                return int(data)
        elif donde == "menu":
            return function.menu(self.name)
        elif donde == "login":
            return input()
        else:
            return int(input())
    def enviar(self,data):
        """
        O metodo xa codifica,solo a string que desexa enviar debe ser enviada
        """
        if self.remoto:
            self.conn.send( (data+"\r\n").encode() )

    #Repeats the message until a valid number number is chosen,last parameter indicate if "0" is a valid number
    def eleccion(self,mensaxe,nparametros,haicero):
        """
        Repite a mensaxe ata que se selecciona un numero valido,o ultimo parametro indica se o "0" e valido
        """
        valido=0
        while valido is 0:
            try:
                print(mensaxe)
                devolver=self.esperar()
                if(haicero is True):
                    if(int(devolver) <=nparametros):
                        valido =1
                else:
                    if(int(devolver) <= nparametros and int(devolver)!= 0):
                        valido=1
            except:
                valido = 0
        #if self.remoto:
         #   self.conn.send("ok\r\n".encode())
        return devolver


        #Return all the hits we have clasifies, 0 if the list is empty and False if an invalid number has been chosen
    def elexir_golpes_clasificados(self,GolpesClasificados,Ceromessage):
        """
        Devolve todos os golpes clasificados, 0 se esta vacio e False se seleccionamos algo invalido
        """
        tamano=0
        print("-----------------------------------------")
        interaccion = 0
        while interaccion < len(GolpesClasificados):
            j=0
            while j < len(constant.GOLPES):
                i=0
                if function.abreviatura(constant.GOLPES[j]) == GolpesClasificados[interaccion]: #this is True if the hit is in GolpesClasificados(has been clasified)
                    print("\t"+str(tamano+1)+")"+constant.GOLPES[j])
                    tamano = tamano+1
                j=j+1
            interaccion=interaccion+1
        if tamano is 0:
            print("No hay registros de golpes clasificados,no puede entrenar asi")
            return -1
        else:
            print("\t0)"+Ceromessage)
            try:
                print("Escolla o golpe que desexa entrenar:")
                golpe = self.esperar()
            except:
                golpe=0
            if golpe > tamano:
                print("Operacion invalida")
                return False
        return golpe

    #Interactive menu to choose the hit+direction
    def seleccion_golpe(self):
        """
        Menu iteractivo para selecciona o golpe a direccion
        """
        print("Escolla un golpe:")
        invalido = True
        while invalido:
            invalido = False
            function.mostrar_golpes()
            golpe=input()
            try:
                golpe=constant.GOLPES[int(golpe)-1]
            except:
                print("Ha seleccionado un numero invalido")
                invalido = True
        print("Has seleccionado "+str(golpe))
        devolver = function.abreviatura(golpe)
        return devolver