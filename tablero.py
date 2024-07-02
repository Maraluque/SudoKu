import numpy as np
import pygame
from pantalla import Utils

class Tablero:

    def __init__(self, pantalla):
        # Inicializa un tablero de Sudoku de 9x9 con ceros
        self.tablero = np.zeros((9, 9), dtype=int)
        self.pantalla = pantalla
        

    def insertar_numero(self, fila, columna, numero):
        """Inserta un número en una posición específica del tablero."""
        if self.es_posible(fila, columna, numero):
            self.tablero[fila, columna] = numero
            return True
        return False

    def es_posible(self, fila, columna, numero):
        """Verifica si es posible insertar un número en la posición dada."""
        # Verificar si el número ya está en la fila
        if numero in self.tablero[fila]:
            return False
        # Verificar si el número ya está en la columna
        if numero in self.tablero[:, columna]:
            return False
        # Verificar si el número ya está en el cuadrante 3x3
        cuadrante_fila = fila // 3 * 3
        cuadrante_columna = columna // 3 * 3
        if numero in self.tablero[cuadrante_fila:cuadrante_fila+3, cuadrante_columna:cuadrante_columna+3]:
            return False
        return True

    def imprimir_tablero(self):
        # Constantes para la GUI
        TAMAÑO_CELDA = 60
        MARGEN = 20
        ANCHO = MARGEN * 2 + TAMAÑO_CELDA * 9  # Ajustado para que dependa del tamaño de la celda y el margen
        ALTO = MARGEN * 2 + TAMAÑO_CELDA * 9  # Igual que ANCHO para mantener la proporción
        COLOR_FONDO = (255, 255, 255)
        COLOR_LINEA = (0, 0, 0)
        self.pantalla.fill(COLOR_FONDO)

        # Dibujar las líneas del tablero
        for fila in range(10):
            grosor = 4 if fila % 3 == 0 else 1
            pygame.draw.line(self.pantalla, COLOR_LINEA, (MARGEN, MARGEN + fila * TAMAÑO_CELDA), (ANCHO - MARGEN, MARGEN + fila * TAMAÑO_CELDA), grosor)
            pygame.draw.line(self.pantalla, COLOR_LINEA, (MARGEN + fila * TAMAÑO_CELDA, MARGEN), (MARGEN + fila * TAMAÑO_CELDA, ALTO - MARGEN), grosor)

        #! no funciona poner los números en el tablero
        # Dibujar los números en el tablero
        fuente = pygame.font.Font(None, 40)
        for fila in range(9):
            for columna in range(9):
                valor = self.tablero[fila][columna]
                if valor != 0:
                    texto = fuente.render(str(valor), True, COLOR_LINEA)
                    x = MARGEN + columna * TAMAÑO_CELDA + (TAMAÑO_CELDA - texto.get_width()) / 2
                    y = MARGEN + fila * TAMAÑO_CELDA + (TAMAÑO_CELDA - texto.get_height()) / 2
                    self.pantalla.blit(texto, (x, y))
        
        # Dibujar botón para volver al menú
        #utils = Utils(self.pantalla)
        #utils.dibujar_boton("Volver al menú", 10, 10, 150, 40, utils.GRIS, utils.ROJO, utils.empezar_juego)

        # Dibujar botón para ver valores de ejemplo en la parte derecha de la pantalla
        #utils.dibujar_boton("Ver valores de ejemplo", 580, 10, 200, 40, utils.GRIS, utils.ROJO, self.poner_valores_ejemplo_sudoku_completo)


    def poner_valores_ejemplo_sudoku_completo(self):
        self.tablero = np.array([[5, 3, 4, 6, 7, 8, 9, 1, 2],
                                 [6, 7, 2, 1, 9, 5, 3, 4, 8],
                                 [1, 9, 8, 3, 4, 2, 5, 6, 7],
                                 [8, 5, 9, 7, 6, 1, 4, 2, 3],
                                 [4, 2, 6, 8, 5, 3, 7, 9, 1],
                                 [7, 1, 3, 9, 2, 4, 8, 5, 6],
                                 [9, 6, 1, 5, 3, 7, 2, 8, 4],
                                 [2, 8, 7, 4, 1, 9, 6, 3, 5],
                                 [3, 4, 5, 2, 8, 6, 1, 7, 9]])
        
            