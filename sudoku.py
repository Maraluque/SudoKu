import numpy as np
import random
import globals
import pygame

class Sudoku:
    def __init__(self):
        self.dificultad = 0
        self.sudoku = np.zeros((9, 9), dtype=int)
        self.posibles = [[[] for _ in range(9)] for _ in range(9)]
        
    def copiar(self, a_copiar):
        self.sudoku = np.copy(a_copiar.sudoku)
        
    def calcular_posibles(self, mostrar=False):
        """
        Calcula los posibles valores para cada celda vacía del sudoku.

        Parámetros:
        - mostrar (bool): Indica si se deben mostrar los posibles valores en cada celda.

        """
        self.posibles = [[[] for _ in range(9)] for _ in range(9)]
        for fila in range(9):
            for columna in range(9):
                if self.sudoku[fila][columna] == 0:
                    self.posibles[fila][columna] = [numero for numero in range(1, 10) if self.es_posible(fila, columna, numero)]
                    if mostrar:
                        print(f"Posibles en [{fila}, {columna}]: {self.posibles[fila][columna]}")
                        
    def poner_valores_unicos(self):
        """
        Pone valores únicos en las celdas con un solo posible valor.

        """
        for fila in range(9):
            for columna in range(9):
                if len(self.posibles[fila][columna]) == 1:
                    print(f"Poniendo valor en [{fila}, {columna}]: {self.posibles[fila][columna][0]}")
                    self.sudoku[fila][columna] = self.posibles[fila][columna][0]
        self.calcular_posibles()

    def resolver_unicos(self):
        """
        Resuelve el sudoku colocando valores únicos en las celdas con un solo posible valor.

        Retorna:
        - cuantos (int): La cantidad de celdas resueltas en esta iteración.

        """
        cuantos = 0
        for fila in range(9):
            for columna in range(9):
                if len(self.posibles[fila][columna]) == 1:
                    self.sudoku[fila][columna] = self.posibles[fila][columna][0]
                    cuantos += 1
        return cuantos
                
    def resolver_sudoku(self, mostrar=False):
        """
        Resuelve el sudoku utilizando el método de resolución por eliminación de posibles valores.

        Parámetros:
        - mostrar (bool): Indica si se deben mostrar los posibles valores en cada iteración.

        Retorna:
        - Resuelto (bool): Indica si el sudoku ha sido resuelto.

        """
        self.calcular_posibles(mostrar)
        resolver = True

        while resolver:
            resolver = (self.resolver_unicos() != 0)
            if resolver:
                self.calcular_posibles(mostrar)
            
        resuelto = True
        for fila in range(9):
            for columna in range(9):
                if self.sudoku[fila][columna] == 0:
                    resuelto = False

        return resuelto
        
    def crear_sudoku(self, config):
        """
        Crea un nuevo sudoku con la configuración dada.

        Parámetros:
        - config (dict): Un diccionario que contiene la configuración del sudoku.

        Retorna:
        - sudoku (numpy.ndarray): El sudoku generado.
        - resuelto (numpy.ndarray): El sudoku resuelto.

        """
        self.calcular_posibles()
        self.intentar_poner_valor(0,0)

        casillas = []

        for fil in range(9):
            for col in range(9):
                casillas.append([fil,col])

        random.shuffle(casillas)

        resuelto = np.copy(self.sudoku)
    

        for [fila,columna] in casillas:
            s_aux = Sudoku()
            s_aux.copiar(self)
            s_aux.sudoku[fila][columna] = 0
            if s_aux.resolver_sudoku():
                self.sudoku[fila][columna] = 0
                self.calcular_posibles()

        if self.get_dificultad() == 0:
            for _ in range(7):
                fila, columna = random.choice(casillas)
                if self.sudoku[fila][columna] == 0:
                    self.sudoku[fila][columna] = resuelto[fila][columna]
        elif self.get_dificultad() == 2:
            for _ in range(int(config["dificil"])):
                fila, columna = random.choice(casillas)
                if self.sudoku[fila][columna] != 0:
                    self.sudoku[fila][columna] = 0
        return self.sudoku, resuelto

    def intentar_poner_valor(self, fila, columna):
        """
        Intenta poner un valor en la celda dada y continúa con el siguiente valor si no es posible.

        Parámetros:
        - fila (int): La fila de la celda.
        - columna (int): La columna de la celda.

        Retorna:
        - True si se pudo poner un valor en la celda, False de lo contrario.

        """
        valores_posibles = [1,2,3,4,5,6,7,8,9]
        random.shuffle(valores_posibles)

        for valor in valores_posibles:
            if valor in self.posibles[fila][columna]:
                self.sudoku[fila][columna] = valor
                self.calcular_posibles()

                siguiente_fila = fila
                siguiente_columna = columna + 1

                if siguiente_columna == 9:
                    siguiente_fila += 1
                    siguiente_columna = 0
                    if siguiente_fila == 9:
                        return True
                if self.intentar_poner_valor(siguiente_fila, siguiente_columna):
                    return True
                self.sudoku[fila][columna] = 0
                self.calcular_posibles()
        return False
        
    def es_posible(self, fila, columna, numero):
        """
        Verifica si es posible colocar un número en la celda dada sin violar las reglas del sudoku.

        Parámetros:
        - fila (int): La fila de la celda.
        - columna (int): La columna de la celda.
        - numero (int): El número a verificar.

        Retorna:
        - True si es posible colocar el número en la celda, False de lo contrario.

        """
        if numero in self.sudoku[fila] and columna != self.sudoku[fila].tolist().index(numero):
            return False
        if numero in [fila[columna] for fila in self.sudoku] and fila != [fila[columna] for fila in self.sudoku].index(numero):
            return False
        inicio_fila = (fila // 3) * 3
        inicio_columna = (columna // 3) * 3
        if numero in self.sudoku[inicio_fila:inicio_fila+3, inicio_columna:inicio_columna+3]:
            return False
        return True
    
    def backtracking(self, fila, columna):
        """
        Resuelve el sudoku utilizando el método de backtracking.

        Parámetros:
        - fila (int): La fila actual.
        - columna (int): La columna actual.

        Retorna:
        - True si el sudoku ha sido resuelto, False de lo contrario.

        """
        if fila == 9:
            return True
        
        if self.sudoku[fila][columna] != 0:
            if columna == 8:
                return self.backtracking(fila + 1, 0)
            else:
                return self.backtracking(fila, columna + 1)
        
        for num in range(1, 10):
            if self.es_posible(fila, columna, num):
                self.sudoku[fila][columna] = num
                
                if columna == 8:
                    if self.backtracking(fila + 1, 0):
                        return True
                else:
                    if self.backtracking(fila, columna + 1):
                        return True
                
                self.sudoku[fila][columna] = 0
        
        return False
    
    def set_dificultad(self, dificultad):
        """
        Establece la dificultad del sudoku.

        Parámetros:
        - dificultad (int): El nivel de dificultad del sudoku.

        """
        self.dificultad = dificultad

    def get_dificultad(self):
        """
        Retorna la dificultad del sudoku.

        """
        return self.dificultad