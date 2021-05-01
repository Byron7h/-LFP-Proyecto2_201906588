# Este será nuestro objeto gramatica

class Gramatica:
    def __init__(self, nombre, no_terminales, terminales, s_inicial, producciones):
        self.nombre = nombre
        self.no_terminales = no_terminales
        self.terminales = terminales
        self.s_inicial = s_inicial
        self.producciones = producciones

    def getNombre(self):
        return self.nombre
    
    def getNo_Terminales(self):
        return self.no_terminales

    def getTerminales(self):
        return self.terminales

    def getS_inicial(self):
        return self.s_inicial

    def getProducciones(self):
        return self.producciones
        






    
