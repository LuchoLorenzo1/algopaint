import gamelib

class Boton:
    def __init__(self, principio, final, funcion, texto='', fill='black', parametro=None, outline=None):
        '''
        Recibe la posición relativa dentro de la botonera, texto que irá dentro del rectangulo, fill(que es el color del fondo)
        Y la función anónima que se ejectutará cuando se presione el botón.
        '''
        self.focus = False
        self.texto = texto
        self.fill = fill
        self.outline = outline
        self.f = funcion
        self.parametro = parametro
        self.principio = principio
        self.final = final

    def check_click(self, coordenada):
        '''
        recibe una coordenada donde se ha hecho un click y devuelve True si esta dentro del botón.
        '''
        return self.principio <= coordenada <= self.final

class Botonera:
    def __init__(self, x1, x2, y1, y2, lista_botones):
        '''
        Recibe la posición de la botonera y una lista con botones (class Boton).
        '''
        self.botones = lista_botones
        self.boton_focus = None
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def mostrar(self):
        '''
        Muestra la botonera
        '''
        for boton in self.botones:
            if boton.focus and not boton.outline:
                outline = 'black'
            else:
                outline = 'grey'

            x1 = self.x1 +  boton.principio
            x2 = self.x1 + boton.final

            gamelib.draw_rectangle(x1, self.y1, x2, self.y2, fill=boton.fill, outline=outline, width=5)

            if boton.texto:
                altura = (self.y1 + self.y2)//2
                ancho = (x1+x2)//2
                text=boton.texto

                gamelib.draw_text(text, ancho, altura, fill='white', size=8)

    def click(self, x, y):
        '''
        Verifica si algun boton de la lista fue clickeado
        '''
        for boton in self.botones:
            if boton.check_click(x):
                if boton.parametro:
                    boton.f(boton.parametro)
                else:
                    boton.f()

                if self.boton_focus:
                    self.boton_focus.focus = False

                boton.focus = True
                self.boton_focus = boton

                return

