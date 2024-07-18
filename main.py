import pygame
import sys
import numpy as np
import globals

class Utils:
    def __init__(self, pantalla):
        self.pantalla = pantalla

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
        while en_menu:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    en_menu = False

            tablero = Tablero(self.pantalla)
            tablero.imprimir_tablero()
                
            pygame.display.flip()
            pygame.time.Clock().tick(60)

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
                    en_menu = False
            
            self.pantalla.fill(globals.BLANCO)
            self.dibujar_boton("Empezar", 100, 100, 200, 50, globals.GRIS, globals.ROJO, self.empezar_juego)
            self.dibujar_boton("Tutorial", 100, 200, 200, 50, globals.GRIS, globals.ROJO, self.ver_tutorial)
            self.dibujar_boton("Info del Creador", 100, 300, 200, 50, globals.GRIS, globals.ROJO, self.ver_info_creador)
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)

class Tablero:
    def __init__(self, pantalla):
        # Crear tablero con números de ejemplo
        self.tablero = np.array([[5, 3, 0, 0, 7, 0, 0, 0, 0],
                                [6, 0, 0, 1, 9, 5, 0, 0, 0],
                                [0, 9, 8, 0, 0, 0, 0, 6, 0],
                                [8, 0, 0, 0, 6, 0, 0, 0, 3],
                                [4, 0, 0, 8, 0, 3, 0, 0, 1],
                                [7, 0, 0, 0, 2, 0, 0, 0, 6],
                                [0, 6, 0, 0, 0, 0, 2, 8, 0],
                                [0, 0, 0, 4, 1, 9, 0, 0, 5],
                                [0, 0, 0, 0, 8, 0, 0, 7, 9]])
        self.pantalla = pantalla

    def insertar_numero(self, fila, columna, numero):
        if self.es_posible(fila, columna, numero):
            self.tablero[fila, columna] = numero
            return True
        return False

    def es_posible(self, fila, columna, numero):
        if numero in self.tablero[fila]:
            return False
        if numero in self.tablero[:, columna]:
            return False
        cuadrante_fila = fila // 3 * 3
        cuadrante_columna = columna // 3 * 3
        if numero in self.tablero[cuadrante_fila:cuadrante_fila+3, cuadrante_columna:cuadrante_columna+3]:
            return False
        return True

    def imprimir_tablero(self):
        self.pantalla.fill(globals.COLOR_FONDO)
        for fila in range(10):
            grosor = 4 if fila % 3 == 0 else 1
            pygame.draw.line(self.pantalla, globals.COLOR_LINEA, (globals.MARGEN, globals.MARGEN + fila * globals.TAMAÑO_CELDA), (globals.ANCHO - globals.MARGEN, globals.MARGEN + fila * globals.TAMAÑO_CELDA), grosor)
            pygame.draw.line(self.pantalla, globals.COLOR_LINEA, (globals.MARGEN + fila * globals.TAMAÑO_CELDA, globals.MARGEN), (globals.MARGEN + fila * globals.TAMAÑO_CELDA, globals.ALTO - globals.MARGEN), grosor)
        
        # Dibujar números
        try:
            fuente = pygame.font.Font(None, 36)
        except Exception as e:
            print(f"Error al cargar la fuente: {e}")
        for fila in range(9):
            for columna in range(9):
                if self.tablero[fila, columna] != 0:
                    try:
                        
                        numero = fuente.render(str(self.tablero[fila, columna]), True, globals.NEGRO)
                        numero_rect = numero.get_rect(center=(globals.MARGEN + columna * globals.TAMAÑO_CELDA + globals.TAMAÑO_CELDA / 2,
                                                            globals.MARGEN + fila * globals.TAMAÑO_CELDA + globals.TAMAÑO_CELDA / 2))
                        self.pantalla.blit(numero, numero_rect)
                    except Exception as e:
                        print(f"Error al renderizar el número en ({fila}, {columna}): {e}")


        
        # Dibujar texto de dificultad
        texto_dificultad = "Dificultad: Fácil"
        fuente_dificultad = pygame.font.Font(None, 36)
        texto = fuente_dificultad.render(texto_dificultad, True, globals.NEGRO)
        texto_rect = texto.get_rect(center=(globals.ANCHO + 100, globals.ALTO // 2))
        self.pantalla.blit(texto, texto_rect)

        pygame.display.flip()

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((globals.PANTALLA_ANCHO, globals.PANTALLA_ALTO))
    pygame.display.set_caption("SUDOku")
    utils = Utils(pantalla)
    utils.mostrar_menu()

if __name__ == "__main__":
    main()