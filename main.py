import os
import csv
import globals
import pygame
import sudoku
import juego

if __name__ == "__main__":
    if not os.path.exists(globals.ARCHIVO_PUNTUACION):
        puntuacion = [['Dificultad', 'Puntuacion']]
        with open(globals.ARCHIVO_PUNTUACION, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(puntuacion)

    config = {}

    if os.path.exists(globals.ARCHIVO_CONFIGURACION):
        with open(globals.ARCHIVO_CONFIGURACION, mode='r') as archivo:
            reader = csv.reader(archivo)
            next(reader)
            for row in reader:
                config[row[0]] = row[1]
    else:
        with open(globals.ARCHIVO_CONFIGURACION, mode='w', newline='') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(["accesibilidad", False])

    logo = pygame.image.load(globals.RUTA_LOGO)

    pygame.display.set_icon(logo)

    pygame.init()
    pantalla = pygame.display.set_mode((globals.PANTALLA_ANCHO, globals.PANTALLA_ALTO))
    pygame.display.set_caption("SUDOku")
    s = sudoku.Sudoku()
    jugar = juego.Juego(pantalla, s, config)
    jugar.mostrar_menu()
