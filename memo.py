import pygame
import sys
import math
import time
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

altura_boton = 50
medida_cuadro_nivel1 = 185
medida_cuadro_nivel2 = 125
nombre_imagen_oculta = "assets/oculta.png"
imagen_oculta = pygame.image.load(nombre_imagen_oculta)
segundos_mostrar_pieza = 2

class Cuadro:
    def __init__(self, fuente_imagen):
        self.mostrar = True
        self.descubierto = False
        self.fuente_imagen = fuente_imagen
        self.imagen_real = pygame.image.load(fuente_imagen)

cuadros_nivel1 = [
    [Cuadro("assets/coco.png"), Cuadro("assets/coco.png"),
     Cuadro("assets/manzana.png"), Cuadro("assets/manzana.png")],
    [Cuadro("assets/limón.png"), Cuadro("assets/limón.png"),
     Cuadro("assets/naranja.png"), Cuadro("assets/naranja.png")],
    [Cuadro("assets/pera.png"), Cuadro("assets/pera.png"),
     Cuadro("assets/piña.png"), Cuadro("assets/piña.png")],
    [Cuadro("assets/plátano.png"), Cuadro("assets/plátano.png"),
     Cuadro("assets/sandía.png"), Cuadro("assets/sandía.png")],
]

cuadros_nivel2 = [
    [Cuadro("assets/coco.png"), Cuadro("assets/coco.png"),
     Cuadro("assets/manzana.png"), Cuadro("assets/manzana.png"),
     Cuadro("assets/limón.png"), Cuadro("assets/limón.png")],
    [Cuadro("assets/naranja.png"), Cuadro("assets/naranja.png"),
     Cuadro("assets/pera.png"), Cuadro("assets/pera.png"),
     Cuadro("assets/piña.png"), Cuadro("assets/piña.png")],
    [Cuadro("assets/plátano.png"), Cuadro("assets/plátano.png"),
     Cuadro("assets/sandía.png"), Cuadro("assets/sandía.png"),
     Cuadro("assets/coco.png"), Cuadro("assets/coco.png")],
    [Cuadro("assets/manzana.png"), Cuadro("assets/manzana.png"),
     Cuadro("assets/limón.png"), Cuadro("assets/limón.png"),
     Cuadro("assets/naranja.png"), Cuadro("assets/naranja.png")],
    [Cuadro("assets/pera.png"), Cuadro("assets/pera.png"),
     Cuadro("assets/piña.png"), Cuadro("assets/piña.png"),
     Cuadro("assets/plátano.png"), Cuadro("assets/plátano.png")],
    [Cuadro("assets/sandía.png"), Cuadro("assets/sandía.png"),
     Cuadro("assets/coco.png"), Cuadro("assets/coco.png"),
     Cuadro("assets/manzana.png"), Cuadro("assets/manzana.png")],
]

color_blanco = (255, 255, 255)
color_negro = (0, 0, 0)
color_gris = (206, 206, 206)
color_azul = (30, 136, 229)
color_azul_fuerte = (0, 0, 255)
color_naranja = (255, 165, 0)

sonido_fondo = pygame.mixer.Sound("assets/fondo.wav")
sonido_clic = pygame.mixer.Sound("assets/clic.wav")
sonido_exito = pygame.mixer.Sound("assets/ganador.wav")
sonido_fracaso = pygame.mixer.Sound("assets/equivocado.wav")
sonido_voltear = pygame.mixer.Sound("assets/voltear.wav")

nivel_actual = 1
cuadros = cuadros_nivel1
medida_cuadro = medida_cuadro_nivel1

anchura_pantalla = len(cuadros[0]) * medida_cuadro
altura_pantalla = (len(cuadros) * medida_cuadro) + altura_boton
anchura_boton = anchura_pantalla

tamanio_fuente = 20
fuente = pygame.font.SysFont("Arial", tamanio_fuente)
xFuente = int((anchura_boton / 2) - (tamanio_fuente / 2))
yFuente = int(altura_pantalla - altura_boton / 2 - tamanio_fuente / 2)

boton = pygame.Rect((anchura_pantalla - 200) // 2, altura_pantalla - altura_boton - 20, 200, altura_boton)
boton_salir = pygame.Rect((anchura_pantalla - 200) // 2, altura_pantalla - altura_boton - 80, 200, altura_boton)
boton_segundo_nivel = pygame.Rect((anchura_pantalla - 200) // 2, altura_pantalla - altura_boton - 140, 200, altura_boton)
mostrar_boton_segundo_nivel = False

ultimos_segundos = None
puede_jugar = True
juego_iniciado = False
x1 = None
y1 = None
x2 = None
y2 = None

menu_imagen = pygame.image.load("assets/menu.png")
titulo = "MEMORAMA"
titulo_fuente = pygame.font.SysFont("Comic Sans MS", 60, bold=True)
titulo_x = (anchura_pantalla - titulo_fuente.size(titulo)[0]) // 2
titulo_y = 100

instrucciones = "Encuentra todas las parejas de frutas!"
instrucciones_fuente = pygame.font.SysFont("Arial", 25)
instrucciones_x = (anchura_pantalla - instrucciones_fuente.size(instrucciones)[0]) // 2
instrucciones_y = titulo_y + 80

def ocultar_todos_los_cuadros():
    for fila in cuadros:
        for cuadro in fila:
            cuadro.mostrar = False
            cuadro.descubierto = False

def aleatorizar_cuadros():
    cantidad_filas = len(cuadros)
    cantidad_columnas = len(cuadros[0])
    for y in range(cantidad_filas):
        for x in range(cantidad_columnas):
            x_aleatorio = random.randint(0, cantidad_columnas - 1)
            y_aleatorio = random.randint(0, cantidad_filas - 1)
            cuadro_temporal = cuadros[y][x]
            cuadros[y][x] = cuadros[y_aleatorio][x_aleatorio]
            cuadros[y_aleatorio][x_aleatorio] = cuadro_temporal

def comprobar_si_gana():
    if gana():
        pygame.mixer.Sound.play(sonido_exito)
        global mostrar_boton_segundo_nivel
        if nivel_actual == 1:
            mostrar_boton_segundo_nivel = True
        reiniciar_juego()

def gana():
    for fila in cuadros:
        for cuadro in fila:
            if not cuadro.descubierto:
                return False
    return True

def reiniciar_juego():
    global juego_iniciado
    juego_iniciado = False

def iniciar_juego():
    pygame.mixer.Sound.play(sonido_clic)
    global juego_iniciado
    for i in range(3):
        aleatorizar_cuadros()
    ocultar_todos_los_cuadros()
    juego_iniciado = True

def iniciar_segundo_nivel():
    global nivel_actual, cuadros, medida_cuadro, anchura_pantalla, altura_pantalla, boton, boton_salir, boton_segundo_nivel
    nivel_actual = 2
    cuadros = cuadros_nivel2
    medida_cuadro = medida_cuadro_nivel2
    anchura_pantalla = len(cuadros[0]) * medida_cuadro
    altura_pantalla = (len(cuadros) * medida_cuadro) + altura_boton
    pantalla_juego = pygame.display.set_mode((anchura_pantalla, altura_pantalla))
    boton = pygame.Rect((anchura_pantalla - 200) // 2, altura_pantalla - altura_boton - 20, 200, altura_boton)
    boton_salir = pygame.Rect((anchura_pantalla - 200) // 2, altura_pantalla - altura_boton - 80, 200, altura_boton)
    boton_segundo_nivel = pygame.Rect((anchura_pantalla - 200) // 2, altura_pantalla - altura_boton - 140, 200, altura_boton)
    iniciar_juego()

pantalla_juego = pygame.display.set_mode((anchura_pantalla, altura_pantalla))
pygame.display.set_caption('Memorama')
pygame.mixer.Sound.play(sonido_fondo, -1)

juego_iniciado = False

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and puede_jugar:
                xAbsoluto, yAbsoluto = event.pos
                if not juego_iniciado:
                    if boton.collidepoint(event.pos):
                        iniciar_juego()
                    elif boton_salir.collidepoint(event.pos):
                        sys.exit()
                    elif mostrar_boton_segundo_nivel and boton_segundo_nivel.collidepoint(event.pos):
                        iniciar_segundo_nivel()
                else:
                    x = math.floor(xAbsoluto / medida_cuadro)
                    y = math.floor(yAbsoluto / medida_cuadro)
                    cuadro = cuadros[y][x]
                    if cuadro.mostrar or cuadro.descubierto:
                        continue
                    if x1 is None and y1 is None:
                        x1 = x
                        y1 = y
                        cuadros[y1][x1].mostrar = True
                        pygame.mixer.Sound.play(sonido_voltear)
                    else:
                        x2 = x
                        y2 = y
                        cuadros[y2][x2].mostrar = True
                        cuadro1 = cuadros[y1][x1]
                        cuadro2 = cuadros[y2][x2]
                        if cuadro1.fuente_imagen == cuadro2.fuente_imagen:
                            cuadros[y1][x1].descubierto = True
                            cuadros[y2][x2].descubierto = True
                            x1 = None
                            x2 = None
                            y1 = None
                            y2 = None
                            pygame.mixer.Sound.play(sonido_clic)
                        else:
                            pygame.mixer.Sound.play(sonido_fracaso)
                            ultimos_segundos = int(time.time())
                            puede_jugar = False
                    comprobar_si_gana()

        ahora = int(time.time())
        if ultimos_segundos is not None and ahora - ultimos_segundos >= segundos_mostrar_pieza:
            cuadros[y1][x1].mostrar = False
            cuadros[y2][x2].mostrar = False
            x1 = None
            y1 = None
            x2 = None
            y2 = None
            ultimos_segundos = None
            puede_jugar = True

        pantalla_juego.fill(color_blanco)

        if not juego_iniciado:
            pantalla_juego.blit(pygame.transform.scale(menu_imagen, (anchura_pantalla, altura_pantalla)), (0, 0))
            pygame.draw.rect(pantalla_juego, color_azul_fuerte, boton, border_radius=10)
            pygame.draw.rect(pantalla_juego, color_azul_fuerte, boton_salir, border_radius=10)
            pantalla_juego.blit(fuente.render(
                "Iniciar juego", True, color_blanco), (boton.x + 30, boton.y + 10))
            pantalla_juego.blit(fuente.render(
                "Salir", True, color_blanco), (boton_salir.x + 60, boton_salir.y + 10))
            if mostrar_boton_segundo_nivel:
                pygame.draw.rect(pantalla_juego, color_azul_fuerte, boton_segundo_nivel, border_radius=10)
                pantalla_juego.blit(fuente.render(
                    "Segundo Nivel", True, color_blanco), (boton_segundo_nivel.x + 30, boton_segundo_nivel.y + 10))
        else:
            x = 0
            y = 0
            for fila in cuadros:
                x = 0
                for cuadro in fila:
                    if cuadro.descubierto or cuadro.mostrar:
                        pantalla_juego.blit(pygame.transform.scale(cuadro.imagen_real, (medida_cuadro, medida_cuadro)), (x, y))
                    else:
                        pantalla_juego.blit(pygame.transform.scale(imagen_oculta, (medida_cuadro, medida_cuadro)), (x, y))
                    x += medida_cuadro
                y += medida_cuadro

        pygame.display.update()
except Exception as e:
    print("Se ha producido una excepción:", e)
finally:
    pygame.quit()
    sys.exit()