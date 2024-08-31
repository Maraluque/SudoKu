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
        self.posibles = [[[] for _ in range(9)] for _ in range(9)]
        for fila in range(9):
            for columna in range(9):
                if self.sudoku[fila][columna] == 0:
                    self.posibles[fila][columna] = [numero for numero in range(1, 10) if self.es_posible(fila, columna, numero)]
                    if mostrar:
                        print(f"Posibles en [{fila}, {columna}]: {self.posibles[fila][columna]}")
                        
    def poner_valores_unicos(self):
        # Poner valores únicos en las celdas con un solo posible
        for fila in range(9):
            for columna in range(9):
                if len(self.posibles[fila][columna]) == 1:
                    print(f"Poniendo valor en [{fila}, {columna}]: {self.posibles[fila][columna][0]}")
                    self.sudoku[fila][columna] = self.posibles[fila][columna][0]
        self.calcular_posibles()

    def resolver_unicos(self):
        cuantos = 0
        for fila in range(9):
            for columna in range(9):
                if len(self.posibles[fila][columna]) == 1:
                    self.sudoku[fila][columna] = self.posibles[fila][columna][0]
                    cuantos += 1
        return cuantos
                
    def resolver_sudoku(self, mostrar=False):
        self.calcular_posibles(mostrar)
        resolver = True

        while resolver:
            resolver = (self.resolver_unicos() != 0)
            if resolver:
                self.calcular_posibles(mostrar)
            
        Resuelto = True
        for fila in range(9):
            for columna in range(9):
                if self.sudoku[fila][columna] == 0:
                    Resuelto = False

        return Resuelto
        
    def crear_sudoku(self, config):
        # Dificultad 0: Fácil (por defecto), 1: Media, 2: Difícil
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


        # Elección de dificultad
        if self.dificultad == 0:
            for _ in range(7):
                fila, columna = random.choice(casillas)
                if self.sudoku[fila][columna] == 0:
                    self.sudoku[fila][columna] = resuelto[fila][columna]
        elif self.dificultad == 2:
            for _ in range(int(config["dificil"])):
                fila, columna = random.choice(casillas)
                if self.sudoku[fila][columna] != 0:
                    self.sudoku[fila][columna] = 0
        return self.sudoku, resuelto

    def intentar_poner_valor(self, fila, columna):
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
        # Verificar fila
        if numero in self.sudoku[fila] and columna != self.sudoku[fila].tolist().index(numero):
            return False
        # Verificar columna
        if numero in [fila[columna] for fila in self.sudoku] and fila != [fila[columna] for fila in self.sudoku].index(numero):
            return False
        # Verificar cuadrado 3x3
        inicio_fila = (fila // 3) * 3
        inicio_columna = (columna // 3) * 3
        if numero in self.sudoku[inicio_fila:inicio_fila+3, inicio_columna:inicio_columna+3]:
            return False
        return True
    
    def backtracking(self, fila, columna):
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
        self.dificultad = dificultad

