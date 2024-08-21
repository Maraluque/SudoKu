import pygame
import sys
import numpy as np
import globals
import random
import time

class Utils:
    def __init__(self, pantalla, sudoku_instance):
        self.pantalla = pantalla
        self.boton_empezar = pygame.Rect(100, 100, 200, 50)
        self.boton_tutorial = pygame.Rect(100, 200, 200, 50)
        self.boton_info_creador = pygame.Rect(100, 300, 200, 50)
        self.boton_comprobar = pygame.Rect(100, 400, 200, 50)
        self.temporizador_iniciado = False
        self.tiempo_inicio = 0
        self.tiempo_actual = 0
        self.tiempo_pausa = 0
        self.instancia_sudoku = sudoku_instance
        self.inicio_juego = True
        self.dificultad = 0
        

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

    def mostrar_pantalla_carga(self):
        # Cargar imágenes de la animación
        frames = [pygame.image.load(f'img/cargando{i}.png') for i in range(1, 12)]  # Asegúrate de tener frame1.png, frame2.png, etc.

        
        # Redimensionar los fotogramas
        tamaño_nuevo = (50, 50)  # Tamaño deseado para los fotogramas
        frames = [pygame.transform.scale(frame, tamaño_nuevo) for frame in frames]

        # Calcular las coordenadas para centrar la animación
        ancho_pantalla, alto_pantalla = self.pantalla.get_size()
        x_centro = (ancho_pantalla - tamaño_nuevo[0]) // 2
        y_centro = (alto_pantalla - tamaño_nuevo[1]) // 2

        self.pantalla.fill(globals.BLANCO)
        for frame in frames:
            self.pantalla.fill(globals.BLANCO)  # Limpiar la pantalla
            self.pantalla.blit(frame, (x_centro, y_centro))  # Dibujar el frame en el centro de la pantalla
            pygame.display.flip()
            time.sleep(0.1)  # Esperar un poco antes de mostrar el siguiente frame

        for frame in frames:
            self.pantalla.fill(globals.BLANCO)  # Limpiar la pantalla
            self.pantalla.blit(frame, (x_centro, y_centro))  # Dibujar el frame en el centro de la pantalla
            pygame.display.flip()
            time.sleep(0.1)  # Esperar un poco antes de mostrar el siguiente frame

    def seleccionar_dificultad(self):
        seleccionando_dificultad = True

        while seleccionando_dificultad:
            self.pantalla.fill(globals.BLANCO)
            easy_button = pygame.Rect(300, 150, 200, 50)
            medium_button = pygame.Rect(300, 250, 200, 50)
            hard_button = pygame.Rect(300, 350, 200, 50)

            font = pygame.font.Font(None, 74)
            button_font = pygame.font.Font(None, 36)


            pygame.draw.rect(self.pantalla, globals.GRIS, easy_button)
            pygame.draw.rect(self.pantalla, globals.GRIS, medium_button)
            pygame.draw.rect(self.pantalla, globals.GRIS, hard_button)
            
            easy_text = button_font.render("Fácil", True, globals.NEGRO)
            medium_text = button_font.render("Medio", True, globals.NEGRO)
            hard_text = button_font.render("Difícil", True, globals.NEGRO)
            
            self.pantalla.blit(easy_text, (easy_button.x + 50, easy_button.y + 10))
            self.pantalla.blit(medium_text, (medium_button.x + 50, medium_button.y + 10))
            self.pantalla.blit(hard_text, (hard_button.x + 50, hard_button.y + 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_button.collidepoint(event.pos):
                        self.set_dificultad(0)
                        seleccionando_dificultad = False
                    elif medium_button.collidepoint(event.pos):
                        self.set_dificultad(1)
                        seleccionando_dificultad = False
                    elif hard_button.collidepoint(event.pos):
                        self.set_dificultad(2)
                        seleccionando_dificultad = False

            pygame.display.flip()
            pygame.time.Clock().tick(60) # 60 FPS

            if self.dificultad:
                seleccionando_dificultad = False

        return self.dificultad

    def set_dificultad(self, dificultad):
        self.dificultad = dificultad

    def empezar_juego(self):
        # pantalla de carga y selección de dificultad
        self.dificultad = self.seleccionar_dificultad()
        self.mostrar_pantalla_carga()

        sudoku, resuelto = self.instancia_sudoku.crear_sudoku()
        self.tablero = Tablero(self.pantalla, sudoku, resuelto)

        en_juego = True
        celda_seleccionada = None
        cambio_en_tablero = True
        
        while en_juego:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    en_juego = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    columna = (pos[0] - globals.MARGEN) // globals.TAMAÑO_CELDA
                    fila = (pos[1] - globals.MARGEN) // globals.TAMAÑO_CELDA
                    if 0 <= columna < 9 and 0 <= fila < 9:
                        celda_seleccionada = (fila, columna)
                        cambio_en_tablero = True
                elif evento.type == pygame.KEYDOWN and celda_seleccionada:
                    if evento.unicode.isdigit() and evento.unicode != '0':
                        fila, columna = celda_seleccionada
                        self.tablero.set_valor(fila, columna, int(evento.unicode))
                        cambio_en_tablero = True
                    elif evento.key == pygame.K_BACKSPACE:
                        self.tablero.borrar_valor(fila, columna)
                        cambio_en_tablero = True

            if cambio_en_tablero:
                self.pantalla.fill(globals.BLANCO)
                

                if celda_seleccionada:
                    fila, columna = celda_seleccionada
                    self.iluminar_celdas(fila, columna)
                    self.iluminar_celda_seleccionada(fila, columna, globals.MORADO_CLARO)
                
                self.tablero.imprimir_numeros()
                self.tablero.imprimir_tablero()
                cambio_en_tablero = False

            # Dibujar temporizador y botones
            hueco_x = globals.PANTALLA_ANCHO - 225  # Ajustar según el tamaño del hueco
            self.dibujar_boton("Iniciar", hueco_x, 50, 100, 50, globals.GRIS, globals.VERDE, self.iniciar_temporizador)
            self.dibujar_temporizador()
            if self.temporizador_iniciado or self.inicio_juego:
                self.dibujar_boton("Pausar", hueco_x + 110, 50, 100, 50, globals.GRIS, globals.ROJO, self.pausar_temporizador)
            else:
                self.dibujar_boton("Continuar", hueco_x + 110, 50, 100, 50, globals.GRIS, globals.ROJO, self.pausar_temporizador)
            self.dibujar_boton("Comprobar", hueco_x, 110, 210, 50, globals.GRIS, globals.AZUL, self.comprobar_solucion)
            self.dibujar_boton("Mostrar Solución", hueco_x, 170, 210, 50, globals.GRIS, globals.AMARILLO, self.tablero.mostrar_solucion)
            self.dibujar_boton("Borrar Tablero", hueco_x, 230, 210, 50, globals.GRIS, globals.NARANJA, self.tablero.borrar_tablero)
            self.dibujar_boton("Salir", hueco_x, 290, 210, 50, globals.GRIS, globals.MORADO_CLARO, self.salir_juego)

            # Dibujar dificultad
            fuente = pygame.font.Font(None, 36)
            texto_dificultad = fuente.render(f"Dificultad: {self.dificultad}", True, globals.NEGRO)

            self.pantalla.blit(texto_dificultad, (globals.PANTALLA_ANCHO - 200, 450))

            self.actualizar_temporizador()
            self.dibujar_temporizador()
            

            pygame.display.flip()
            pygame.time.Clock().tick(60) # 60 FPS

    def comprobar_solucion(self):
        for fila in range(9):
            for columna in range(9):
                if self.tablero.sudoku[fila][columna] == self.tablero.resuelto[fila][columna]:
                    self.iluminar_celda_seleccionada(fila, columna, globals.VERDE_CLARO)  # Celda correcta
                else:
                    self.iluminar_celda_seleccionada(fila, columna, globals.MORADO_CLARO)  # Celda incorrecta
        self.tablero.imprimir_numeros()
        self.tablero.imprimir_tablero()
        pygame.display.update()

    def dibujar_temporizador(self):
        rect_temporizador = pygame.Rect(globals.PANTALLA_ANCHO - 170, 10, 100, 25)  # Ajusta la posición y tamaño según sea necesario
        self.pantalla.fill((255, 255, 255), rect_temporizador)
        minutos = int(self.tiempo_actual // 60)
        segundos = int(self.tiempo_actual % 60)
        tiempo_formateado = f"{minutos:02}:{segundos:02}"
        fuente = pygame.font.Font(None, 36)
        texto = pygame.font.Font(None, 36).render(tiempo_formateado, True, globals.NEGRO)
        self.pantalla.blit(texto, (globals.PANTALLA_ANCHO - 150, 10))

    def iniciar_temporizador(self):
        self.reiniciar_temporizador()
        self.temporizador_iniciado = True

    def pausar_temporizador(self):
        self.inicio_juego= False
        if self.temporizador_iniciado:
            self.tiempo_pausa = time.time() - self.tiempo_inicio
            self.temporizador_iniciado = False
        else:
            self.tiempo_inicio = time.time() - self.tiempo_pausa
            self.temporizador_iniciado = True
        time.sleep(0.1)

    def reiniciar_temporizador(self):
        self.tiempo_inicio = time.time()
        self.tiempo_actual = 0
        self.tiempo_pausa = 0

    def actualizar_temporizador(self):
        if self.temporizador_iniciado:
            self.tiempo_actual = time.time() - self.tiempo_inicio

    def salir_juego(self):
        pygame.quit()
        sys.exit()

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
class Sudoku:
    def __init__(self, dificultad=0):
        self.dificultad = dificultad
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
        
    def crear_sudoku(self):
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
                self.sudoku[fila][columna] = resuelto[fila][columna]

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
        if numero in self.sudoku[fila]:
            return False
        # Verificar columna
        if numero in [fila[columna] for fila in self.sudoku]:
            return False
        # Verificar cuadrado 3x3
        inicio_fila = (fila // 3) * 3
        inicio_columna = (columna // 3) * 3
        if numero in self.sudoku[inicio_fila:inicio_fila+3, inicio_columna:inicio_columna+3]:
            return False
        return True


class Tablero:
    def __init__(self, pantalla, sudoku, resuelto):
        self.sudoku = sudoku      
        self.resuelto = resuelto
        self.inicial = np.copy(self.sudoku)
        self.pantalla = pantalla
        
    def set_valor(self, fila, columna, valor):
        if self.inicial[fila, columna] == 0:  # Solo permitir cambios en celdas que eran 0 inicialmente
            if self.es_posible(fila, columna, valor):
                self.sudoku[fila][columna] = valor
            else:
                self.sudoku[fila][columna] = -valor

    def borrar_valor(self, fila, columna):
        if self.inicial[fila][columna] == 0:  # Solo permitir borrar en celdas que eran 0 inicialmente
            self.sudoku[fila][columna] = 0

    def borrar_tablero(self):
        print("Borrando tablero")
        for fila in range(9):
            for columna in range(9):
                self.sudoku[fila][columna] = self.inicial[fila][columna]

        # Limpiar la pantalla
        self.pantalla.fill(globals.BLANCO)

        self.imprimir_numeros()
        self.imprimir_tablero()
        pygame.display.update()

    def es_posible(self, fila, columna, numero):
        # Verificar fila
        if numero in self.sudoku[fila]:
            return False
        # Verificar columna
        if numero in [fila[columna] for fila in self.sudoku]:
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
                    valor = self.sudoku[fila][columna]
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
        print("comprobando solución")
        for fila in range(9):
            for columna in range(9):
                if self.inicial[fila, columna] == 0:  # Solo comprobar celdas que no estaban rellenas inicialmente
                    if self.sudoku[fila][columna] != self.resuelto[fila][columna]:
                        self.iluminar_celda(fila, columna, globals.AMARILLO)
                    else:
                        self.iluminar_celda(fila, columna, globals.VERDE)
        self.dibujar_tablero_comprobado()
        pygame.display.update()
        # si está bien muestra un mensaje de enhorabuena

    def dibujar_tablero_comprobado(self):
        print("dibujando tablero")
        for fila in range(9):
            for columna in range(9):
                valor = self.sudoku[fila][columna]
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
        print("Mostrando la solución")
        self.borrar_tablero()
        for fila in range(9):
            for columna in range(9):
                self.sudoku[fila][columna] = self.resuelto[fila][columna]
        self.imprimir_numeros()
        self.imprimir_tablero()
        pygame.display.update()

    

if __name__ == "__main__":
    pygame.init()
    pantalla = pygame.display.set_mode((globals.PANTALLA_ANCHO, globals.PANTALLA_ALTO))
    pygame.display.set_caption("SUDOku")
    s = Sudoku()
    utils = Utils(pantalla, s)
    utils.mostrar_menu()

    