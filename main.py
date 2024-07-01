# Importamos la librería de Pygame
import pygame
import sys
from pantalla import Utils

# Inicializamos Pygame
pygame.init()

# Configuramos la ventana del juego
pantalla_ancho = 800
pantalla_alto = 600
pantalla = pygame.display.set_mode((pantalla_ancho, pantalla_alto))

utils = Utils(pantalla)

# Configuramos el título de la ventana
pygame.display.set_caption("SUDOku")

# Definimos colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

utils.mostrar_menu()

# Bucle principal del juego
while True:
    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Actualizaciones de juego

    # Rellenamos el fondo
    pantalla.fill(BLANCO)

    # Dibujamos elementos en la pantalla

    # Actualizamos la pantalla
    pygame.display.flip()

    # Controlamos la tasa de refresco
    pygame.time.Clock().tick(60)
    