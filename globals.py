import os

# Rutas
directorio_actual = os.path.dirname(os.path.abspath(__file__))

fuente = os.path.join(directorio_actual, "font", "roboto", "Roboto-Light.ttf")
RUTA_IMG_PAUSAR = os.path.join(directorio_actual, "img", "pausar.png")
RUTA_IMG_INICIAR = os.path.join(directorio_actual, "img", "empezar.png")
RUTA_IMG_AJUSTES = os.path.join(directorio_actual, "img", "ajustes.png")
RUTA_IMG_BORRAR = os.path.join(directorio_actual, "img", "borrar.png")
RUTA_IMG_SONIDO = os.path.join(directorio_actual, "img", "sonido.png")
RUTA_IMG_SILENCIO = os.path.join(directorio_actual, "img", "silencio.png")

# Botones
BORDER_RADIUS = 30
TAM_FUENTE = 24

# Tamaños
PANTALLA_ANCHO = 800
PANTALLA_ALTO = 600

TAMAÑO_CELDA = 60
MARGEN = 20
ANCHO = MARGEN * 2 + TAMAÑO_CELDA * 9
ALTO = MARGEN * 2 + TAMAÑO_CELDA * 9

# Colores
COLOR_FONDO = (255, 255, 255)
COLOR_LINEA = (0, 0, 0)

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (200, 200, 200)
ROJO = (255, 102, 102)
VERDE_CLARO = (200, 255, 200)
MORADO_CLARO = (230, 200, 230)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
NARANJA = (255, 165, 0)