


class clasificador:
    
    def __init__(self,tipoX,golpeX,filtroX,overfittingX,clfX,sel_atribX = "null",forzaX = "null",labelsX = "null"):
        print("Novo clasificador")
        self.tipo = tipoX
        self.golpe = golpeX
        self.filtro = filtroX
        self.overfitting = overfittingX
        self.clf = clfX
        self.sel_atrib = sel_atribX
        self.forza = forzaX
        self.labels = labelsX
 
    def equals(self,golpeX,tipoX=None,filtroX=None,overfitX=None):
        """
        Aceptamos:
        1)golpe
        2)golpe e tipo
        3)golpe,tipo,overfit e filtro
        """
        if tipoX is None and filtroX is None and overfitX is None:
            if self.golpe == golpeX:
                return True
            return False
        
        if filtroX is None and overfitX is None:
            if self.golpe == golpeX and self.tipo == tipoX:
                return True
            return False

        if self.tipo == tipoX and self.golpe == golpeX and self.filtro == filtroX and self.overfitting == overfitX:
            return True
        return False
