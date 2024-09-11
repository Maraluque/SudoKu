import os
import csv
import globals
import pygame
import sudoku
import partida as juego

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
            writer.writerow(["Configuracion", "Valor"])
            writer.writerow(["accesibilidad", False])
            writer.writerow(["dificil",2])
            config["accesibilidad"] = False
            config["dificil"] = 2

    logo = pygame.image.load(globals.RUTA_LOGO)

    pygame.display.set_icon(logo)

    pygame.init()
    pantalla = pygame.display.set_mode((globals.PANTALLA_ANCHO, globals.PANTALLA_ALTO))
    pygame.display.set_caption("Sudo ku")
    s = sudoku.Sudoku()
    jugar = juego.Partida(pantalla, s, config)
    jugar.mostrar_menu()
