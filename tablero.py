import numpy as np
import globals
import pygame

class Tablero:
    def __init__(self, pantalla, sudoku, resuelto):
        self.sudoku = sudoku      
        self.resuelto = resuelto
        self.inicial = np.copy(self.sudoku)
        self.pantalla = pantalla
        
    def set_valor(self, fila, columna, valor):
        """
        Establece el valor de una celda en el tablero.

        Parámetros:
        - fila: entero que representa la fila de la celda.
        - columna: entero que representa la columna de la celda.
        - valor: entero que representa el valor a establecer en la celda.
        """
        if self.inicial[fila, columna] == 0:
            if self.sudoku[fila][columna] == valor:
                return
            elif self.es_posible(fila, columna, valor):
                self.sudoku[fila][columna] = valor
            else:
                self.sudoku[fila][columna] = -valor

    def borrar_valor(self, fila, columna):
        """
        Borra el valor de una celda en el tablero.

        Parámetros:
        - fila: entero que representa la fila de la celda.
        - columna: entero que representa la columna de la celda.
        """
        if self.inicial[fila][columna] == 0:
            self.sudoku[fila][columna] = 0

    def borrar_tablero(self):
        """
        Borra el contenido del tablero y lo restablece a su estado inicial.
        """
        for fila in range(9):
            for columna in range(9):
                self.sudoku[fila][columna] = self.inicial[fila][columna]

        self.pantalla.fill(globals.BLANCO)

        self.imprimir_numeros()
        self.imprimir_tablero()
        pygame.display.update()

    def es_posible(self, fila, columna, numero):
        """
        Verifica si es posible colocar un número en una celda del tablero.

        Parámetros:
        - fila: entero que representa la fila de la celda.
        - columna: entero que representa la columna de la celda.
        - numero: entero que representa el número a verificar.

        Retorna:
        - True si es posible colocar el número en la celda, False en caso contrario.
        """
        if numero in self.sudoku[fila]:
            return False
        if numero in [fila[columna] for fila in self.sudoku]:
            return False
        inicio_fila = (fila // 3) * 3
        inicio_columna = (columna // 3) * 3
        if numero in self.sudoku[inicio_fila:inicio_fila+3, inicio_columna:inicio_columna+3]:
            return False
        return True
        
    def imprimir_tablero(self):
        """
        Imprime las líneas del tablero en la pantalla.
        """
        for fila in range(10):
            grosor = 4 if fila % 3 == 0 else 1
            pygame.draw.line(self.pantalla, globals.NEGRO, (globals.MARGEN, globals.MARGEN + fila * globals.TAMAÑO_CELDA), (globals.ANCHO - globals.MARGEN, globals.MARGEN + fila * globals.TAMAÑO_CELDA), grosor)
            pygame.draw.line(self.pantalla, globals.NEGRO, (globals.MARGEN + fila * globals.TAMAÑO_CELDA, globals.MARGEN), (globals.MARGEN + fila * globals.TAMAÑO_CELDA, globals.ALTO - globals.MARGEN), grosor)

    def imprimir_numeros(self, solucion=False):
        """
        Imprime los números en el tablero.

        Parámetros:
        - solucion: booleano que indica si se imprimirá la solución en lugar del sudoku actual.
        """
        for fila in range(9):
            for columna in range(9):
                if not solucion:
                    valor = self.sudoku[fila][columna]
                else:
                    valor = self.resuelto[fila, columna]
                if valor != 0:
                    if valor > 0:
                        color = globals.NEGRO
                    elif globals.es_accesible():
                        color = globals.NEGRO
                        fondo_cruz = pygame.image.load(globals.RUTA_CRUZ)
                        fondo_cruz = pygame.transform.scale(fondo_cruz, (globals.TAMAÑO_CELDA, globals.TAMAÑO_CELDA))
                        self.pantalla.blit(fondo_cruz, (globals.MARGEN + columna * globals.TAMAÑO_CELDA, globals.MARGEN + fila * globals.TAMAÑO_CELDA))
                    else:
                        color = globals.ROJO

                    if self.inicial[fila][columna] == valor:
                        texto = pygame.font.Font(globals.fuente_negrita, globals.TAM_FUENTE).render(str(abs(valor)), True, color)
                    else:
                        texto = pygame.font.Font(globals.fuente, globals.TAM_FUENTE).render(str(abs(valor)), True, color)
                    texto_rect = texto.get_rect(center=(
                        globals.MARGEN + columna * globals.TAMAÑO_CELDA + globals.TAMAÑO_CELDA / 2,
                        globals.MARGEN + fila * globals.TAMAÑO_CELDA + globals.TAMAÑO_CELDA / 2
                    ))
                    
                    self.pantalla.blit(texto, texto_rect)

    def iluminar_celda(self, fila, columna, color):
        """
        Ilumina una celda del tablero con un color específico.

        Parámetros:
        - fila: entero que representa la fila de la celda.
        - columna: entero que representa la columna de la celda.
        - color: tupla que representa el color en formato RGB.
        """
        rect = pygame.Rect(
            globals.MARGEN + columna * globals.TAMAÑO_CELDA,
            globals.MARGEN + fila * globals.TAMAÑO_CELDA,
            globals.TAMAÑO_CELDA,
            globals.TAMAÑO_CELDA
        )
        pygame.draw.rect(self.pantalla, color, rect)
        valor = self.sudoku[fila][columna]
        if valor != 0:
            texto = pygame.font.Font(globals.fuente, globals.TAM_FUENTE).render(str(valor), True, globals.NEGRO)
            texto_rect = texto.get_rect(center=(
                globals.MARGEN + columna * globals.TAMAÑO_CELDA + globals.TAMAÑO_CELDA / 2,
                globals.MARGEN + fila * globals.TAMAÑO_CELDA + globals.TAMAÑO_CELDA / 2
            ))
            self.pantalla.blit(texto, texto_rect)

    def comprobar_solucion(self):
        """
        Comprueba si la solución del sudoku es correcta y resalta las celdas incorrectas en amarillo.

        No recibe ningún parámetro.

        No retorna ningún valor.
        """
        for fila in range(9):
            for columna in range(9):
                if self.inicial[fila, columna] == 0:
                    if self.sudoku[fila][columna] != self.resuelto[fila][columna]:
                        self.iluminar_celda(fila, columna, globals.AMARILLO)
                    else:
                        self.iluminar_celda(fila, columna, globals.VERDE)
        self.dibujar_tablero_comprobado()
        pygame.display.update()

    def dibujar_tablero_comprobado(self):
        """
        Dibuja el tablero con la solución comprobada.

        No recibe ningún parámetro.

        No retorna ningún valor.
        """
        for fila in range(9):
            for columna in range(9):
                valor = self.sudoku[fila][columna]
                if valor != 0:
                    color = globals.NEGRO if valor > 0 else globals.ROJO
                    texto = pygame.font.Font(globals.fuente, globals.TAM_FUENTE).render(str(abs(valor)), True, color)
                    texto_rect = texto.get_rect(center=(
                        globals.MARGEN + columna * globals.TAMAÑO_CELDA + globals.TAMAÑO_CELDA / 2,
                        globals.MARGEN + fila * globals.TAMAÑO_CELDA + globals.TAMAÑO_CELDA / 2
                    ))
                    self.pantalla.blit(texto, texto_rect)
        for i in range(10):
            grosor = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.pantalla, globals.NEGRO, (globals.MARGEN, globals.MARGEN + i * globals.TAMAÑO_CELDA), (globals.MARGEN + 9 * globals.TAMAÑO_CELDA, globals.MARGEN + i * globals.TAMAÑO_CELDA), grosor)
            pygame.draw.line(self.pantalla, globals.NEGRO, (globals.MARGEN + i * globals.TAMAÑO_CELDA, globals.MARGEN), (globals.MARGEN + i * globals.TAMAÑO_CELDA, globals.MARGEN + 9 * globals.TAMAÑO_CELDA), grosor)

    def mostrar_solucion(self):
        """
        Muestra la solución del sudoku en el tablero.

        No recibe ningún parámetro.

        No retorna ningún valor.
        """
        self.borrar_tablero()
        for fila in range(9):
            for columna in range(9):
                self.sudoku[fila][columna] = self.resuelto[fila][columna]
        self.imprimir_numeros()
        self.imprimir_tablero()
        pygame.display.update()
