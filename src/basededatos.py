from usuario import usuario
from clasificador import clasificador


class basededatos:
    clasificadores = []

    def __init__(self):
        print("Inicializando a base de datos")

    def addClf(self,golpeX,tipoX,filtroX,overfittingX,clfX,sel_atribX="null",forzaX="null",labelsX="null"):
        newclf = clasificador(tipoX,golpeX,filtroX,overfittingX,clfX,sel_atribX,forzaX,labelsX)
        self.clasificadores.append(newclf)

    def getclf(self,golpe,tipo=None,filtro=None,overfit=None):
        """
            Devolve o obxeto clf ou null se non existe
        """
        if tipo == None:
            i=0
            while i<len(self.clasificadores):
                if self.clasificadores[i].equals(golpe):
                    return self.clasificadores[i]
                i=i+1
            return "null"
        i=0
        while i<len(self.clasificadores):
            if self.clasificadores[i].equals(golpe,tipo,filtro,overfit):
                return self.clasificadores[i]
            i=i+1
        return "null"

    def contains(self,golpe,tipo=None,filtro=None,overfit=None):
        """
        Devolve un boolean,sin acabar de implementar
        """
        if tipo is None and filtro is None and overfit is None:
            i=0
            while i<len(self.clasificadores):
                if self.clasificadores[i].equals(golpe):
                    return True
                i+=1
            return False

        if  filtro is None and overfit is None:
            i=0
            while i<len(self.clasificadores):
                if self.clasificadores[i].equals(golpe,tipo):
                    return True
                i+=1
            return False

        i=0
        while i<len(self.clasificadores):
            #print(clasificador(self.clasificadores[i]))
            if self.clasificadores[i].equals(golpeX=golpe,tipoX=tipo,filtroX=filtro,overfitX= overfit):
                return True
            i+=1
        return False

    def updateClf(self,golpe,tipo,filtro,overfit,clf,sel_atrib,forza="null",labels="null"):
        """
        Returna un bolean co exito da operacion
        """
        resultado = self.getclf(golpe, tipo, filtro,overfit)
        if resultado == "null":
            return False
        resultado.clf = clf
        resultado.sel_atrib = sel_atrib
        if forza == "null" or labels == "null":
            return True
        resultado.forza = forza
        resultado.labels = labels
        return True