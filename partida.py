import pygame
import sys
import numpy as np
import globals
import random
import time
import csv
import tablero

class Partida:
    def __init__(self, pantalla, sudoku_instance, ajustes):
        self.pantalla = pantalla
        self.temporizador_iniciado = False
        self.tiempo_inicio = 0
        self.tiempo_actual = 0
        self.tiempo_pausa = 0
        self.instancia_sudoku = sudoku_instance
        self.inicio_juego = True
        self.dificultad = 0
        self.config = ajustes
        

    def dibujar_boton(self, mensaje, x, y, ancho, alto, color_inactivo, color_activo, accion=None, logo=None):
        """
        Dibuja un botón en la pantalla.

        Args:
            mensaje (str): El texto que se mostrará en el botón.
            x (int): La coordenada x del botón.
            y (int): La coordenada y del botón.
            ancho (int): El ancho del botón.
            alto (int): El alto del botón.
            color_inactivo (tuple): El color del botón cuando no está seleccionado.
            color_activo (tuple): El color del botón cuando está seleccionado.
            accion (function, optional): La función que se ejecutará cuando se haga clic en el botón. Defaults to None.
            logo (pygame.Surface, optional): La imagen que se mostrará en el botón. Defaults to None.

        Returns:
            pygame.Rect: El rectángulo que representa el botón.
        """
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = pygame.Rect(x, y, ancho, alto)

        sombra_rect = rect.copy()
        sombra_rect.topleft = (rect.topleft[0] + 5, rect.topleft[1] + 5)
        pygame.draw.rect(self.pantalla, globals.GRIS, sombra_rect, border_radius=globals.BORDER_RADIUS)

        if rect.collidepoint(mouse):
            pygame.draw.rect(self.pantalla, color_activo, rect, border_radius=globals.BORDER_RADIUS)
            if click[0] == 1 and accion is not None:
                accion()
            texto_color = globals.NEGRO
        else:
            pygame.draw.rect(self.pantalla, color_inactivo, rect, border_radius=globals.BORDER_RADIUS)
            texto_color = globals.BLANCO

        if logo:
            logo_rect = logo.get_rect()
            logo_rect.center = rect.center
            self.pantalla.blit(logo, logo_rect)
        else:
            fuente = pygame.font.Font(globals.fuente, globals.TAM_FUENTE)
            texto = fuente.render(mensaje, True, texto_color)
            texto_rect = texto.get_rect(center=rect.center)
            self.pantalla.blit(texto, texto_rect)

        return rect

    def mostrar_pantalla_carga(self):
        """
        Muestra una pantalla de carga animada.

        Carga una serie de imágenes y las muestra en secuencia para simular una animación de carga.

        """
        frames = []
        frames.append(pygame.image.load(globals.IMG_CARGANDO1))
        frames.append(pygame.image.load(globals.IMG_CARGANDO2))
        frames.append(pygame.image.load(globals.IMG_CARGANDO3))
        frames.append(pygame.image.load(globals.IMG_CARGANDO4))
        frames.append(pygame.image.load(globals.IMG_CARGANDO5))
        frames.append(pygame.image.load(globals.IMG_CARGANDO6))
        frames.append(pygame.image.load(globals.IMG_CARGANDO7))
        frames.append(pygame.image.load(globals.IMG_CARGANDO8))
        frames.append(pygame.image.load(globals.IMG_CARGANDO9))
        frames.append(pygame.image.load(globals.IMG_CARGANDO10))
        frames.append(pygame.image.load(globals.IMG_CARGANDO11))
        frames.append(pygame.image.load(globals.IMG_CARGANDO12))


        tam_nuevo = (50, 50)
        frames = [pygame.transform.scale(frame, tam_nuevo) for frame in frames]

        ancho_pantalla, alto_pantalla = self.pantalla.get_size()
        x_centro = (ancho_pantalla - tam_nuevo[0]) // 2
        y_centro = (alto_pantalla - tam_nuevo[1]) // 2

        self.pantalla.fill(globals.BLANCO)
        for frame in frames:
            self.pantalla.fill(globals.BLANCO)
            self.pantalla.blit(frame, (x_centro, y_centro))
            pygame.display.flip()
            time.sleep(0.1)

    def mostrar_puntuacion(self):
        """
        Muestra la pantalla de puntuaciones.

        Muestra una tabla con las puntuaciones de los jugadores en cada dificultad.

        """
        en_puntuacion = True

        puntuaciones = []
        with open(globals.ARCHIVO_PUNTUACION, mode='r', newline='') as archivo:
            reader = csv.reader(archivo)
            next(reader)
            for row in reader:
                puntuaciones.append(row)
        puntuaciones.sort(key=lambda x: (x[0], float(x[1])))

        fondo = pygame.image.load(globals.RUTA_FONDO_PUNTUACION)
        fondo = pygame.transform.scale(fondo, (globals.PANTALLA_ANCHO, globals.PANTALLA_ALTO))

        medalla_bronce = pygame.image.load(globals.RUTA_MEDALLA_BRONCE)
        medalla_plata = pygame.image.load(globals.RUTA_MEDALLA_PLATA)
        medalla_oro = pygame.image.load(globals.RUTA_MEDALLA_ORO)

        medalla_bronce = pygame.transform.scale(medalla_bronce, (40, 40))
        medalla_plata = pygame.transform.scale(medalla_plata, (40, 40))
        medalla_oro = pygame.transform.scale(medalla_oro, (40, 40))

        while en_puntuacion:
            self.pantalla.fill(globals.BLANCO)
            self.pantalla.blit(fondo, (0, 0))
            boton_volver = self.dibujar_boton("Volver al menú", (globals.PANTALLA_ANCHO - 200) // 2, globals.PANTALLA_ALTO - 100, 200, 50, globals.GRIS_CLARO, globals.MORADO, self.mostrar_menu)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if boton_volver.collidepoint(mouse_pos):
                        en_puntuacion = False
                        self.mostrar_menu()


            fuente = pygame.font.Font(globals.fuente, globals.TAM_FUENTE_PUNTUACION)
            fuente_columnas = pygame.font.Font(globals.fuente, globals.TAM_FUENTE - 4)
            fuente_negrita = pygame.font.Font(globals.fuente_negrita, globals.TAM_FUENTE_PUNTUACION)
            fuente_columnas_negrita = pygame.font.Font(globals.fuente_negrita, globals.TAM_FUENTE)
            fuente_titulo_negrita = pygame.font.Font(globals.fuente_negrita, globals.TAM_FUENTE + 10)
            texto_titulo = fuente_titulo_negrita.render("Puntuaciones", True, globals.NEGRO)
            texto_titulo_rect = texto_titulo.get_rect(center=(globals.PANTALLA_ANCHO // 2, 50))
            self.pantalla.blit(texto_titulo, texto_titulo_rect)

            fila = 100
            texto_cabecera = fuente_columnas_negrita.render("Fácil", True, globals.NEGRO)
            texto_cabecera_rect = texto_cabecera.get_rect(center=(globals.PANTALLA_ANCHO // 2 - 100, fila))
            self.pantalla.blit(texto_cabecera, texto_cabecera_rect)

            texto_cabecera = fuente_columnas_negrita.render("Media", True, globals.NEGRO)
            texto_cabecera_rect = texto_cabecera.get_rect(center=(globals.PANTALLA_ANCHO // 2, fila))
            self.pantalla.blit(texto_cabecera, texto_cabecera_rect)

            texto_cabecera = fuente_columnas_negrita.render("Difícil", True, globals.NEGRO)
            texto_cabecera_rect = texto_cabecera.get_rect(center=(globals.PANTALLA_ANCHO // 2 + 100, fila))
            self.pantalla.blit(texto_cabecera, texto_cabecera_rect)

            texto_media = fuente_columnas.render("Promedio", True, globals.NEGRO)
            texto_media_rect = texto_media.get_rect(center=(globals.PANTALLA_ANCHO // 2 - 200, fila + 356))
            self.pantalla.blit(texto_media, texto_media_rect)

            pygame.draw.line(self.pantalla, globals.GRIS_CLARO, (globals.PANTALLA_ANCHO // 2 - 50, fila - 25), (globals.PANTALLA_ANCHO // 2 - 50, fila + 380), 2)
            pygame.draw.line(self.pantalla, globals.GRIS_CLARO, (globals.PANTALLA_ANCHO // 2 - 150, fila - 75), (globals.PANTALLA_ANCHO // 2 - 150, fila + 380), 2)
            pygame.draw.line(self.pantalla, globals.GRIS_CLARO, (globals.PANTALLA_ANCHO // 2 + 50, fila - 25), (globals.PANTALLA_ANCHO // 2 + 50, fila + 380), 2)
            pygame.draw.line(self.pantalla, globals.GRIS_CLARO, (globals.PANTALLA_ANCHO // 2 + 150, fila - 75), (globals.PANTALLA_ANCHO // 2 + 150, fila + 380), 2)
            pygame.draw.line(self.pantalla, globals.GRIS_CLARO, (globals.PANTALLA_ANCHO // 2 - 150, fila - 25), (globals.PANTALLA_ANCHO // 2 + 150, fila - 25), 2)
            pygame.draw.line(self.pantalla, globals.GRIS_CLARO, (globals.PANTALLA_ANCHO // 2 - 150, fila - 75), (globals.PANTALLA_ANCHO // 2 + 150, fila - 75), 2)
            pygame.draw.line(self.pantalla, globals.GRIS_CLARO, (globals.PANTALLA_ANCHO // 2 - 150, fila + 25), (globals.PANTALLA_ANCHO // 2 + 150, fila + 25), 2)
            pygame.draw.line(self.pantalla, globals.GRIS_CLARO, (globals.PANTALLA_ANCHO // 2 - 250, fila + 380), (globals.PANTALLA_ANCHO // 2 + 150, fila + 380), 2)
            pygame.draw.line(self.pantalla, globals.GRIS_CLARO, (globals.PANTALLA_ANCHO // 2 - 250, fila + 380), (globals.PANTALLA_ANCHO // 2 - 250, fila + 330), 2)
            pygame.draw.line(self.pantalla, globals.GRIS_CLARO, (globals.PANTALLA_ANCHO // 2 - 250, fila + 330), (globals.PANTALLA_ANCHO // 2 + 150, fila + 330), 2)

            self.pantalla.blit(medalla_oro, (globals.PANTALLA_ANCHO // 2 - 200, 130))
            self.pantalla.blit(medalla_plata, (globals.PANTALLA_ANCHO // 2 - 200, 180))
            self.pantalla.blit(medalla_bronce, (globals.PANTALLA_ANCHO // 2 - 200, 230))

            fila += 50

            matriz_puntuaciones = [[None, None, None] for _ in range(7)]

            facil_count = 0
            media_count = 0
            dificil_count = 0
            for puntuacion in puntuaciones:
                if puntuacion[0] == "facil" and facil_count < 7:
                    matriz_puntuaciones[facil_count][0] = str(round(float(puntuacion[1]) / 60, 2)) + " m"
                    facil_count += 1
                elif puntuacion[0] == "media" and media_count < 7:
                    matriz_puntuaciones[media_count][1] = str(round(float(puntuacion[1]) / 60, 2)) + " m"
                    media_count += 1
                elif puntuacion[0] == "dificil" and dificil_count < 7:
                    matriz_puntuaciones[dificil_count][2] = str(round(float(puntuacion[1]) / 60, 2)) + " m"
                    dificil_count += 1

            for i in range(6):
                if matriz_puntuaciones[i][0] is not None:
                    if i == 0:
                        texto_puntuacion_facil = fuente_negrita.render(str(matriz_puntuaciones[i][0]), True, globals.NEGRO)
                    else:
                        texto_puntuacion_facil = fuente.render(str(matriz_puntuaciones[i][0]), True, globals.NEGRO)
                    texto_puntuacion_facil_rect = texto_puntuacion_facil.get_rect(center=(globals.PANTALLA_ANCHO // 2 - 100, fila))
                    self.pantalla.blit(texto_puntuacion_facil, texto_puntuacion_facil_rect)

                if matriz_puntuaciones[i][1] is not None:
                    if i == 0:
                        texto_puntuacion_media = fuente_negrita.render(str(matriz_puntuaciones[i][1]), True, globals.NEGRO)
                    else:
                        texto_puntuacion_media = fuente.render(str(matriz_puntuaciones[i][1]), True, globals.NEGRO)
                    texto_puntuacion_media_rect = texto_puntuacion_media.get_rect(center=(globals.PANTALLA_ANCHO // 2, fila))
                    self.pantalla.blit(texto_puntuacion_media, texto_puntuacion_media_rect)

                if matriz_puntuaciones[i][2] is not None:
                    if i == 0:
                        texto_puntuacion_dificil = fuente_negrita.render(str(matriz_puntuaciones[i][2]), True, globals.NEGRO)
                    else:
                        texto_puntuacion_dificil = fuente.render(str(matriz_puntuaciones[i][2]), True, globals.NEGRO)
                    texto_puntuacion_dificil_rect = texto_puntuacion_dificil.get_rect(center=(globals.PANTALLA_ANCHO // 2 + 100, fila))
                    self.pantalla.blit(texto_puntuacion_dificil, texto_puntuacion_dificil_rect)

                fila += 50
            promedio_facil = sum(float(p[0].split(" ")[0]) for p in matriz_puntuaciones if p[0]) / facil_count if any(p[0] for p in matriz_puntuaciones) else 0
            promedio_media = sum(float(p[1].split(" ")[0]) for p in matriz_puntuaciones if p[1]) / media_count if any(p[1] for p in matriz_puntuaciones) else 0
            promedio_dificil = sum(float(p[2].split(" ")[0]) for p in matriz_puntuaciones if p[2]) / dificil_count if any(p[2] for p in matriz_puntuaciones) else 0

            texto_promedio_facil = fuente.render(f"{round(promedio_facil, 2)} m", True, globals.GRIS_CLARO)
            texto_promedio_facil_rect = texto_promedio_facil.get_rect(center=(globals.PANTALLA_ANCHO // 2 - 100, fila + 7))
            self.pantalla.blit(texto_promedio_facil, texto_promedio_facil_rect)

            texto_promedio_media = fuente.render(f"{round(promedio_media, 2)} m", True, globals.GRIS_CLARO)
            texto_promedio_media_rect = texto_promedio_media.get_rect(center=(globals.PANTALLA_ANCHO // 2, fila + 7))
            self.pantalla.blit(texto_promedio_media, texto_promedio_media_rect)

            texto_promedio_dificil = fuente.render(f"{round(promedio_dificil, 2)} m", True, globals.GRIS_CLARO)
            texto_promedio_dificil_rect = texto_promedio_dificil.get_rect(center=(globals.PANTALLA_ANCHO // 2 + 100, fila + 7))
            self.pantalla.blit(texto_promedio_dificil, texto_promedio_dificil_rect)

            pygame.display.flip()
            pygame.time.Clock().tick(globals.FPS)

    def seleccionar_dificultad(self):
        """
        Permite al jugador seleccionar la dificultad del juego.

        Muestra una pantalla con tres botones para elegir entre las dificultades Fácil, Medio y Difícil.
        Al hacer clic en uno de los botones, se establece la dificultad seleccionada y se sale de la pantalla de selección.

        Returns:
            int: El índice de la dificultad seleccionada (0 para Fácil, 1 para Medio, 2 para Difícil).
        """
        seleccionando_dificultad = True
        fondo = pygame.image.load(globals.RUTA_FONDO)
        fondo = pygame.transform.scale(fondo, (globals.PANTALLA_ANCHO, globals.PANTALLA_ALTO))

        while seleccionando_dificultad:
            self.pantalla.fill(globals.BLANCO)
            self.pantalla.blit(fondo, (0, 0))

            boton_facil = self.dibujar_boton("Fácil", 550, 150, 200, 50, globals.GRIS_CLARO, globals.AZUL1)
            boton_medio = self.dibujar_boton("Medio", 550, 250, 200, 50, globals.GRIS_CLARO, globals.AZUL1)
            boton_dificil = self.dibujar_boton("Difícil", 550, 350, 200, 50, globals.GRIS_CLARO, globals.AZUL1)

            boton_volver = self.dibujar_boton("Volver al menú", 550, 500, 200, 50, globals.GRIS_CLARO, globals.MORADO, self.mostrar_menu)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if boton_facil.collidepoint(mouse_pos):
                        seleccionando_dificultad = False
                        self.set_dificultad(0)
                    elif boton_medio.collidepoint(mouse_pos):
                        seleccionando_dificultad = False
                        self.set_dificultad(1)
                    elif boton_dificil.collidepoint(mouse_pos):
                        seleccionando_dificultad = False
                        self.set_dificultad(2)
                    elif boton_volver.collidepoint(mouse_pos):
                        seleccionando_dificultad = False
                        self.mostrar_menu()
                    
            pygame.display.flip()
            pygame.time.Clock().tick(globals.FPS)

            

        return self.dificultad

    def set_dificultad(self, dificultad):
        """
        Establece la dificultad del juego.

        Args:
            dificultad (int): El índice de la dificultad seleccionada (0 para Fácil, 1 para Medio, 2 para Difícil).
        """
        self.dificultad = dificultad

    def empezar_juego(self):
        """
        Inicia el juego de sudoku.

        Muestra la pantalla de carga y la selección de dificultad.
        Crea el tablero de sudoku y lo muestra en la pantalla.
        Permite al jugador interactuar con el tablero y realizar acciones como ingresar números, borrar celdas, pausar el juego, etc.
        Comprueba si el jugador ha completado correctamente el sudoku y muestra un mensaje de felicitación en caso afirmativo.

        """
        self.dificultad = self.seleccionar_dificultad()
        self.mostrar_pantalla_carga()
        self.instancia_sudoku.set_dificultad(self.dificultad)
        sudoku, resuelto = self.instancia_sudoku.crear_sudoku(self.config)
        self.tablero = tablero.Tablero(self.pantalla, sudoku, resuelto)
        self.iniciar_temporizador()

        en_juego = True
        celda_seleccionada = None
        cambio_en_tablero = True

        leyenda = pygame.image.load(globals.RUTA_LEYENDA)
        leyenda = pygame.transform.scale(leyenda, (235, 235))
        
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
                    else:
                        celda_seleccionada = None
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
                if globals.es_accesible():
                    self.pantalla.blit(leyenda, (globals.PANTALLA_ANCHO - 230, 270))
                if celda_seleccionada:
                    fila, columna = celda_seleccionada
                    self.iluminar_celdas(fila, columna)
                    self.iluminar_celda_seleccionada(fila, columna, globals.MORADO_CLARO, True)

                self.tablero.imprimir_numeros()
                self.tablero.imprimir_tablero()
                cambio_en_tablero = False

            logo_pausa = pygame.image.load(globals.RUTA_IMG_PAUSAR)
            logo_reanudar = pygame.image.load(globals.RUTA_IMG_INICIAR)

            logo_pausa = pygame.transform.scale(logo_pausa, (50, 50))
            logo_reanudar = pygame.transform.scale(logo_reanudar, (50, 50))

            hueco_x = globals.PANTALLA_ANCHO - 225
            self.dibujar_boton("Iniciar", hueco_x + 30, 50, 60, 50, globals.GRIS_CLARO, globals.AZUL2, self.iniciar_temporizador, logo_reanudar)
            self.dibujar_temporizador()
            if self.temporizador_iniciado or self.inicio_juego:
                self.dibujar_boton("Pausar", hueco_x + 110, 50, 60, 50, globals.GRIS_CLARO, globals.AZUL2, self.pausar_temporizador, logo_pausa)
            else:
                self.dibujar_boton("Continuar", hueco_x + 110, 50, 60, 50, globals.GRIS_CLARO, globals.AZUL2, self.pausar_temporizador, logo_reanudar)
            self.dibujar_boton("Comprobar", hueco_x, 110, 210, 50, globals.GRIS_CLARO, globals.AZUL1, self.comprobar_solucion)
            self.dibujar_boton("Mostrar Solución", hueco_x, 170, 210, 50, globals.GRIS_CLARO, globals.AZUL1, self.tablero.mostrar_solucion)
            self.dibujar_boton("Borrar Tablero", hueco_x, 230, 210, 50, globals.GRIS_CLARO, globals.AZUL1, self.tablero.borrar_tablero)
            self.dibujar_boton("Salir", hueco_x, 500, 210, 50, globals.GRIS_CLARO, globals.MORADO, self.salir_juego)

            self.actualizar_temporizador()
            self.dibujar_temporizador()
            

            pygame.display.flip()
            pygame.time.Clock().tick(globals.FPS)

    def comprobar_solucion(self):
        """
        Comprueba si el jugador ha completado correctamente el sudoku.

        Recorre todas las celdas del tablero y compara los valores ingresados por el jugador con los valores de la solución.
        Ilumina las celdas correctas en verde y las celdas incorrectas en morado, o de una forma diferente si la accesibilidad está activa.
        Muestra el tablero actualizado en la pantalla.

        """
        completo = True
        for fila in range(9):
            for columna in range(9):
                if self.tablero.sudoku[fila][columna] == self.tablero.resuelto[fila][columna]:
                    self.iluminar_celda_seleccionada(fila, columna, globals.VERDE_CLARO, False)
                else:
                    self.iluminar_celda_seleccionada(fila, columna, globals.MORADO_CLARO, False, True)
                    completo = False
        self.tablero.imprimir_numeros()
        self.tablero.imprimir_tablero()

        if completo:
            self.pausar_temporizador()
            confeti1 = pygame.image.load(globals.RUTA_IMG_CONFETI)
            confeti2 = pygame.image.load(globals.RUTA_IMG_CONFETI2)
            cortina_confeti = pygame.image.load(globals.RUTA_IMG_CORTINA_CONFETI)

            confeti1 = pygame.transform.scale(confeti1, (60, 60))
            confeti2 = pygame.transform.scale(confeti2, (60, 60))
            cortina_confeti = pygame.transform.scale(cortina_confeti, (globals.PANTALLA_ANCHO, globals.PANTALLA_ALTO))

            dificultad_texto = ["fácil", "media", "difícil"][self.dificultad]
            mensaje = "¡Enhorabuena! Has completado el sudoku."
            dificultad = f"Dificultad: {dificultad_texto}."
            minutos = int(self.tiempo_actual // 60)
            segundos = int(self.tiempo_actual % 60)
            tiempo = f"Tiempo: {minutos} minutos {segundos} segundos."


            rect_ventana = pygame.Rect(100, 200, 400, 200)
            sombra_rect = pygame.Rect(rect_ventana.topleft[0] + 5, rect_ventana.topleft[1] + 5, rect_ventana.width, rect_ventana.height)

            fuente = pygame.font.Font(globals.fuente, globals.TAM_FUENTE - 5)

            texto_enhorabuena = fuente.render(mensaje, True, globals.NEGRO)
            texto_dificultad = fuente.render(dificultad, True, globals.NEGRO)
            texto_tiempo = fuente.render(tiempo, True, globals.NEGRO)

            texto_enhorabuena_rect = texto_enhorabuena.get_rect(center=(rect_ventana.centerx, rect_ventana.centery - 30))
            texto_dificultad_rect = texto_dificultad.get_rect(center=rect_ventana.center)
            texto_tiempo_rect = texto_tiempo.get_rect(center=(rect_ventana.centerx, rect_ventana.centery + 30))
            
            self.pantalla.blit(cortina_confeti, (0, 0))

            pygame.draw.rect(self.pantalla, globals.GRIS_CLARO, sombra_rect, border_radius=globals.BORDER_RADIUS)
            pygame.draw.rect(self.pantalla, globals.MORADO_CLARO, rect_ventana, border_radius=globals.BORDER_RADIUS)

            self.pantalla.blit(texto_enhorabuena, texto_enhorabuena_rect)
            self.pantalla.blit(texto_dificultad, texto_dificultad_rect)
            self.pantalla.blit(texto_tiempo, texto_tiempo_rect)

            confeti1_rect = confeti1.get_rect(bottomleft=(110,390))
            confeti2_rect = confeti2.get_rect(bottomleft=(430,390))

            self.pantalla.blit(confeti1, confeti1_rect)
            self.pantalla.blit(confeti2, confeti2_rect)

            with open(globals.ARCHIVO_PUNTUACION, mode='a', newline='') as archivo:
                writer = csv.writer(archivo)
                writer.writerow([dificultad_texto.replace("á","a").replace("í","i"), self.tiempo_actual])


        pygame.display.update()

    def dibujar_temporizador(self):
        """
        Dibuja el temporizador en la pantalla.

        Muestra el tiempo transcurrido en el juego en formato MM:SS.

        """
        rect_temporizador = pygame.Rect(globals.PANTALLA_ANCHO - 170, 10, 100, 25)
        self.pantalla.fill((255, 255, 255), rect_temporizador)
        minutos = int(self.tiempo_actual // 60)
        segundos = int(self.tiempo_actual % 60)
        tiempo_formateado = f"{minutos:02}:{segundos:02}"
        texto = pygame.font.Font(globals.fuente, globals.TAM_FUENTE).render(tiempo_formateado, True, globals.NEGRO)
        self.pantalla.blit(texto, (globals.PANTALLA_ANCHO - 150, 10))

    def iniciar_temporizador(self):
        """
        Inicia el temporizador del juego.

        Reinicia el temporizador y marca el inicio del juego.

        """
        self.reiniciar_temporizador()
        self.temporizador_iniciado = True

    def pausar_temporizador(self):
        """
        Pausa o reanuda el temporizador del juego.

        Si el temporizador está en marcha, lo pausa y guarda el tiempo transcurrido.
        Si el temporizador está pausado, lo reanuda y ajusta el tiempo de inicio.

        """
        self.inicio_juego= False
        if self.temporizador_iniciado:
            self.tiempo_pausa = time.time() - self.tiempo_inicio
            self.temporizador_iniciado = False
        else:
            self.tiempo_inicio = time.time() - self.tiempo_pausa
            self.temporizador_iniciado = True
        time.sleep(0.1)

    def reiniciar_temporizador(self):
        """
        Reinicia el temporizador del juego.

        Establece el tiempo de inicio, el tiempo actual y el tiempo de pausa a cero.

        """
        self.tiempo_inicio = time.time()
        self.tiempo_actual = 0
        self.tiempo_pausa = 0

    def actualizar_temporizador(self):
        """
        Actualiza el temporizador del juego.

        Calcula el tiempo transcurrido desde el inicio del juego.

        """
        if self.temporizador_iniciado:
            self.tiempo_actual = time.time() - self.tiempo_inicio

    def salir_juego(self):
        """
        Sale del juego.

        Cierra la ventana del juego y finaliza el programa.

        """
        pygame.quit()
        sys.exit()

    def iluminar_celdas(self, fila, columna):
        """
        Ilumina las celdas del tablero.

        Ilumina las celdas del cuadrado 3x3 al que pertenece la celda seleccionada.
        Ilumina las celdas horizontales y verticales de la celda seleccionada.

        Args:
            fila (int): La fila de la celda seleccionada.
            columna (int): La columna de la celda seleccionada.

        """
        inicio_fila = (fila // 3) * 3
        inicio_columna = (columna // 3) * 3
        for i in range(3):
            for j in range(3):
                self.dibujar_rectangulo(inicio_fila + i, inicio_columna + j, globals.VERDE_CLARO, False)

        for i in range(9):
            self.dibujar_rectangulo(fila, i, globals.VERDE_CLARO, False)
            self.dibujar_rectangulo(i, columna, globals.VERDE_CLARO, False)

    def iluminar_celda_seleccionada(self, fila, columna, color, central, incorrecta=False):
        """
        Ilumina la celda seleccionada en el tablero.

        Ilumina la celda seleccionada con un color específico.

        Args:
            fila (int): La fila de la celda seleccionada.
            columna (int): La columna de la celda seleccionada.
            color (tuple): El color en formato RGB.
            central (bool): Indica si la celda seleccionada es la celda central del cuadrado 3x3.
            incorrecta (bool, optional): Indica si la celda seleccionada es incorrecta. Por defecto es False.

        """
        self.dibujar_rectangulo(fila, columna, color, central, incorrecta)

    def dibujar_rectangulo(self, fila, columna, color, central, incorrecta=False):
        """
        Dibuja un rectángulo en el tablero.

        Dibuja un rectángulo en la posición correspondiente del tablero con un color específico.

        Args:
            fila (int): La fila del rectángulo.
            columna (int): La columna del rectángulo.
            color (tuple): El color en formato RGB.
            central (bool): Indica si el rectángulo es el central del cuadrado 3x3.
            incorrecta (bool, optional): Indica si el número introducido es incorrecto para mostrarlo de manera accesible. Por defecto es False.

        """
        grosor_linea = 4 if (fila % 3 == 0 or columna % 3 == 0) else 1
        rect = pygame.Rect(
            globals.MARGEN + columna * globals.TAMAÑO_CELDA + grosor_linea // 2,
            globals.MARGEN + fila * globals.TAMAÑO_CELDA + grosor_linea // 2,
            globals.TAMAÑO_CELDA - grosor_linea + 2.5,
            globals.TAMAÑO_CELDA - grosor_linea + 2.5
        )
        
        pygame.draw.rect(self.pantalla, color, rect)
        if globals.es_accesible():
            if central:
                imagen_cruz = pygame.image.load(globals.RUTA_COLOREADO)
                imagen_cruz = pygame.transform.scale(imagen_cruz, (globals.TAMAÑO_CELDA - grosor_linea + 2.5, globals.TAMAÑO_CELDA - grosor_linea + 2.5))
                self.pantalla.blit(imagen_cruz, rect.topleft)
            elif incorrecta:
                imagen_cruz = pygame.image.load(globals.RUTA_CRUZ)
                imagen_cruz = pygame.transform.scale(imagen_cruz, (globals.TAMAÑO_CELDA - grosor_linea + 2.5, globals.TAMAÑO_CELDA - grosor_linea + 2.5))
                self.pantalla.blit(imagen_cruz, rect.topleft)

    def ver_tutorial(self):
        """
        Muestra el tutorial del juego.

        Muestra la primera página del tutorial en la pantalla.
        Permite al jugador navegar entre las diferentes páginas del tutorial.
        """
        en_tutorial = True

        tutorial = pygame.image.load(globals.RUTA_TUTORIAL_1)

        while en_tutorial:
            self.pantalla.fill(globals.BLANCO)

            self.pantalla.blit(tutorial, ((globals.PANTALLA_ANCHO - 600) // 2, 50))

            boton_volver = self.dibujar_boton("Volver al menú", (globals.PANTALLA_ANCHO - 700) // 2, globals.PANTALLA_ALTO - 90, 200, 50, globals.GRIS_CLARO, globals.MORADO)
            boton_siguiente = self.dibujar_boton("Siguiente", (globals.PANTALLA_ANCHO + 300) // 2, globals.PANTALLA_ALTO - 90, 200, 50, globals.GRIS_CLARO, globals.AZUL1)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = evento.pos
                    if boton_volver.collidepoint(mouse_pos):
                        en_tutorial = False
                        self.mostrar_menu()
                    elif boton_siguiente.collidepoint(mouse_pos):
                        en_tutorial = False
                        self.ver_tutorial_pagina2()
            
            pygame.display.flip()
            pygame.time.Clock().tick(globals.FPS)
    
    def ver_tutorial_pagina2(self):
        """
        Muestra la segunda página del tutorial.

        Muestra la segunda página del tutorial en la pantalla.
        Permite al jugador navegar entre las diferentes páginas del tutorial.
        """
        en_tutorial = True

        tutorial = pygame.image.load(globals.RUTA_TUTORIAL_2)

        while en_tutorial:
            self.pantalla.fill(globals.BLANCO)

            self.pantalla.blit(tutorial, ((globals.PANTALLA_ANCHO - 600) // 2, 50))

            boton_volver = self.dibujar_boton("Volver al menú", (globals.PANTALLA_ANCHO - 700) // 2, globals.PANTALLA_ALTO - 90, 200, 50, globals.GRIS_CLARO, globals.MORADO)
            boton_anterior = self.dibujar_boton("Anterior", (globals.PANTALLA_ANCHO - 200) // 2, globals.PANTALLA_ALTO - 90, 200, 50, globals.GRIS_CLARO, globals.AZUL1)
            boton_siguiente = self.dibujar_boton("Siguiente", (globals.PANTALLA_ANCHO + 300) // 2, globals.PANTALLA_ALTO - 90, 200, 50, globals.GRIS_CLARO, globals.AZUL1)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = evento.pos
                    if boton_volver.collidepoint(mouse_pos):
                        en_tutorial = False
                        self.mostrar_menu()
                    elif boton_anterior.collidepoint(mouse_pos):
                        en_tutorial = False
                        self.ver_tutorial()
                    elif boton_siguiente.collidepoint(mouse_pos):
                        en_tutorial = False
                        self.ver_tutorial_pagina3()
            
            pygame.display.flip()
            pygame.time.Clock().tick(globals.FPS)

    def ver_tutorial_pagina3(self):
        """
        Muestra la tercera página del tutorial.

        Muestra la tercera página del tutorial en la pantalla.
        Permite al jugador navegar entre las diferentes páginas del tutorial.
        """
        en_tutorial = True

        tutorial = pygame.image.load(globals.RUTA_TUTORIAL_3)

        while en_tutorial:
            self.pantalla.fill(globals.BLANCO)

            self.pantalla.blit(tutorial, ((globals.PANTALLA_ANCHO - 600) // 2, 50))

            boton_volver = self.dibujar_boton("Volver al menú", (globals.PANTALLA_ANCHO - 700) // 2, globals.PANTALLA_ALTO - 90, 200, 50, globals.GRIS_CLARO, globals.MORADO)
            boton_anterior = self.dibujar_boton("Anterior", (globals.PANTALLA_ANCHO - 200) // 2, globals.PANTALLA_ALTO - 90, 200, 50, globals.GRIS_CLARO, globals.AZUL1)
            boton_siguiente = self.dibujar_boton("Siguiente", (globals.PANTALLA_ANCHO + 300) // 2, globals.PANTALLA_ALTO - 90, 200, 50, globals.GRIS_CLARO, globals.AZUL1)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = evento.pos
                    if boton_volver.collidepoint(mouse_pos):
                        en_tutorial = False
                        self.mostrar_menu()
                    elif boton_anterior.collidepoint(mouse_pos):
                        en_tutorial = False
                        self.ver_tutorial_pagina2()
                    elif boton_siguiente.collidepoint(mouse_pos):
                        en_tutorial = False
                        self.ver_tutorial_pagina4()
            
            pygame.display.flip()
            pygame.time.Clock().tick(globals.FPS)

    def ver_tutorial_pagina4(self):
        """
        Muestra la cuarta página del tutorial.

        Muestra la cuarta página del tutorial en la pantalla.
        Permite al jugador navegar entre las diferentes páginas del tutorial.
        """
        en_tutorial = True

        tutorial = pygame.image.load(globals.RUTA_TUTORIAL_4)

        while en_tutorial:
            self.pantalla.fill(globals.BLANCO)

            self.pantalla.blit(tutorial, ((globals.PANTALLA_ANCHO - 600) // 2, 50))

            boton_volver = self.dibujar_boton("Volver al menú", (globals.PANTALLA_ANCHO - 700) // 2, globals.PANTALLA_ALTO - 90, 200, 50, globals.GRIS_CLARO, globals.MORADO)
            boton_anterior = self.dibujar_boton("Anterior", (globals.PANTALLA_ANCHO - 200) // 2, globals.PANTALLA_ALTO - 90, 200, 50, globals.GRIS_CLARO, globals.AZUL1)
            boton_siguiente = self.dibujar_boton("Siguiente", (globals.PANTALLA_ANCHO + 300) // 2, globals.PANTALLA_ALTO - 90, 200, 50, globals.GRIS_CLARO, globals.AZUL1)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = evento.pos
                    if boton_volver.collidepoint(mouse_pos):
                        en_tutorial = False
                        self.mostrar_menu()
                    elif boton_anterior.collidepoint(mouse_pos):
                        en_tutorial = False
                        self.ver_tutorial_pagina3()
                    elif boton_siguiente.collidepoint(mouse_pos):
                        en_tutorial = False
                        self.ver_tutorial_pagina5()
            
            pygame.display.flip()
            pygame.time.Clock().tick(globals.FPS)

    def ver_tutorial_pagina5(self):
        """
        Muestra la quinta página del tutorial.

        Muestra la quinta página del tutorial en la pantalla.
        Permite al jugador navegar entre las diferentes páginas del tutorial.
        """
        en_tutorial = True

        tutorial = pygame.image.load(globals.RUTA_TUTORIAL_5)

        while en_tutorial:
            self.pantalla.fill(globals.BLANCO)

            self.pantalla.blit(tutorial, ((globals.PANTALLA_ANCHO - 600) // 2, 50))

            boton_volver = self.dibujar_boton("Volver al menú", (globals.PANTALLA_ANCHO - 700) // 2, globals.PANTALLA_ALTO - 90, 200, 50, globals.GRIS_CLARO, globals.MORADO)
            boton_anterior = self.dibujar_boton("Anterior", (globals.PANTALLA_ANCHO - 200) // 2, globals.PANTALLA_ALTO - 90, 200, 50, globals.GRIS_CLARO, globals.AZUL1)
            boton_siguiente = self.dibujar_boton("Siguiente", (globals.PANTALLA_ANCHO + 300) // 2, globals.PANTALLA_ALTO - 90, 200, 50, globals.GRIS_CLARO, globals.AZUL1)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = evento.pos
                    if boton_volver.collidepoint(mouse_pos):
                        en_tutorial = False
                        self.mostrar_menu()
                    elif boton_anterior.collidepoint(mouse_pos):
                        en_tutorial = False
                        self.ver_tutorial_pagina4()
                    elif boton_siguiente.collidepoint(mouse_pos):
                        en_tutorial = False
                        self.ver_tutorial_pagina6()
            
            pygame.display.flip()
            pygame.time.Clock().tick(globals.FPS)

    def ver_tutorial_pagina6(self):
        """
        Muestra la sexta página del tutorial.

        Muestra la sexta página del tutorial en la pantalla.
        Permite al jugador navegar entre las diferentes páginas del tutorial.
        """
        en_tutorial = True

        tutorial = pygame.image.load(globals.RUTA_TUTORIAL_6)

        while en_tutorial:
            self.pantalla.fill(globals.BLANCO)

            self.pantalla.blit(tutorial, ((globals.PANTALLA_ANCHO - 600) // 2, 50))

            boton_volver = self.dibujar_boton("Volver al menú", (globals.PANTALLA_ANCHO - 700) // 2, globals.PANTALLA_ALTO - 90, 200, 50, globals.GRIS_CLARO, globals.MORADO)
            boton_anterior = self.dibujar_boton("Anterior", (globals.PANTALLA_ANCHO - 200) // 2, globals.PANTALLA_ALTO - 90, 200, 50, globals.GRIS_CLARO, globals.AZUL1)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = evento.pos
                    if boton_volver.collidepoint(mouse_pos):
                        en_tutorial = False
                        self.mostrar_menu()
                    elif boton_anterior.collidepoint(mouse_pos):
                        en_tutorial = False
                        self.ver_tutorial_pagina5()
            
            pygame.display.flip()
            pygame.time.Clock().tick(globals.FPS)

    def ver_creditos(self):
        """
        Muestra la pantalla de créditos.

        Muestra la pantalla de créditos en la que se muestra información sobre el trabajo de fin de grado, el autor y el tutor.
        Permite al jugador volver al menú principal.
        """
        en_creditos = True
        
        fondo = pygame.image.load(globals.RUTA_FONDO_PUNTUACION)
        fondo = pygame.transform.scale(fondo, (globals.PANTALLA_ANCHO, globals.PANTALLA_ALTO))

        fuente_normal = pygame.font.Font(globals.fuente, globals.TAM_FUENTE - 5)
        fuente_titulo_negrita = pygame.font.Font(globals.fuente_negrita, globals.TAM_FUENTE + 10)

        logo_uja = pygame.image.load(globals.RUTA_LOGO_UJA)
        logo_uja = pygame.transform.scale(logo_uja, (200, 70))

        logo_epsj = pygame.image.load(globals.RUTA_LOGO_EPSJ)
        logo_epsj = pygame.transform.scale(logo_epsj, (150, 80))


        while en_creditos:
            
            self.pantalla.fill(globals.BLANCO)
            self.pantalla.blit(fondo, (0, 0))

            self.pantalla.blit(logo_uja, ((globals.PANTALLA_ANCHO // 2) - 200, globals.PANTALLA_ALTO - 200))
            self.pantalla.blit(logo_epsj, ((globals.PANTALLA_ANCHO // 2) + 20, globals.PANTALLA_ALTO - 200))

            boton_volver = self.dibujar_boton("Volver al menú", (globals.PANTALLA_ANCHO - 200) // 2, globals.PANTALLA_ALTO - 110, 200, 50, globals.GRIS_CLARO, globals.MORADO)

            texto_titulo = fuente_titulo_negrita.render("Créditos", True, globals.NEGRO)
            texto_titulo_rect = texto_titulo.get_rect(center=(globals.PANTALLA_ANCHO // 2, 70))
            self.pantalla.blit(texto_titulo, texto_titulo_rect)

            texto_tfg = fuente_normal.render("Trabajo de Fin de Grado de Ingeniería Informática", True, globals.NEGRO)
            texto_tfg_rect = texto_tfg.get_rect(center=(globals.PANTALLA_ANCHO // 2, 160))
            self.pantalla.blit(texto_tfg, texto_tfg_rect)
            
            texto_nombre = fuente_normal.render("Hecho por: María de las Maravillas Luque Carmona", True, globals.NEGRO)
            texto_nombre_rect = texto_nombre.get_rect(center=(globals.PANTALLA_ANCHO // 2, 200))
            self.pantalla.blit(texto_nombre, texto_nombre_rect)

            texto_tutor = fuente_normal.render("Tutor: Ángel Luis García Fernandez", True, globals.NEGRO)
            texto_tutor_rect = texto_tutor.get_rect(center=(globals.PANTALLA_ANCHO // 2, 240))
            self.pantalla.blit(texto_tutor, texto_tutor_rect)

            texto_tfg = fuente_normal.render("Universidad de Jaén", True, globals.NEGRO)
            texto_tfg_rect = texto_tfg.get_rect(center=(globals.PANTALLA_ANCHO // 2, 280))
            self.pantalla.blit(texto_tfg, texto_tfg_rect)

            texto_dept = fuente_normal.render("Departamento de informática", True, globals.NEGRO)
            texto_dept_rect = texto_dept.get_rect(center=(globals.PANTALLA_ANCHO // 2, 320))
            self.pantalla.blit(texto_dept, texto_dept_rect)
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if boton_volver.collidepoint(evento.pos):
                        en_creditos = False
                        self.mostrar_menu()
        
            pygame.display.flip()

    def ajustes(self):
        """
        Muestra la pantalla de ajustes.

        Muestra la pantalla de ajustes en la que se pueden modificar diferentes configuraciones del juego, como el modo de accesibilidad y la dificultad.
        Permite al jugador volver al menú principal.
        """
        en_ajustes = True
        
        fondo = pygame.image.load(globals.RUTA_FONDO_PUNTUACION)
        fondo = pygame.transform.scale(fondo, (globals.PANTALLA_ANCHO, globals.PANTALLA_ALTO))
        
        fuente_columnas = pygame.font.Font(globals.fuente, globals.TAM_FUENTE)
        fuente_titulo_negrita = pygame.font.Font(globals.fuente_negrita, globals.TAM_FUENTE + 10)

        while en_ajustes:
            self.pantalla.fill(globals.BLANCO)
            
            self.pantalla.blit(fondo, (0, 0))
    
            boton_volver = self.dibujar_boton("Volver al menú", (globals.PANTALLA_ANCHO - 200) // 2, globals.PANTALLA_ALTO - 110, 200, 50, globals.GRIS_CLARO, globals.MORADO)
    
            texto_titulo = fuente_titulo_negrita.render("Ajustes", True, globals.NEGRO)
            texto_titulo_rect = texto_titulo.get_rect(center=(globals.PANTALLA_ANCHO // 2, 40))
            self.pantalla.blit(texto_titulo, texto_titulo_rect)

            texto_modo_accesibilidad = fuente_columnas.render("Modo accesibilidad", True, globals.NEGRO)
            texto_modo_accesibilidad_rect = texto_modo_accesibilidad.get_rect(center=(globals.PANTALLA_ANCHO // 2, 140))
            self.pantalla.blit(texto_modo_accesibilidad, texto_modo_accesibilidad_rect)

            boton_activar = self.dibujar_boton("Activar", (globals.PANTALLA_ANCHO - 450) // 2, 190, 200, 50, globals.GRIS_CLARO, globals.AZUL1)
            boton_desactivar = self.dibujar_boton("Desactivar", (globals.PANTALLA_ANCHO + 50) // 2, 190, 200, 50, globals.GRIS_CLARO, globals.AZUL1)

            estado_accesibilidad = "Activado" if globals.es_accesible() else "Desactivado"
            texto_estado_accesibilidad = fuente_columnas.render(f"Accesibilidad: {estado_accesibilidad}", True, globals.NEGRO)
            texto_estado_accesibilidad_rect = texto_estado_accesibilidad.get_rect(center=(globals.PANTALLA_ANCHO // 2, 310))
            self.pantalla.blit(texto_estado_accesibilidad, texto_estado_accesibilidad_rect)

            pygame.draw.line(self.pantalla, globals.GRIS_CLARO, (150, 340), (globals.PANTALLA_ANCHO - 150, 340), 2)

            texto_configuracion_dificultad = fuente_columnas.render("Nivel de dificultad (modo difícil)", True, globals.NEGRO)
            texto_configuracion_dificultad_rect = texto_configuracion_dificultad.get_rect(center=(globals.PANTALLA_ANCHO // 2, 390))
            self.pantalla.blit(texto_configuracion_dificultad, texto_configuracion_dificultad_rect)

            boton_reducir_dificultad = self.dibujar_boton("-", (globals.PANTALLA_ANCHO - 130) // 2, 420, 40, 40, globals.GRIS_CLARO, globals.AZUL2)
            
            texto_dificultad = fuente_columnas.render(str(self.config["dificil"]), True, globals.NEGRO)
            texto_dificultad_rect = texto_dificultad.get_rect(center=(globals.PANTALLA_ANCHO // 2, 440))
            self.pantalla.blit(texto_dificultad, texto_dificultad_rect)

            boton_aumentar_dificultad = self.dibujar_boton("+", (globals.PANTALLA_ANCHO + 50) // 2, 420, 40, 40, globals.GRIS_CLARO, globals.AZUL2)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if boton_volver.collidepoint(evento.pos):
                        en_ajustes = False
                        self.mostrar_menu()
                    elif boton_activar.collidepoint(evento.pos):
                        self.toggle_accesibilidad(accesible=True)
                    elif boton_desactivar.collidepoint(evento.pos):
                        self.toggle_accesibilidad(accesible=False)
                    elif boton_reducir_dificultad.collidepoint(evento.pos):
                        self.modificar_dificultad_dificil(-1)
                    elif boton_aumentar_dificultad.collidepoint(evento.pos):
                        self.modificar_dificultad_dificil(1)
                    
            pygame.display.flip()
            pygame.time.Clock().tick(globals.FPS)

    def modificar_dificultad_dificil(self, cambio):
        """
        Modifica la dificultad del modo difícil.

        Parámetros:
        - cambio: entero que indica el cambio en la dificultad (positivo o negativo)

        La función modifica el valor de la dificultad del modo difícil en la configuración del juego.
        Si el valor de la dificultad supera el límite máximo (7) o el límite mínimo (1), se ajusta al límite correspondiente.
        Si el valor de la dificultad es mayor a 5, muestra un aviso indicando que puede generar sudokus con múltiples soluciones.
        """
        self.config["dificil"] = max(1, min(7, int(self.config["dificil"]) + cambio))
        if int(self.config["dificil"]) > 5:
            aviso = True
            while aviso:
                rectangulo = pygame.Rect(globals.PANTALLA_ANCHO // 2 - 200, globals.PANTALLA_ALTO // 2 - 100, 400, 200)
                pygame.draw.rect(self.pantalla, globals.GRIS, rectangulo)
                pygame.draw.rect(self.pantalla, globals.GRIS_CLARO, rectangulo, 4)
                fuente = pygame.font.Font(globals.fuente, 20)
                texto = "Atención, subir la dificultad por encima de 5 puede ocasionar la generación de sudokus con múltiples soluciones."
                palabras = texto.split()
                lineas = []
                linea_actual = palabras[0]
                for palabra in palabras[1:]:
                    if fuente.size(linea_actual + " " + palabra)[0] <= rectangulo.width - 20:
                        linea_actual += " " + palabra
                    else:
                        lineas.append(linea_actual)
                        linea_actual = palabra
                lineas.append(linea_actual)
                for i, linea in enumerate(lineas):
                    texto_linea = fuente.render(linea, True, globals.NEGRO)
                    texto_linea_rect = texto_linea.get_rect(center=(rectangulo.centerx, rectangulo.centery - 40 + i * 30))
                    self.pantalla.blit(texto_linea, texto_linea_rect)

                boton_aceptar = self.dibujar_boton("Aceptar", globals.PANTALLA_ANCHO // 2 - 50, globals.PANTALLA_ALTO // 2 + 50, 100, 40, globals.GRIS_CLARO, globals.MORADO)
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif evento.type == pygame.MOUSEBUTTONDOWN:
                        if boton_aceptar.collidepoint(evento.pos):
                            aviso = False
                pygame.display.flip()


        with open(globals.ARCHIVO_CONFIGURACION, mode='r', newline='') as archivo:
            lines = archivo.readlines()
    
        with open(globals.ARCHIVO_CONFIGURACION, mode='w', newline='') as archivo:
            archivo.write("")
            writer = csv.writer(archivo)
            comprobado = False
            for line in lines:
                if not comprobado and "Configuracion" in line:
                    writer.writerow(["Configuracion", "Valor"])
                    comprobado = True
                elif "dificil" in line:
                    writer.writerow(["dificil", self.config["dificil"]])
                else:
                    writer.writerow(line.strip().split(','))

    def toggle_accesibilidad(self, accesible):
        """
        Cambia el estado de accesibilidad del juego.

        Parámetros:
        - accesible: booleano que indica si el modo de accesibilidad debe estar activado o desactivado

        La función modifica el valor del modo de accesibilidad en la configuración del juego.
        """
        with open(globals.ARCHIVO_CONFIGURACION, mode='r', newline='') as archivo:
            lines = archivo.readlines()
    
        with open(globals.ARCHIVO_CONFIGURACION, mode='w', newline='') as archivo:
            archivo.write("")
            writer = csv.writer(archivo)
            comprobado = False
            for line in lines:
                if not comprobado and "Configuracion" in line:
                    writer.writerow(["Configuracion", "Valor"])
                    comprobado = True
                elif "accesibilidad" in line:
                    writer.writerow(["accesibilidad", str(accesible)])
                else:
                    writer.writerow(line.strip().split(','))

    def mostrar_menu(self):
        """
        Muestra el menú principal del juego.

        Muestra los diferentes botones del menú (Empezar, Tutorial, Créditos, Ajustes, Puntuación, Salir) en la pantalla.
        Permite al jugador interactuar con los botones y realizar diferentes acciones según el botón seleccionado.
        """
        en_menu = True

        fondo = pygame.image.load(globals.RUTA_FONDO)
        fondo = pygame.transform.scale(fondo, (globals.PANTALLA_ANCHO, globals.PANTALLA_ALTO))

        while en_menu:

            self.pantalla.fill(globals.BLANCO)
            self.pantalla.blit(fondo, (0, 0))
            
            boton_empezar = self.dibujar_boton("Empezar", 550, 50, 200, 50, globals.GRIS_CLARO, globals.AZUL1, self.empezar_juego)
            boton_tutorial = self.dibujar_boton("Tutorial", 550, 130, 200, 50, globals.GRIS_CLARO, globals.AZUL1, self.ver_tutorial)
            boton_creditos = self.dibujar_boton("Créditos", 550, 210, 200, 50, globals.GRIS_CLARO, globals.AZUL1, self.ver_creditos)
            boton_ajustes = self.dibujar_boton("Ajustes", 550, 290, 200, 50, globals.GRIS_CLARO, globals.AZUL1, self.ajustes)
            boton_puntuacion = self.dibujar_boton("Puntuación", 550, 370, 200, 50, globals.GRIS_CLARO, globals.AZUL1, self.mostrar_puntuacion)
            boton_salir = self.dibujar_boton("Salir", 550, 500, 200, 50, globals.GRIS_CLARO, globals.MORADO)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = evento.pos
                    if boton_empezar.collidepoint(mouse_pos):
                        self.empezar_juego()
                        en_menu = False
                    elif boton_tutorial.collidepoint(mouse_pos):
                        self.ver_tutorial()
                        en_menu = False
                    elif boton_creditos.collidepoint(mouse_pos):
                        self.ver_creditos()
                        en_menu = False
                    elif boton_salir.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    elif boton_puntuacion.collidepoint(mouse_pos):
                        self.mostrar_puntuacion()
                        en_menu = False
                    elif boton_ajustes.collidepoint(mouse_pos):
                        self.ajustes()
                        en_menu = False

            pygame.display.flip()
            pygame.time.Clock().tick(globals.FPS)