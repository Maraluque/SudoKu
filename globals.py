import os

# Rutas
directorio_actual = os.path.dirname(os.path.abspath(__file__))

fuente = os.path.join(directorio_actual, "font", "roboto", "Roboto-Light.ttf")
fuente_negrita = os.path.join(directorio_actual, "font", "roboto", "Roboto-Regular.ttf")
RUTA_IMG_PAUSAR = os.path.join(directorio_actual, "img", "pausar.png")
RUTA_IMG_INICIAR = os.path.join(directorio_actual, "img", "empezar.png")
RUTA_FONDO = os.path.join(directorio_actual, "img", "fondo.jpg")
RUTA_FONDO_PUNTUACION = os.path.join(directorio_actual, "img", "fondo_puntuacion.jpg")
RUTA_IMG_CONFETI = os.path.join(directorio_actual, "img", "confeti.png")
RUTA_IMG_CONFETI2 = os.path.join(directorio_actual, "img", "confeti2.png")
RUTA_IMG_CORTINA_CONFETI = os.path.join(directorio_actual, "img", "cortina_confeti.png")
RUTA_LOGO = os.path.join(directorio_actual, "img", "logo.png")
RUTA_MEDALLA_BRONCE = os.path.join(directorio_actual, "img", "bronce.png")
RUTA_MEDALLA_PLATA = os.path.join(directorio_actual, "img", "plata.png")
RUTA_MEDALLA_ORO = os.path.join(directorio_actual, "img", "oro.png")
RUTA_FOTO = os.path.join(directorio_actual, "img", "foto_orla.jpeg")
RUTA_CRUZ = os.path.join(directorio_actual, "img", "cruz.png")
RUTA_COLOREADO = os.path.join(directorio_actual, "img", "coloreado.png")

ARCHIVO_PUNTUACION = os.path.join(directorio_actual, "puntuacion.csv")
ARCHIVO_CONFIGURACION = os.path.join(directorio_actual, "configuracion.csv")

# Botones
BORDER_RADIUS = 30
TAM_FUENTE = 24
TAM_FUENTE_PUNTUACION = 20

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
GRIS_CLARO = (100, 100, 100)
ROJO = (255, 102, 102)
VERDE_CLARO = (200, 255, 200)
MORADO_CLARO = (230, 200, 230)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AZUL_CLARO = (0, 0, 125)
AMARILLO = (255, 255, 0)
NARANJA = (255, 165, 0)