from paint import Grilla
from botonera import Boton, Botonera

#CONSTANTES GLOBALES

N = 20
M = 20

TAMANO_PIXEL = 20

MARGEN = 10

ALTO_BARRA_OPCIONES = 50

ANCHO_PANTALLA = N*TAMANO_PIXEL + 2*MARGEN

if ANCHO_PANTALLA < 420:
    ANCHO_PANTALLA = 420

ALTO_PANTALLA = M*TAMANO_PIXEL + 3*ALTO_BARRA_OPCIONES + 4*MARGEN

COLORES_INICIALES = ('#000000','#FFFFFF','#FFFF00','#FF0000','#0000FF', '#00FF00')


def devuelve_estructura_inicial():
    '''
    Diseña e inicializa instancias de las clases Grilla, Boton y Botonera para la interfaz de la aplicación y las devuelve
    '''
    X1 = MARGEN
    X2 = ANCHO_PANTALLA - MARGEN

    #---------------
    #CREACION GRILLA
    #---------------

    y1_grilla = MARGEN
    y2_grilla = M*TAMANO_PIXEL + MARGEN

    grilla = Grilla(X1, X2, y1_grilla, y2_grilla, N, M, TAMANO_PIXEL)

    #---------------
    #CREACION BOTONES COLORES
    #---------------

    largo_botones = (ANCHO_PANTALLA - MARGEN*(len(COLORES_INICIALES)+1)) / len(COLORES_INICIALES)

    lista_botones_colores = []
    for i, color in enumerate(COLORES_INICIALES):
        principio = (largo_botones + MARGEN)*i
        final = principio + largo_botones

        nuevo_boton = Boton(principio, final, lambda x: grilla.imagen.cambiar_color(x), fill=color, parametro=color)
        lista_botones_colores.append(nuevo_boton)

    y1_colores = y2_grilla + MARGEN
    y2_colores = y1_colores + ALTO_BARRA_OPCIONES

    botonera_colores = Botonera(X1, X2, y1_colores, y2_colores, lista_botones_colores)

    #---------------
    #CREACION BOTONES OPCIONES
    #---------------

    funciones = {
            'borrar': lambda: grilla.imagen.borrar(),
            'color': lambda: grilla.imagen.elegir_color(),
            'balde': lambda: grilla.alternar_balde(),
            'deshacer': lambda: grilla.deshacer(),
            'rehacer': lambda: grilla.rehacer()
    }

    largo_botones = (ANCHO_PANTALLA - MARGEN*(len(funciones)+1)) / len(funciones)

    lista_botones_opciones = []
    for i, elemento in enumerate(funciones.items()):
        texto, funcion = elemento

        principio = (largo_botones + MARGEN)*i
        final = principio + largo_botones

        lista_botones_opciones.append(Boton(principio, final, funcion, texto=texto, outline='grey') )

    y1_opciones = y2_colores + MARGEN
    y2_opciones = y1_opciones + ALTO_BARRA_OPCIONES
    botonera_opciones = Botonera(X1, X2, y1_opciones, y2_opciones, lista_botones_opciones)

    #-----------------
    # CREACION BOTONES OPCIONES DE ARCHIVOS Y ESO (guardar, cargar, etc..)
    #-----------------

    funciones = {
            'guardar ppm': lambda: grilla.imagen.guardar_ppm(),
            'guardar png': lambda: grilla.imagen.guardar_png(),
            'cargar ppm': lambda: grilla.imagen.cargar_ppm(),
    }

    largo_botones = (ANCHO_PANTALLA - MARGEN*(len(funciones)+1)) / len(funciones)
    lista_botones_archivos = []
    for i, elemento in enumerate(funciones.items()):
        texto, funcion = elemento

        principio = (largo_botones + MARGEN)*i
        final = principio + largo_botones

        lista_botones_archivos.append(Boton(principio, final, funcion, texto=texto, outline='grey') )

    y1_opciones_archivos = y2_opciones + MARGEN
    y2_opciones_archivos = ALTO_PANTALLA - MARGEN
    botonera_opciones_archivos = Botonera(X1, X2, y1_opciones_archivos, y2_opciones_archivos, lista_botones_archivos)

    return grilla, (botonera_colores, botonera_opciones, botonera_opciones_archivos)
