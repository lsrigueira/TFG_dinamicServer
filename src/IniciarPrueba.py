"""AQUI FALTACOLLER SEMPRE O SEL:ATRIB,SOLO SE COLLIA DENTRO DO IF E PETABA AS VECES POR ESO
"""

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict
from sklearn.feature_selection import SelectFromModel
from requests import get
import time
import socket
aux=time.time()

import numpy as np
from sklearn.model_selection import GridSearchCV
from collections import namedtuple
#import Controlar
import os
import xlsxwriter
import requests

import function
import constant
import usuario
from usuario import usuario
#############################################################PROGRAMA PRINCIPAL#############################################################
url = 'http://192.168.0.5:8000'
mac = 1130

Time=[]
Value=[]
GolpesClasificados=[]
resposta=123123
hits_database=[[]]

remoto = False
if(int(input("\nDesexa executar o programa en remoto ou local(Defecto)\n\r1)Remoto\n\r2)Local")) == 1):
    remoto = True
    ippublica = get('https://api.ipify.org').text
    ipprivada = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    myargs= {"MAC" : mac, "IPPrivada" : ipprivada, "IPPublica" : ippublica}
    requests.post(url,myargs)
    print("Enviados os datos")


user1 = usuario(remoto)
Constants = namedtuple('Constants', ['Back', 'Train_Algorithm', 'Train_Me','History','Data_Csv','Calibrate','Show_Vector','Configuration'])
constants = Constants(0, 1, 2, 3, 4, 5, 6, 7)
aux=time.time()-aux

#Inicializa todos los archivos(para permitirnos hacer un append) y pide un inicio de sesion
#devolviendo un False si el usuario sigue en modo anonimo
resposta=user1.eleccion("Desexa iniciar sesion?\n\t\t1)Si\n\t\t2)No",2,False)

if int(resposta) is 1: 
    print("Escriba o seu nome de usuario")
    username = user1.esperar("login")
    function.iniciosesion(username)
    user1.enviar("LogOk")
else: 
    print("Continuara en modo anonimo")
    username=False

function.iniciar(hits_database)

aux2=time.time()

#Controlador=Controlar.Controller()
user1.setName(username)
if user1.name is not False:
    #Leemos su .json para saber que golpes tiene en la base de datos y ensenhar solo eses en el modo practica
    GolpesClasificados.extend(function.cargarperfil(user1.name))
aux2=time.time()-aux2
print(aux+aux2)

while resposta!=0:
    #Le pasamos la sesion porque si es un usuario anonimo no puede acceder al menu completo.
    
    resposta = user1.esperar("menu")

    if int(resposta) is constants.Train_Algorithm:
        user1.enviar("ok")
        abreviatura=user1.eleccion(function.mostrar_golpes(),len(constant.GOLPES),False)
        if abreviatura not in GolpesClasificados:
            GolpesClasificados.append(abreviatura)
        interaccion = 0
        forza=[[]]
        tempos=[[]]
        calidade=[]
        repetir = True 
        if int(abreviatura) is 1:
            user1.enviar("etiquetar-crochet")
        else:
            user1.enviar("etiquetar-patada")    
        while repetir:
            #Controlador.main()
            
            auxy=function.readJSONS()
            FinalValues=auxy[1]
            FinalTimes=auxy[0]
            if interaccion is 0:
                forza[0]=FinalValues
                tempos[0]=FinalTimes
            else :
                forza.append(FinalValues)
                tempos.append(FinalTimes)
            valido=user1.eleccion(function.mostrar_direccions(),len(constant.DIRECCIONS),False)
            
            calidade.append(constant.DIRECCIONS[int(valido)-1])
            valido=user1.eleccion("Desex    a seguir clasificando?\n\t1)Si\n\t2)No",2,False)
            if int(valido) is 2:
                repetir = False
            interaccion=interaccion+1
        function.escribirJSON(abreviatura,user1.name,tempos=tempos,forza=forza,calidade=calidade)#opens "temporal.json" if there is no sesion
    #forza and calidade are optional values so we need to indicate what "forza" is.Its confusing in this case cause they have the same name

    elif int(resposta) is constants.Train_Me:
        user1.enviar("ok")      #confirmamos que chegou a mensaxe
        index_golpe = False     #One index to get the hit from GolpesClasificados(abrev already)
        
        while index_golpe is False:#index_golpe
            index_golpe=user1.elexir_golpes_clasificados(GolpesClasificados,"Atras")#This function return False if an invalid number has been chosen
         #Atras is the message that appears in position "0"
       
        if int(index_golpe) is -1 or int(index_golpe) is 0:#Function return -1 if the list is empty,0 if they want to go "atras"
            user1.enviar("back")
            continue#Its a "break" for the "elif"
        hitname=GolpesClasificados[int(index_golpe)-1]#to get the real hit name,(funcion menu starts at 1)
        repetir = True
        while repetir:
           #Controlador.main()
           forza=function.readJSONS()[1]
           if (not user1.mydb.contains(hitname) or user1.remoto): 
               user1.enviar("clasificadores")   
               aux=function.calibrar(user1,user1.name,hitname,False,False)
           clasificador=user1.mydb.getclf(hitname)
           print(clasificador.clf)
           clf_real = clasificador.clf
           sel_atrib = clasificador.sel_atrib
           auxyy = [[]]
           auxyy[0] = forza
           forza = auxyy
           pot = function.potencia(forza[0]) #We have to do it now,with the 135 values
           if "Linear" in str(clf_real):
                if not clasificador.overfitting:
                    forza = sel_atrib.transform(forza)
                    forza = function.reshapecasero(forza)
            
           elif clasificador.overfitting:
               print("VAMOS ATRANSFORMAR ESTO")
               forza = sel_atrib.transform(forza)
               forza = function.reshapecasero(forza)

           print(len(forza[0]))
           try:
                etiqueta = function.getresultado(forza[0],clf_real)[2:-2] #[2:-2]is jsut to deletede "['" and "']" to print
           except:
                print("Exception,using another algorithm")
                aux=function.calibrar(user1,user1.name,hitname,False,True)
                clf_real = aux[0]
                sel_atrib = aux[1]
                forza = sel_atrib.transform(forza)
                forza = function.reshapecasero(forza)
                etiqueta = function.getresultado(forza[0],clf_real)[2:-2]

           vectorhitname = function.ultimosgolpes(user1.name,hitname)
           vectoretiqueta = function.ultimosgolpes(user1.name,hitname,etiqueta)
           historialhitname = function.leerhistorial(hitname[:-4]) #Hitname e nombre_clf,no historial solo gardamos o nome
           historialetiqueta = function.leerhistorial(hitname[:-4],etiqueta)
           mediahitname = function.mediapot(vectorhitname,historialhitname)
           mediaetiqueta = function.mediapot(vectoretiqueta,historialetiqueta)
           print("\n-------------------------Resultados-------------------------")
           potenciagolpe = str(100*pot/mediahitname)
           potenciagolpetag = str(100*pot/mediaetiqueta)
           print("O golpe con potencia "+str(pot)+" foi "+str(etiqueta))
           print("\t"+potenciagolpe+"% de "+str(hitname[:-4]))
           print("\t"+potenciagolpetag+"% de "+str(hitname[:-4])+" "+str(etiqueta))
           index_enviar_golpe = potenciagolpe.find(".")
           if index_enviar_golpe is -1:
               index_enviar_golpe = 6
           index_enviar_tag = potenciagolpe.find(".")
           if index_enviar_tag is -1:
               index_enviar_tag = 6       

           print(str(round(pot))+","+potenciagolpe[:index_enviar_golpe]+"%,"+potenciagolpetag[:index_enviar_tag]+"%,"+str(etiqueta))
           user1.enviar(str(round(pot))+","+potenciagolpe[:index_enviar_golpe]+"%,"+potenciagolpetag[:index_enviar_tag]+"%,"+str(etiqueta))
           valido = user1.eleccion("Desexa seguir clasificando?\n\t1)Si\n\t2)No",2,False)
           if int(valido) is 2:
              repetir = False
           function.escribirJSON(str(time.gmtime(time.time())[3]+2)+"-"+str(time.gmtime(time.time())[4]),"historial",string="Nombre:"+hitname[:-4]+"\n\t\t\tPotencia:"+str(pot)+"\n\t\t\tCalificacion:\""+str(etiqueta)+"\"")

    elif int(resposta) is constants.History:
        #Ensenhamos el historial de golpes del runtime
        user1.enviar("ok")
        alldata = function.verhistorial()
        print(alldata)
        justNow = ( "18:16,Cro,53451.89279,Derecha,;"
                    "18:16,Pat,33721.32414,Izquierda,;"
                    "18:17,Cro,61592.19533,Izquierda,;"
                    "18:17,Pat,46724.38465,Derecha,;"
                    "18:17,Cro,72363.24735,Derecha,;"
                    "18:17,Pat,34612.36728,Izquierda,;"
                    "18:17,Cro,33277.98598,Izquierda,;"
                    "18:18,Pat,24515.26958,Derecha,;"
                    "18:18,Cro,32523.26898,Derecha,;"
                    "18:18,Pat,45673.25842,Izquierda,;"
                    "18:18,Cro,29703.12352,Izquierda,;")
        
        user1.enviar(justNow)

    elif int(resposta) is constants.Data_Csv:
        #Se crean <nombreusuario>_<nombregolpe>.xlsx en el path indicado
        # en "constant.py" que contiene el vector de cada golpe asi como su etiqueta y potencia
        function.getexcel(user1.name + ".json")

    elif int(resposta) is constants.Calibrate:
        user1.enviar("ok")
        index_golpe = False#One index to get the hit from GolpesClasificados(abrev already)
        while index_golpe is False:#index_golpe
            index_golpe=user1.elexir_golpes_clasificados(GolpesClasificados,"Todos")#This function return False if an invalid number has been chosen
        if int(index_golpe) is -1:#Function return -1 if the list is empty
            continue#Its a "break" for the "elif"
        #NOTA,SE PULSAN 0 HAI QUE CALIBRAR TODOS FALTAN POR IMPLEMENTAR ESAS COUSAS
        hitname=GolpesClasificados[int(index_golpe)-1]#to get the real hit name,(funcion menu starts at 1)
        user1.enviar("Clasificadores")   
        aux=function.calibrar(user1,user1.name,hitname,True,False)
        clf=aux[0]
        sel_atrib=aux[1]

    elif int(resposta) is constants.Show_Vector:
        index_golpe=False
        while index_golpe is False:
           index_golpe=user1.elexir_golpes_clasificados(GolpesClasificados,"Atras")#This function return False if an invalid number has been chosen
        if int(index_golpe) is -1 or 0:   #Function return -1 if the list is empty,0 if they want to go "atras"
           continue
        hitname=GolpesClasificados[int(index_golpe)-1]#to get the real hit name,(funcion menu starts at 1)
        decide=user1.eleccion("Con ou Sin overfitting?\n\t1)Sin Overfitting\n\t2)Con Overfitting",2,False)
        if int(decide) is 2:
            print("Decidido con overfitting")
            if user1.mydb.contains(hitname,"LinearSVC","nada",True):
                function.pintarvectoresTSNE(user1.name,hitname)
            else:
                print("Non existen clasificadores dese tipo")
        else:
            print("Decidido sin overfitting")
            if user1.mydb.contains(hitname,"LinearSVC","nada",False):
                clasificador=user1.mydb.getclf(hitname,"LinearSVC","nada",False)
                function.pintarvectoresTSNE(user1.name,hitname,clasificador.sel_atrib)
            else:
                print("Non existen clasificadores dese tipo")

    elif int(resposta) is constants.Configuration:
            valido=user1.eleccion("Que desexa modificar?\n\t1)Filtros\n\t0)Salir",1,True)
            if int(valido) is 0:
                continue
            elif int(valido) is 1:
                newfiltro=user1.eleccion(
                    """Que filtro desexa usar?\n\t1)Nada\n\t2)Normal\n\t3)deletevibration
                    4)reducepot""",4,False)
                if int(newfiltro) is 1:
                    user1.filtro = "nada"
                elif int(newfiltro) is 2:
                    user1.filtro = "normal"
                elif int(newfiltro) is 3:
                    user1.filtro = "deletevibration"
                elif int(newfiltro) is 4:
                    user1.filtro = "reducepot"


    elif int(resposta) is 8:
        index_golpe = False     #One index to get the hit from GolpesClasificados(abrev already)
        while index_golpe is False:#index_golpe
            index_golpe=user1.elexir_golpes_clasificados(GolpesClasificados,"Atras")#This function return False if an invalid number has been chosen
            #Atras is the message that appears in position "0"
        if int(index_golpe) is -1 or 0:#Function return -1 if the list is empty,0 if they want to go "atras"
            continue#Its a "break" for the "elif"
        hitname=GolpesClasificados[int(index_golpe)-1]#to get the real hit name,(funcion menu starts at 1)
        vectorfinal= function.valueandlabels(user1.name+".json",hitname,True)
        aux=vectorfinal[0]
        todosvalues=aux[0:int(len(aux)/2)]
        todoslabels=aux[int(len(aux)/2):]
        todostimes=vectorfinal[1]
        i=0
        finaltimes=[[]]
        finalvalues=[[]]
        while i <len(todosvalues):
            if todoslabels[i]=="Derecha":
                todoslabels[i]="Dereita"
            elif todoslabels[i]=="Izquierda":
                todoslabels[i]="Esquerda"
            finalvector=function.reducepot(todostimes[i],todosvalues[i])
            if i is 0:
                finaltimes[0]=finalvector[0:int(len(finalvector)/2)]
                finalvalues[0]=finalvector[int(len(finalvector)/2):]
            else:
                finaltimes.append(finalvector[0:int(len(finalvector)/2)])
                finalvalues.append(finalvector[int(len(finalvector)/2):])
            i=i+1

        function.escribirJSON(hitname,"prueba3",tempos=finaltimes,forza=finalvalues,calidade=todoslabels)

        """aux=function.valueandlabels("prueba3.json",hitname,True)
        auxvect=aux[0]
        values = auxvect[0:int(len(auxvect) / 2)]
        labels = auxvect[int(len(auxvect) / 2):int(len(auxvect))]
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print(values)
        print(labels)
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print(aux[1])
        print(len(aux[1]))
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        """
        """AQUI XA TEnhO TODOS OS DATOS QUE NECESITARIA PARA PROCESAR
        
        """
        """ESTO ERA PARA A PRUEBA DE CAMBIAR O MAXIMO VALOR DO EJE
        index_golpe = False
        while index_golpe is False:
            index_golpe = function.elexir_golpes_clasificados(GolpesClasificados,
                                                              "Atras")  # This function return False if an invalid number has been chosen
        if int(index_golpe) is -1 or 0:  # Function return -1 if the list is empty,0 if they want to go "atras"
            continue
        hitname = GolpesClasificados[int(index_golpe) - 1]  # to get the real hit name,(funcion menu starts at 1)
        function.cambiaramaximo(sesion,hitname,"prueba2")
        """
        """Esto era para a minha prueba de contar o signo
        
        NOTA, E SE FACEMOS O DE AHORA PERO CONTANDO TODOS OS SIGNOS?
        
        index_golpe = False
        while index_golpe is False:
            index_golpe = function.elexir_golpes_clasificados(GolpesClasificados,
                                                              "Atras")  # This function return False if an invalid number has been chosen
        if int(index_golpe) is -1 or 0:  # Function return -1 if the list is empty,0 if they want to go "atras"
            continue
        hitname = GolpesClasificados[int(index_golpe) - 1]  # to get the real hit name,(funcion menu starts at 1)
        print("\t1)Contamos o signo das mostras de cada eixe de cada acelerometro e ponhemos a 0 as do signo minoritario")
        print("\t2)Contamos o signo das mostras de cada eixe e ponhemos a 0 os eixes completos")
        aux=input()
        if int(aux) is 1:
            print("Elexida opcion 1")
            eleccion="muestrascero"
        else:
            print("Elexida opcion 2")
            eleccion="ejecero"
        function.cambiarjsons(sesion,hitname,"prueba1",eleccion)
        """


    elif int(resposta) is 15:#U wont see 15 in menu, but return 15
           print("Escriba o seu nome de usuario")
           user1.name = user1.esperar("login")
           function.iniciosesion(user1.name)
           GolpesClasificados.extend(function.cargarperfil(user1.name))

    elif int(resposta) is constants.Back:
             with open(constant.PATH+"temporal.json",'a') as temporal_file:
                 temporal_file.write("}")
             with open(constant.PATH+"historial.json",'a') as temporal_file:
                 temporal_file.write("}")
             print("PROGRAMA REMATADO CON EXITO")


    else :
        print("Opcion non valida\n")
