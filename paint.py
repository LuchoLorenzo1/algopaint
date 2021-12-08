import gamelib
import png
from pila import Pila

def copia(diccionario):
    '''
    Recibe un diccionario y devuelve su copia. (para diccionarios con valores mutables)
    '''
    copia = {}
    for key, value in diccionario.items():
        copia[key] = value.copy()
    return copia

class Grilla:
    def __init__(self, x1, x2, y1, y2, n, m, tamano_pixel):
        '''
        Recibe la posición de la grilla, los numeros n y m, que son los pixeles ancho y largo que tendra cada imagen. Y también el tamaño del lado del pixel dentro de la aplicación.
        '''
        self.imagen = Imagen(n,m)
        self.tamano_pixel = tamano_pixel

        self.balde = False
        self.historial = Pila()
        self.historial_rehacer = Pila()

        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.n = n
        self.m = m


    def mostrar(self):
        '''
        Muestra la grilla
        '''
        for m in range(self.m):
            for n in range(self.n):
                X1 = self.x1 + n*self.tamano_pixel
                Y1 = self.y1 + m*self.tamano_pixel
                X2 = X1 + self.tamano_pixel
                Y2 = Y1 + self.tamano_pixel

                color = self.imagen.imagen.get(m,{}).get(n,'#FFFFFF')
                gamelib.draw_rectangle(X1, Y1, X2, Y2, fill=color, outline='black')

    def click(self, x, y):
        '''
        Recibe las coordenadas dentro de la imagen y muta la grilla poniendole el color actual en esas coordenadas
        '''
        copy = copia(self.imagen.imagen)

        pixelx = x // self.tamano_pixel
        pixely = y // self.tamano_pixel

        if self.balde:
            color_inicial = self.imagen.devolver_color_en(pixelx, pixely)
            self.imagen.balde_pintura(pixelx, pixely, color_inicial)
        else:
            self.imagen.pintar(pixelx, pixely)

        if copy != self.imagen.imagen:
            self.historial.apilar(copy)
            self.historial_rehacer.vaciar()

    def alternar_balde(self):
        '''
        Alterna el booleano del balde.
        '''
        if self.balde:
            gamelib.say('Se ha desactivado el balde')
        else:
            gamelib.say('Se ha activado el balde')
        self.balde = not self.balde

    def deshacer(self):
        '''
        Vuelve una imagen atrás en el historial.
        '''
        if self.historial.esta_vacia():
            gamelib.say('No hay más cambios anteriores')
        else:
            self.historial_rehacer.apilar(self.imagen.imagen)

            self.imagen.imagen = copia(self.historial.desapilar())

    def rehacer(self):
        '''
        Deshace el deshacer
        '''
        if self.historial_rehacer.esta_vacia():
            gamelib.say('No hay más cambios por rehacer')
        else:
            self.historial.apilar(self.imagen.imagen)

            self.imagen.imagen =copia(self.historial_rehacer.desapilar())


class Imagen:
    def __init__(self, n, m):
        self.imagen = {}
        self.color_actual = '#000000'
        self.n = n
        self.m = m

    def devolver_color_en(self, i, j):
        '''
        Devuelve el color que tiene la imagen en la posición i,j.
        '''
        if 0 <= i < self.n and 0 <= j < self.m:
            self.imagen[j] = self.imagen.get(j, {})
            return self.imagen[j].get(i, '#FFFFFF')
        else:
            return None

    def cambiar_color(self, color):
        '''
        Recibe un color por parametro, chequea si correctamente es hexadecimal y lo define como color actual.
        '''
        if len(color) != 7 or color[0] != '#':
            gamelib.say('El color elegido no es correcto')
            return
        try:
            int(color[1:7],16)
            self.color_actual = color
        except ValueError:
            gamelib.say('El color elegido no es correcto')

    def elegir_color(self):
        '''
        Le pregunta al usuario por un nuevo color.
        '''
        nuevo_color = gamelib.input('Elige un color en formato hexadecimal. E.g. "#F0F0F2"')
        if nuevo_color:
            self.cambiar_color(nuevo_color)
        else:
            gamelib.say('Debes ingresar un color')

    def pintar(self, i, j):
        '''
        Recibe las coordenadas y pone el color actual en ese lugar de la imagen.
        '''
        self.imagen[j] = self.imagen.get(j, {})
        self.imagen[j][i] = self.color_actual

    def borrar(self):
        '''
        vacía la grilla
        '''
        choice = gamelib.input('Estas seguro que quieres borrar todo? SI/NO')
        if choice == 'SI':
            self.imagen = {}
            return True
        else:
            return False

    def cargar_ppm(self):
        '''
        Pregunta por el nombre del archivo ppm, y carga los datos del archivo dentro de la imagen.
        '''
        try:
            nombre_archivo = gamelib.input('Ingrese un nombre para el archivo')

            if not nombre_archivo:
                gamelib.say('Debes ingresar un nombre para el archivo')
                return

            if not self.borrar():
                return

            with open(nombre_archivo) as f:
                next(f)
                n,m = f.readline().rstrip().split(' ')
                self.n = int(n)
                self.m = int(m)

                next(f)
                for m, linea in enumerate(f):
                    for n in range(self.n):
                        color_hex = '#'
                        principio = n*11 + n*3
                        final = principio + 12
                        r, g, b = linea[principio:final].split()
                        color_hex += f'{int(r):02x}'
                        color_hex += f'{int(g):02x}'
                        color_hex += f'{int(b):02x}'

                        if color_hex != '#ffffff':
                            self.imagen[m] = self.imagen.get(m,{})
                            self.imagen[m][n] = color_hex.upper()

        except (UnicodeDecodeError, ValueError):
            gamelib.say('Debes ingresar un archivo en formato PPM')

    def guardar_png(self):
        '''
        Pregunta por un el nombre del archivo y lo guarda en formato png
        '''
        nombre_archivo = gamelib.input('Nombre del archivo: ')
        if not nombre_archivo:
            gamelib.say('Debes ingresar un nombre')
            return

        paleta = []
        imagen = []

        for M in range(self.m):
            fila = []
            for N in range(self.n):
                color = self.imagen.get(M, {}).get(N, '#FFFFFF')[1:]

                tupla_color = (int(color[0:2],16) , int(color[2:4],16), int(color[4:6],16))

                if tupla_color not in paleta:
                    paleta.append(tupla_color)

                fila.append(paleta.index(tupla_color))

            imagen.append(fila)
        png.escribir(nombre_archivo, paleta, imagen)

    def guardar_ppm(self):
        '''
        Pregunta por un nombre archivo ppm y escribe en el mismo la imagen (en formato ppm)
        '''
        nombre_archivo = gamelib.input('Nombre del archivo: ')

        if not nombre_archivo:
            gamelib.say('Debes ingresar un nombre')
            return

        with open(nombre_archivo, 'w') as f:
            f.write('P3' + '\n')
            f.write(f'{self.n} {self.m}\n')
            f.write('255\n')

            for M in range(self.m):
                linea = ''
                for N in range(self.n):
                    color = self.imagen.get(M, {}).get(N, '#FFFFFF')[1:]
                    for i in range(0,3):
                        numero = str(int(color[2*i:2*i + 2],16))
                        linea += ' '*(3-len(numero)) + numero + ' '

                    linea += '  '
                f.write(linea + '\n')

    def balde_pintura(self, x, y, color_inicial):
        self.pintar(x,y)

        if self.devolver_color_en(x+1, y) == color_inicial:
            self.balde_pintura(x+1, y, color_inicial)

        if self.devolver_color_en(x-1, y) == color_inicial:
            self.balde_pintura(x-1, y, color_inicial)

        if self.devolver_color_en(x, y+1) == color_inicial:
            self.balde_pintura(x, y+1, color_inicial)

        if self.devolver_color_en(x, y-1) == color_inicial:
            self.balde_pintura(x, y-1, color_inicial)

