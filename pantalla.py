import pygame
import sys

class Utils:
    def __init__(self,pantalla):
        self.NEGRO = (0, 0, 0)
        self.BLANCO = (255, 255, 255)
        self.GRIS = (200, 200, 200)
        self.ROJO = (255, 0, 0)
        self.pantalla = pantalla

    # Función para dibujar botones
    def dibujar_boton(self, mensaje, x, y, ancho, alto, color_inactivo, color_activo, accion=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + ancho > mouse[0] > x and y + alto > mouse[1] > y:
            pygame.draw.rect(self.pantalla, color_activo, (x, y, ancho, alto))
            if click[0] == 1 and accion:
                accion()
        else:
            pygame.draw.rect(self.pantalla, color_inactivo, (x, y, ancho, alto))
        
        texto = pygame.font.Font(None, 20).render(mensaje, True, self.NEGRO)
        texto_rect = texto.get_rect(center=(x + ancho / 2, y + alto / 2))
        self.pantalla.blit(texto, texto_rect)

    # Funciones para cada botón
    def empezar_juego(self):
        print("Empezar juego")  # Aquí iría la lógica para empezar el juego

    def ver_tutorial(self):
        print("Ver tutorial")  # Aquí iría la lógica para mostrar el tutorial

    def ver_info_creador(self):
        print("Ver info del creador")  # Aquí iría la lógica para mostrar la info del creador

    # Pantalla de menú
    def mostrar_menu(self):
        en_menu = True
        while en_menu:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.pantalla.fill(self.BLANCO)
            self.dibujar_boton("Empezar", 100, 100, 200, 50, self.GRIS, self.ROJO, self.empezar_juego)
            self.dibujar_boton("Tutorial", 100, 200, 200, 50, self.GRIS, self.ROJO, self.ver_tutorial)
            self.dibujar_boton("Info del Creador", 100, 300, 200, 50, self.GRIS, self.ROJO, self.ver_info_creador)
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)