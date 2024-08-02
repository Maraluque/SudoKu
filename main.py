import pygame
import sys
import numpy as np
import globals
import time

class Utils:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.boton_empezar = pygame.Rect(100, 100, 200, 50)
        self.boton_tutorial = pygame.Rect(100, 200, 200, 50)
        self.boton_info_creador = pygame.Rect(100, 300, 200, 50)
        self.boton_comprobar = pygame.Rect(100, 400, 200, 50)
        self.temporizador_iniciado = False
        self.tiempo_inicio = 0
        self.tiempo_actual = 0
        self.modo_comprobacion = False
        self.tablero = Tablero(self.pantalla)

    def dibujar_boton(self, mensaje, x, y, ancho, alto, color_inactivo, color_activo, accion=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + ancho > mouse[0] > x and y + alto > mouse[1] > y:
            pygame.draw.rect(self.pantalla, color_activo, (x, y, ancho, alto))
            if click[0] == 1 and accion:
                accion()
        else:
            pygame.draw.rect(self.pantalla, color_inactivo, (x, y, ancho, alto))
        
        texto = pygame.font.Font(None, 20).render(mensaje, True, globals.NEGRO)
        texto_rect = texto.get_rect(center=(x + ancho / 2, y + alto / 2))
        self.pantalla.blit(texto, texto_rect)

    def empezar_juego(self):
        en_menu = True
        celda_seleccionada = None

        while en_menu:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    en_menu = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton_comprobar.collidepoint(evento.pos):
                        self.modo_comprobacion = True
                    else:
                        pos = pygame.mouse.get_pos()
                        columna = (pos[0] - globals.MARGEN) // globals.TAMAÑO_CELDA
                        fila = (pos[1] - globals.MARGEN) // globals.TAMAÑO_CELDA
                        if 0 <= columna < 9 and 0 <= fila < 9:
                            celda_seleccionada = (fila, columna)
                elif evento.type == pygame.KEYDOWN and celda_seleccionada:
                    if evento.unicode.isdigit() and evento.unicode != '0':
                        fila, columna = celda_seleccionada
                        self.tablero.set_valor(fila, columna, int(evento.unicode))
                    elif evento.key == pygame.K_BACKSPACE:
                        self.tablero.borrar_valor(fila, columna)

            self.pantalla.fill(globals.BLANCO)
            
            if self.modo_comprobacion:
                self.comprobar_solucion()

            if celda_seleccionada:
                fila, columna = celda_seleccionada
                self.iluminar_celdas(fila, columna)
                self.iluminar_celda_seleccionada(fila, columna, globals.MORADO_CLARO)
            
            self.tablero.imprimir_numeros()
            self.tablero.imprimir_tablero()

            # Dibujar temporizador y botones
            hueco_x = globals.PANTALLA_ANCHO - 225  # Ajustar según el tamaño del hueco
            self.dibujar_boton("Iniciar", hueco_x, 50, 100, 50, globals.GRIS, globals.VERDE, self.iniciar_temporizador)
            self.dibujar_boton("Detener", hueco_x + 110, 50, 100, 50, globals.GRIS, globals.ROJO, self.detener_temporizador)
            self.dibujar_boton("Comprobar", hueco_x, 110, 210, 50, globals.GRIS, globals.AZUL, self.comprobar_solucion)
            self.dibujar_boton("Mostrar Solución", hueco_x, 170, 210, 50, globals.GRIS, globals.AMARILLO, self.tablero.mostrar_solucion)
            self.dibujar_boton("Salir", hueco_x, 230, 210, 50, globals.GRIS, globals.NARANJA, self.salir_juego)


            pygame.display.flip()
            pygame.time.Clock().tick(60)

    def comprobar_solucion(self):
        for fila in range(9):
            for columna in range(9):
                if self.tablero.inicial[fila][columna] == 0:  # Solo comprobar celdas que no estaban rellenas inicialmente
                    if self.tablero.sudoku[fila][columna] == self.tablero.resuelto[fila][columna]:
                        self.iluminar_celda_seleccionada(fila, columna, globals.VERDE_CLARO)  # Celda correcta
                    else:
                        self.iluminar_celda_seleccionada(fila, columna, globals.ROJO)  # Celda incorrecta
        self.tablero.imprimir_numeros()
        self.tablero.imprimir_tablero()
        pygame.display.update()

    def dibujar_temporizador(self):
        if self.temporizador_iniciado:
            self.tiempo_actual = time.time() - self.tiempo_inicio
        minutos = int(self.tiempo_actual // 60)
        segundos = int(self.tiempo_actual % 60)
        tiempo_str = f"{minutos:02}:{segundos:02}"
        texto = pygame.font.Font(None, 36).render(tiempo_str, True, globals.NEGRO)
        self.pantalla.blit(texto, (globals.PANTALLA_ANCHO - 150, 10))

    def iniciar_temporizador(self):
        if not self.temporizador_iniciado:
            self.temporizador_iniciado = True
            self.tiempo_inicio = time.time() - self.tiempo_actual

    def detener_temporizador(self):
        self.temporizador_iniciado = False
        self.tiempo_actual = 0  # Poner el tiempo a cero

    def salir_juego(self):
        # Implementar lógica para salir del juego y volver al menú
        pass

    def iluminar_celdas(self, fila, columna):
        # Iluminar las celdas del cuadrado 3x3
        inicio_fila = (fila // 3) * 3
        inicio_columna = (columna // 3) * 3
        for i in range(3):
            for j in range(3):
                self.dibujar_rectangulo(inicio_fila + i, inicio_columna + j, globals.VERDE_CLARO)

        # Iluminar las celdas horizontales y verticales
        for i in range(9):
            self.dibujar_rectangulo(fila, i, globals.VERDE_CLARO)  # Horizontal
            self.dibujar_rectangulo(i, columna, globals.VERDE_CLARO)  # Vertical

    def iluminar_celda_seleccionada(self, fila, columna, color):
        self.dibujar_rectangulo(fila, columna, color)

    def dibujar_rectangulo(self, fila, columna, color):
        grosor_linea = 4 if (fila % 3 == 0 or columna % 3 == 0) else 1
        rect = pygame.Rect(
            globals.MARGEN + columna * globals.TAMAÑO_CELDA + grosor_linea // 2,
            globals.MARGEN + fila * globals.TAMAÑO_CELDA + grosor_linea // 2,
            globals.TAMAÑO_CELDA - grosor_linea + 2.5,
            globals.TAMAÑO_CELDA - grosor_linea + 2.5
        )
        pygame.draw.rect(self.pantalla, color, rect)


    def ver_tutorial(self):
        print("Ver tutorial")  # Aquí iría la lógica para mostrar el tutorial

    def ver_info_creador(self):
        ruta = "foto_orla.jpeg"
        mi_foto_original = pygame.image.load(ruta)  # Carga la foto
        mi_foto = pygame.transform.scale(mi_foto_original, (130, 170))  # Redimensiona la foto
    
        margen_derecho = 10  # Margen derecho en píxeles
        margen_superior = 10  # Margen superior en píxeles
        posicion_x = self.pantalla.get_width() - mi_foto.get_width() - margen_derecho
        posicion_y = margen_superior
    
        self.pantalla.fill(globals.BLANCO)
        self.pantalla.blit(mi_foto, (posicion_x, posicion_y))
    
        fuente = pygame.font.Font(None, 24)
        descripcion = fuente.render("Proyecto de Trabajo de Fin de Grado realizado por María de las Maravillas Luque Carmona", True, globals.NEGRO)
        descripcion_rect = descripcion.get_rect(center=(self.pantalla.get_width() / 2, 300))
        self.pantalla.blit(descripcion, descripcion_rect)
    
        contacto = fuente.render("Contacto: mmlc0007@red.ujaen.es", True, globals.NEGRO)
        contacto_rect = contacto.get_rect(center=(self.pantalla.get_width() / 2, 350))
        self.pantalla.blit(contacto, contacto_rect)
    
        pygame.display.flip()
        pygame.time.wait(5000)  # Espera 5 segundos
        self.mostrar_menu()  # Regresa al menú principal

    def mostrar_menu(self):
        en_menu = True
        while en_menu:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.boton_empezar.collidepoint(pos):
                        en_menu = False
                        self.empezar_juego()
                    elif self.boton_tutorial.collidepoint(pos):
                        self.ver_tutorial()
                    elif self.boton_info_creador.collidepoint(pos):
                        self.ver_info_creador()

            self.pantalla.fill(globals.BLANCO)
            self.dibujar_boton("Empezar", 100, 100, 200, 50, (200, 200, 200), (255, 0, 0), self.empezar_juego)
            self.dibujar_boton("Tutorial", 100, 200, 200, 50, (200, 200, 200), (255, 0, 0))
            self.dibujar_boton("Info del Creador", 100, 300, 200, 50, (200, 200, 200), (255, 0, 0))

            pygame.display.flip()
            pygame.time.Clock().tick(60)

class Tablero:
    def __init__(self, pantalla):
        # Crear tablero con números de ejemplo
        self.sudoku = np.array([[5, 3, 0, 0, 7, 0, 0, 0, 0],
                                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                                [0, 0, 0, 0, 8, 0, 0, 7, 9]])
                                
        self.resuelto = np.array([[5, 3, 4, 6, 7, 8, 9, 1, 2],
                                [6, 7, 2, 1, 9, 5, 3, 4, 8],
                                [1, 9, 8, 3, 4, 2, 5, 6, 7],
                                [8, 5, 9, 7, 6, 1, 4, 2, 3],
                                [4, 2, 6, 8, 5, 3, 7, 9, 1],
                                [7, 1, 3, 9, 2, 4, 8, 5, 6],
                                [9, 6, 1, 5, 3, 7, 2, 8, 4],
                                [2, 8, 7, 4, 1, 9, 6, 3, 5],
                                [3, 4, 5, 2, 8, 6, 1, 7, 9]])
        self.inicial = np.copy(self.sudoku)
        self.pantalla = pantalla

    def set_valor(self, fila, columna, valor):
        if self.inicial[fila, columna] == 0:  # Solo permitir cambios en celdas que eran 0 inicialmente
            if self.es_posible(fila, columna, valor):
                self.sudoku[fila, columna] = valor
            else:
                self.sudoku[fila, columna] = -valor

    def borrar_valor(self, fila, columna):
        if self.inicial[fila, columna] == 0:  # Solo permitir borrar en celdas que eran 0 inicialmente
            self.sudoku[fila, columna] = 0

    def es_posible(self, fila, columna, numero):
        # Verificar fila
        if numero in self.sudoku[fila]:
            return False
        # Verificar columna
        if numero in self.sudoku[:, columna]:
            return False
        # Verificar cuadrado 3x3
        inicio_fila = (fila // 3) * 3
        inicio_columna = (columna // 3) * 3
        if numero in self.sudoku[inicio_fila:inicio_fila+3, inicio_columna:inicio_columna+3]:
            return False
        return True

    def imprimir_tablero(self):
        for fila in range(10):
            grosor = 4 if fila % 3 == 0 else 1
            pygame.draw.line(self.pantalla, globals.COLOR_LINEA, (globals.MARGEN, globals.MARGEN + fila * globals.TAMAÑO_CELDA), (globals.ANCHO - globals.MARGEN, globals.MARGEN + fila * globals.TAMAÑO_CELDA), grosor)
            pygame.draw.line(self.pantalla, globals.COLOR_LINEA, (globals.MARGEN + fila * globals.TAMAÑO_CELDA, globals.MARGEN), (globals.MARGEN + fila * globals.TAMAÑO_CELDA, globals.ALTO - globals.MARGEN), grosor)


    def imprimir_numeros(self, solucion=False):
        for fila in range(9):
            for columna in range(9):
                if not solucion:
                    valor = self.sudoku[fila, columna]
                else:
                    valor = self.resuelto[fila, columna]
                if valor != 0:
                    color = globals.NEGRO if valor > 0 else globals.ROJO
                    texto = pygame.font.Font(None, 36).render(str(abs(valor)), True, color)
                    texto_rect = texto.get_rect(center=(
                        globals.MARGEN + columna * globals.TAMAÑO_CELDA + globals.TAMAÑO_CELDA / 2,
                        globals.MARGEN + fila * globals.TAMAÑO_CELDA + globals.TAMAÑO_CELDA / 2
                    ))
                    self.pantalla.blit(texto, texto_rect)

    def iluminar_celda(self, fila, columna, color):
        rect = pygame.Rect(
            globals.MARGEN + columna * globals.TAMAÑO_CELDA,
            globals.MARGEN + fila * globals.TAMAÑO_CELDA,
            globals.TAMAÑO_CELDA,
            globals.TAMAÑO_CELDA
        )
        pygame.draw.rect(self.pantalla, color, rect)
        valor = self.sudoku[fila][columna]
        if valor != 0:
            texto = pygame.font.Font(None, 36).render(str(valor), True, globals.NEGRO)
            texto_rect = texto.get_rect(center=(
                globals.MARGEN + columna * globals.TAMAÑO_CELDA + globals.TAMAÑO_CELDA / 2,
                globals.MARGEN + fila * globals.TAMAÑO_CELDA + globals.TAMAÑO_CELDA / 2
            ))
            self.pantalla.blit(texto, texto_rect)

    def comprobar_solucion(self):
        for fila in range(9):
            for columna in range(9):
                if self.inicial[fila, columna] == 0:  # Solo comprobar celdas que no estaban rellenas inicialmente
                    if self.sudoku[fila][columna] != self.resuelto[fila][columna]:
                        self.iluminar_celda(fila, columna, globals.ROJO)
                    else:
                        self.iluminar_celda(fila, columna, globals.VERDE)
        self.dibujar_tablero()
        pygame.display.update()
        # si está bien muestra un mensaje de enhorabuena

    def dibujar_tablero(self):
        for fila in range(9):
            for columna in range(9):
                valor = self.sudoku[fila, columna]
                if valor != 0:
                    color = globals.NEGRO if valor > 0 else globals.ROJO
                    texto = pygame.font.Font(None, 36).render(str(abs(valor)), True, color)
                    texto_rect = texto.get_rect(center=(
                        globals.MARGEN + columna * globals.TAMAÑO_CELDA + globals.TAMAÑO_CELDA / 2,
                        globals.MARGEN + fila * globals.TAMAÑO_CELDA + globals.TAMAÑO_CELDA / 2
                    ))
                    self.pantalla.blit(texto, texto_rect)
        # Dibujar las líneas del tablero
        for i in range(10):
            grosor = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.pantalla, globals.NEGRO, (globals.MARGEN, globals.MARGEN + i * globals.TAMAÑO_CELDA), (globals.MARGEN + 9 * globals.TAMAÑO_CELDA, globals.MARGEN + i * globals.TAMAÑO_CELDA), grosor)
            pygame.draw.line(self.pantalla, globals.NEGRO, (globals.MARGEN + i * globals.TAMAÑO_CELDA, globals.MARGEN), (globals.MARGEN + i * globals.TAMAÑO_CELDA, globals.MARGEN + 9 * globals.TAMAÑO_CELDA), grosor)


    def mostrar_solucion(self):
        # Implementar lógica para mostrar la solución
        pass

    def crear_sudoku(self, dificultad):
        # Implementar lógica para crear los sudokus
        pass

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((globals.PANTALLA_ANCHO, globals.PANTALLA_ALTO))
    pygame.display.set_caption("SUDOku")
    utils = Utils(pantalla)
    utils.mostrar_menu()

    

if __name__ == "__main__":
    main()