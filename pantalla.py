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
        from tablero import Tablero
        en_menu = True
        while en_menu:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            tablero = Tablero(self.pantalla)
            tablero.imprimir_tablero()
                
            pygame.display.flip()
            pygame.time.Clock().tick(60)

    def ver_tutorial(self):
        print("Ver tutorial")  # Aquí iría la lógica para mostrar el tutorial

    def ver_info_creador(self):
        # Cargar y redimensionar la imagen a tamaño carnet (130x170 píxeles aproximadamente)
        ruta = "foto_orla.jpeg"
        mi_foto_original = pygame.image.load(ruta)  # Carga la foto
        mi_foto = pygame.transform.scale(mi_foto_original, (130, 170))  # Redimensiona la foto
    
        # Calcular la posición para colocar la foto en la parte superior derecha con un margen
        margen_derecho = 10  # Margen derecho en píxeles
        margen_superior = 10  # Margen superior en píxeles
        posicion_x = self.pantalla.get_width() - mi_foto.get_width() - margen_derecho
        posicion_y = margen_superior
    
        # Limpiar pantalla y dibujar fondo
        self.pantalla.fill(self.BLANCO)
    
        # Dibujar la imagen en la posición calculada
        self.pantalla.blit(mi_foto, (posicion_x, posicion_y))
    
        # Configurar y dibujar el texto de la descripción y contacto como antes
        fuente = pygame.font.Font(None, 24)
        descripcion = fuente.render("Proyecto de Trabajo de Fin de Grado realizado por María de las Maravillas Luque Carmona", True, self.NEGRO)
        descripcion_rect = descripcion.get_rect(center=(self.pantalla.get_width() / 2, 300))
        self.pantalla.blit(descripcion, descripcion_rect)
    
        contacto = fuente.render("Contacto: mmlc0007@red.ujaen.es", True, self.NEGRO)
        contacto_rect = contacto.get_rect(center=(self.pantalla.get_width() / 2, 350))
        self.pantalla.blit(contacto, contacto_rect)
    
        # Actualizar la pantalla
        pygame.display.flip()
    
        # Esperar un momento antes de regresar al menú
        pygame.time.wait(5000)  # Espera 5 segundos
        self.mostrar_menu()  # Regresa al menú principal
    
    # Pantalla de menú
    def mostrar_menu(self):
        en_menu = True
        while en_menu:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    en_menu = False
            
            self.pantalla.fill(self.BLANCO)
            self.dibujar_boton("Empezar", 100, 100, 200, 50, self.GRIS, self.ROJO, self.empezar_juego)
            self.dibujar_boton("Tutorial", 100, 200, 200, 50, self.GRIS, self.ROJO, self.ver_tutorial)
            self.dibujar_boton("Info del Creador", 100, 300, 200, 50, self.GRIS, self.ROJO, self.ver_info_creador)
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)