import pygame
import sys
import numpy as np
import globals
import random
import time
import os
import csv

class Juego:
    def __init__(self, pantalla, sudoku_instance):
        self.pantalla = pantalla
        self.boton_comprobar = pygame.Rect(100, 400, 200, 50)
        self.temporizador_iniciado = False
        self.seleccionando_dificultad = False
        self.tiempo_inicio = 0
        self.tiempo_actual = 0
        self.tiempo_pausa = 0
        self.instancia_sudoku = sudoku_instance
        self.inicio_juego = True
        self.dificultad = 0
        

    def dibujar_boton(self, mensaje, x, y, ancho, alto, color_inactivo, color_activo, accion=None, logo=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = pygame.Rect(x, y, ancho, alto)

        # Sombra
        sombra_rect = rect.copy()
        sombra_rect.topleft = (rect.topleft[0] + 5, rect.topleft[1] + 5)
        pygame.draw.rect(self.pantalla, globals.GRIS, sombra_rect, border_radius=globals.BORDER_RADIUS)

        if rect.collidepoint(mouse):
            pygame.draw.rect(self.pantalla, color_activo, rect, border_radius=globals.BORDER_RADIUS)
            if click[0] == 1 and accion is not None:
                accion()
        else:
            pygame.draw.rect(self.pantalla, color_inactivo, rect, border_radius=globals.BORDER_RADIUS)

        # Añadir logo centrado si se proporciona
        if logo:
            logo_rect = logo.get_rect()
            logo_rect.center = rect.center
            self.pantalla.blit(logo, logo_rect)
        else:
            # Añadir texto centrado
            fuente = pygame.font.Font(globals.fuente, globals.TAM_FUENTE)
            texto = fuente.render(mensaje, True, globals.BLANCO)
            texto_rect = texto.get_rect(center=rect.center)
            self.pantalla.blit(texto, texto_rect)

        

        return rect

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

    def mostrar_puntuacion(self):
        en_puntuacion = True

        puntuaciones = []
        with open(globals.ARCHIVO_PUNTUACION, mode='r', newline='') as archivo:
            reader = csv.reader(archivo)
            next(reader)  # Saltar la cabecera
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
            boton_volver = self.dibujar_boton("Volver al menú", (globals.PANTALLA_ANCHO - 200) // 2, globals.PANTALLA_ALTO - 100, 200, 50, globals.GRIS_CLARO, globals.MORADO_CLARO, self.mostrar_menu)

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
            fuente_columnas = pygame.font.Font(globals.fuente, globals.TAM_FUENTE)
            fuente_titulo = pygame.font.Font(globals.fuente, globals.TAM_FUENTE + 10)
            fuente_negrita = pygame.font.Font(globals.fuente_negrita, globals.TAM_FUENTE_PUNTUACION)
            fuente_columnas_negrita = pygame.font.Font(globals.fuente_negrita, globals.TAM_FUENTE)
            fuente_titulo_negrita = pygame.font.Font(globals.fuente_negrita, globals.TAM_FUENTE + 10)
            texto_titulo = fuente_titulo_negrita.render("Puntuaciones", True, globals.NEGRO)
            texto_titulo_rect = texto_titulo.get_rect(center=(globals.PANTALLA_ANCHO // 2, 50))
            self.pantalla.blit(texto_titulo, texto_titulo_rect)

            fila = 100
            # Cabecera de la tabla
            texto_cabecera = fuente_columnas_negrita.render("Fácil", True, globals.NEGRO)
            texto_cabecera_rect = texto_cabecera.get_rect(center=(globals.PANTALLA_ANCHO // 2 - 100, fila))
            self.pantalla.blit(texto_cabecera, texto_cabecera_rect)

            texto_cabecera = fuente_columnas_negrita.render("Media", True, globals.NEGRO)
            texto_cabecera_rect = texto_cabecera.get_rect(center=(globals.PANTALLA_ANCHO // 2, fila))
            self.pantalla.blit(texto_cabecera, texto_cabecera_rect)

            texto_cabecera = fuente_columnas_negrita.render("Difícil", True, globals.NEGRO)
            texto_cabecera_rect = texto_cabecera.get_rect(center=(globals.PANTALLA_ANCHO // 2 + 100, fila))
            self.pantalla.blit(texto_cabecera, texto_cabecera_rect)

            # Líneas separadoras
            pygame.draw.line(self.pantalla, globals.GRIS_CLARO, (globals.PANTALLA_ANCHO // 2 - 50, fila - 25), (globals.PANTALLA_ANCHO // 2 - 50, fila + 380), 2)
            pygame.draw.line(self.pantalla, globals.GRIS_CLARO, (globals.PANTALLA_ANCHO // 2 - 150, fila - 75), (globals.PANTALLA_ANCHO // 2 - 150, fila + 380), 2)
            pygame.draw.line(self.pantalla, globals.GRIS_CLARO, (globals.PANTALLA_ANCHO // 2 + 50, fila - 25), (globals.PANTALLA_ANCHO // 2 + 50, fila + 380), 2)
            pygame.draw.line(self.pantalla, globals.GRIS_CLARO, (globals.PANTALLA_ANCHO // 2 + 150, fila - 75), (globals.PANTALLA_ANCHO // 2 + 150, fila + 380), 2)
            pygame.draw.line(self.pantalla, globals.GRIS_CLARO, (globals.PANTALLA_ANCHO // 2 - 150, fila - 25), (globals.PANTALLA_ANCHO // 2 + 150, fila - 25), 2)
            pygame.draw.line(self.pantalla, globals.GRIS_CLARO, (globals.PANTALLA_ANCHO // 2 - 150, fila - 75), (globals.PANTALLA_ANCHO // 2 + 150, fila - 75), 2)
            pygame.draw.line(self.pantalla, globals.GRIS_CLARO, (globals.PANTALLA_ANCHO // 2 - 150, fila + 25), (globals.PANTALLA_ANCHO // 2 + 150, fila + 25), 2)
            pygame.draw.line(self.pantalla, globals.GRIS_CLARO, (globals.PANTALLA_ANCHO // 2 - 150, fila + 380), (globals.PANTALLA_ANCHO // 2 + 150, fila + 380), 2)

            self.pantalla.blit(medalla_oro, (globals.PANTALLA_ANCHO // 2 - 200, 130))
            self.pantalla.blit(medalla_plata, (globals.PANTALLA_ANCHO // 2 - 200, 180))
            self.pantalla.blit(medalla_bronce, (globals.PANTALLA_ANCHO // 2 - 200, 230))

            fila += 50

            # Crear matriz para almacenar las puntuaciones
            matriz_puntuaciones = [[None, None, None] for _ in range(7)]

            # Mostrar las primeras 7 puntuaciones de cada dificultad
            facil_count = 0
            media_count = 0
            dificil_count = 0
            for puntuacion in puntuaciones:
                if puntuacion[0] == "facil" and facil_count < 7:
                    matriz_puntuaciones[facil_count][0] = str(round(float(puntuacion[1]), 4))
                    facil_count += 1
                elif puntuacion[0] == "media" and media_count < 7:
                    matriz_puntuaciones[media_count][1] = str(round(float(puntuacion[1]), 4))
                    media_count += 1
                elif puntuacion[0] == "dificil" and dificil_count < 7:
                    matriz_puntuaciones[dificil_count][2] = str(round(float(puntuacion[1]), 4))
                    dificil_count += 1

            # Mostrar la matriz en formato tabla
            for i in range(7):
                if i == 0:
                    texto_puntuacion_facil = fuente_negrita.render(matriz_puntuaciones[i][0], True, globals.NEGRO)
                    texto_puntuacion_media = fuente_negrita.render(matriz_puntuaciones[i][1], True, globals.NEGRO)
                    texto_puntuacion_dificil = fuente_negrita.render(matriz_puntuaciones[i][2], True, globals.NEGRO)
                else:
                    texto_puntuacion_facil = fuente.render(matriz_puntuaciones[i][0], True, globals.NEGRO)
                    texto_puntuacion_media = fuente.render(matriz_puntuaciones[i][1], True, globals.NEGRO)
                    texto_puntuacion_dificil = fuente.render(matriz_puntuaciones[i][2], True, globals.NEGRO)

                texto_puntuacion_facil_rect = texto_puntuacion_facil.get_rect(center=(globals.PANTALLA_ANCHO // 2 - 100, fila))
                texto_puntuacion_media_rect = texto_puntuacion_media.get_rect(center=(globals.PANTALLA_ANCHO // 2, fila))
                texto_puntuacion_dificil_rect = texto_puntuacion_dificil.get_rect(center=(globals.PANTALLA_ANCHO // 2 + 100, fila))

                self.pantalla.blit(texto_puntuacion_facil, texto_puntuacion_facil_rect)
                self.pantalla.blit(texto_puntuacion_media, texto_puntuacion_media_rect)
                self.pantalla.blit(texto_puntuacion_dificil, texto_puntuacion_dificil_rect)

                fila += 50

            pygame.display.flip()
            pygame.time.Clock().tick(60) # 60 FPS

            

    def seleccionar_dificultad(self):
        self.seleccionando_dificultad = True
        fondo = pygame.image.load(globals.RUTA_FONDO)
        fondo = pygame.transform.scale(fondo, (globals.PANTALLA_ANCHO, globals.PANTALLA_ALTO))

        while self.seleccionando_dificultad:
            self.pantalla.fill(globals.BLANCO)
            self.pantalla.blit(fondo, (0, 0))

            boton_facil = self.dibujar_boton("Fácil", 550, 150, 200, 50, globals.GRIS_CLARO, globals.VERDE)
            boton_medio = self.dibujar_boton("Medio", 550, 250, 200, 50, globals.GRIS_CLARO, globals.AMARILLO)
            boton_dificil = self.dibujar_boton("Difícil", 550, 350, 200, 50, globals.GRIS_CLARO, globals.ROJO)

            boton_volver = self.dibujar_boton("Volver al menú", 550, 500, 200, 50, globals.GRIS_CLARO, globals.MORADO_CLARO, self.mostrar_menu)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if boton_facil.collidepoint(mouse_pos):
                        self.seleccionando_dificultad = False
                        self.set_dificultad(0)
                    elif boton_medio.collidepoint(mouse_pos):
                        self.seleccionando_dificultad = False
                        self.set_dificultad(1)
                    elif boton_dificil.collidepoint(mouse_pos):
                        self.seleccionando_dificultad = False
                        self.set_dificultad(2)
                    elif boton_volver.collidepoint(mouse_pos):
                        self.seleccionando_dificultad = False
                        self.mostrar_menu()
                    

                

            pygame.display.flip()
            pygame.time.Clock().tick(60) # 60 FPS

            

        return self.dificultad

    def set_dificultad(self, dificultad):
        self.dificultad = dificultad
        self.seleccionando_dificultad = False

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
            # Cargar imágenes
            logo_pausa = pygame.image.load(globals.RUTA_IMG_PAUSAR)
            logo_reanudar = pygame.image.load(globals.RUTA_IMG_INICIAR)

            # Escalar imágenes al tamaño adecuado
            logo_pausa = pygame.transform.scale(logo_pausa, (50, 50))
            logo_reanudar = pygame.transform.scale(logo_reanudar, (50, 50))

            hueco_x = globals.PANTALLA_ANCHO - 225
            self.dibujar_boton("Iniciar", hueco_x + 30, 50, 60, 50, globals.GRIS_CLARO, globals.VERDE, self.iniciar_temporizador, logo_reanudar)
            self.dibujar_temporizador()
            if self.temporizador_iniciado or self.inicio_juego:
                self.dibujar_boton("Pausar", hueco_x + 110, 50, 60, 50, globals.GRIS_CLARO, globals.ROJO, self.pausar_temporizador, logo_pausa)
            else:
                self.dibujar_boton("Continuar", hueco_x + 110, 50, 60, 50, globals.GRIS_CLARO, globals.ROJO, self.pausar_temporizador, logo_reanudar)
            self.dibujar_boton("Comprobar", hueco_x, 110, 210, 50, globals.GRIS_CLARO, globals.AZUL, self.comprobar_solucion)
            self.dibujar_boton("Mostrar Solución", hueco_x, 170, 210, 50, globals.GRIS_CLARO, globals.AMARILLO, self.tablero.mostrar_solucion)
            self.dibujar_boton("Borrar Tablero", hueco_x, 230, 210, 50, globals.GRIS_CLARO, globals.NARANJA, self.tablero.borrar_tablero)
            self.dibujar_boton("Salir", hueco_x, 500, 210, 50, globals.GRIS_CLARO, globals.MORADO_CLARO, self.salir_juego)
            
            #TODO: ELIMINAR ESTO
            # Dibujar dificultad
            fuente = pygame.font.Font(globals.fuente, globals.TAM_FUENTE)
            texto_dificultad = fuente.render(f"Dificultad: {self.dificultad}", True, globals.NEGRO)

            self.pantalla.blit(texto_dificultad, (globals.PANTALLA_ANCHO - 200, 450))

            self.actualizar_temporizador()
            self.dibujar_temporizador()
            

            pygame.display.flip()
            pygame.time.Clock().tick(60) # 60 FPS

    def comprobar_solucion(self):
        completo = True
        for fila in range(9):
            for columna in range(9):
                if self.tablero.sudoku[fila][columna] == self.tablero.resuelto[fila][columna]:
                    self.iluminar_celda_seleccionada(fila, columna, globals.VERDE_CLARO)  # Celda correcta
                else:
                    self.iluminar_celda_seleccionada(fila, columna, globals.MORADO_CLARO)  # Celda incorrecta
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
            tiempo = f"Tiempo: {self.tiempo_actual:.2f} segundos."


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
        rect_temporizador = pygame.Rect(globals.PANTALLA_ANCHO - 170, 10, 100, 25)
        self.pantalla.fill((255, 255, 255), rect_temporizador)
        minutos = int(self.tiempo_actual // 60)
        segundos = int(self.tiempo_actual % 60)
        tiempo_formateado = f"{minutos:02}:{segundos:02}"
        texto = pygame.font.Font(globals.fuente, globals.TAM_FUENTE).render(tiempo_formateado, True, globals.NEGRO)
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

    def ver_creditos(self):
        #TODO: ARREGLAR ESTO
        mi_foto_original = pygame.image.load(globals.RUTA_FOTO)  # Carga la foto
        mi_foto = pygame.transform.scale(mi_foto_original, (130, 170))  # Redimensiona la foto
    
        margen_derecho = 10  # Margen derecho en píxeles
        margen_superior = 10  # Margen superior en píxeles
        posicion_x = self.pantalla.get_width() - mi_foto.get_width() - margen_derecho
        posicion_y = margen_superior
    
        self.pantalla.fill(globals.BLANCO)
        self.pantalla.blit(mi_foto, (posicion_x, posicion_y))
    
        fuente = pygame.font.Font(globals.fuente, globals.TAM_FUENTE)
        descripcion = fuente.render("Proyecto de Trabajo de Fin de Grado realizado por María de las Maravillas Luque Carmona", True, globals.NEGRO)
        descripcion_rect = descripcion.get_rect(center=(self.pantalla.get_width() / 2, 300))
        self.pantalla.blit(descripcion, descripcion_rect)
    
        contacto = fuente.render("Contacto: mmlc0007@red.ujaen.es", True, globals.NEGRO)
        contacto_rect = contacto.get_rect(center=(self.pantalla.get_width() / 2, 350))
        self.pantalla.blit(contacto, contacto_rect)
    
        pygame.display.flip()
        pygame.time.wait(5000)  # Espera 5 segundos
        self.mostrar_menu()  # Regresa al menú principal

    def ajustes(self):
        # edición de los ajustes del juego
        pass

    def mostrar_menu(self):
        en_menu = True

        fondo = pygame.image.load(globals.RUTA_FONDO)
        fondo = pygame.transform.scale(fondo, (globals.PANTALLA_ANCHO, globals.PANTALLA_ALTO))

        while en_menu:

            self.pantalla.fill(globals.BLANCO)
            
            self.pantalla.blit(fondo, (0, 0))
            
            boton_empezar = self.dibujar_boton("Empezar", 550, 50, 200, 50, globals.GRIS_CLARO, globals.ROJO, self.empezar_juego)
            boton_tutorial = self.dibujar_boton("Tutorial", 550, 130, 200, 50, globals.GRIS_CLARO, globals.ROJO, self.ver_tutorial)
            boton_creditos = self.dibujar_boton("Créditos", 550, 210, 200, 50, globals.GRIS_CLARO, globals.ROJO, self.ver_creditos)
            boton_ajustes = self.dibujar_boton("Ajustes", 550, 290, 200, 50, globals.GRIS_CLARO, globals.ROJO, self.ajustes)
            boton_puntuacion = self.dibujar_boton("Puntuación", 550, 370, 200, 50, globals.GRIS_CLARO, globals.AZUL, self.mostrar_puntuacion)
            boton_salir = self.dibujar_boton("Salir", 550, 500, 200, 50, globals.GRIS_CLARO, globals.MORADO_CLARO)

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
                        self.salir_juego()
                        en_menu = False
                    elif boton_puntuacion.collidepoint(mouse_pos):
                        self.seleccionando_dificultad = False
                        self.mostrar_puntuacion()
                    elif boton_ajustes.collidepoint(mouse_pos):
                        self.ajustes()
                        en_menu = False

            

            
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


class Tablero:
    def __init__(self, pantalla, sudoku, resuelto):
        self.sudoku = sudoku      
        self.resuelto = resuelto
        self.inicial = np.copy(self.sudoku)
        self.pantalla = pantalla
        
    def set_valor(self, fila, columna, valor):
        if self.inicial[fila, columna] == 0:  # Solo permitir cambios en celdas que eran 0 inicialmente
            if self.sudoku[fila][columna] == valor:
                return
            elif self.es_posible(fila, columna, valor):
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
                    texto = pygame.font.Font(globals.fuente, globals.TAM_FUENTE).render(str(abs(valor)), True, color)
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
            texto = pygame.font.Font(globals.fuente, globals.TAM_FUENTE).render(str(valor), True, globals.NEGRO)
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
                    texto = pygame.font.Font(globals.fuente, globals.TAM_FUENTE).render(str(abs(valor)), True, color)
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
    if not os.path.exists(globals.ARCHIVO_PUNTUACION):
        puntuacion = [['Dificultad', 'Puntuacion']]
        with open(globals.ARCHIVO_PUNTUACION, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(puntuacion)

    logo = pygame.image.load(globals.RUTA_LOGO)

    pygame.display.set_icon(logo)

    pygame.init()
    pantalla = pygame.display.set_mode((globals.PANTALLA_ANCHO, globals.PANTALLA_ALTO))
    pygame.display.set_caption("SUDOku")
    s = Sudoku()
    juego = Juego(pantalla, s)
    juego.mostrar_menu()