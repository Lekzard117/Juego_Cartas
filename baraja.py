import os

class Carta:
    PALOS = ['Corazones', 'Diamantes', 'Treboles', 'Picas']
    VALORES = ['As', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jota', 'Reina', 'Rey']


    def __init__(self, palo, valor, volteado = True):
        self.palo = palo
        self.valor = valor
        self.volteado = volteado

        self.frontal = self.cargar_frontal()
        self.reversa = self.cargar_reversa()

    def cargar_frontal(self):
        archivo = f"{self.valor}_de_{self.palo}.png".lower()
        ruta = os.path.join("cartas", archivo)
        if os.path.exists(ruta):
            return ruta
        else:
            raise FileNotFoundError(f"No se encontró la imagen para {self.valor} de {self.palo}: {ruta}")

    def cargar_reversa(self):
        ruta = os.path.join("cartas", "reverso.png")  # Ajusta según tu estructura
        if os.path.exists(ruta):
            return ruta
        else:
            raise FileNotFoundError(f"No se encontró la imagen de reversa: {ruta}")

    def voltear(self):
        self.volteado = not self.volteado

    def obtener_imagen(self):
        """
        Devuelve la ruta de la imagen según el estado de la carta.
        """
        return self.reversa if self.volteado else self.frontal

class Mazo:

    def __init__(self, mezclar = False):
        self.cartas = []
        for palo in Carta.PALOS:
            for valor in Carta.VALORES:
                self.cartas.append(Carta(palo, valor))
