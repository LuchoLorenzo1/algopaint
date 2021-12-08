import gamelib
from interfaz import devuelve_estructura_inicial, ANCHO_PANTALLA, ALTO_PANTALLA, MARGEN

def main():
    '''
    Se ocupa del main loop del juego
    '''

    gamelib.resize(ANCHO_PANTALLA, ALTO_PANTALLA)
    grilla, botoneras = devuelve_estructura_inicial()

    click_apretado = False

    while gamelib.is_alive():

        gamelib.draw_begin()

        gamelib.draw_rectangle(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA, fill='grey')
        grilla.mostrar()

        for botonera in botoneras:
            botonera.mostrar()

        gamelib.draw_end()

        ev = gamelib.wait()
        if not ev:
            break

        if ev.type == gamelib.EventType.ButtonPress and ev.mouse_button == 1:
            if MARGEN <= ev.x <= ANCHO_PANTALLA - MARGEN:

                if grilla.y1 <= ev.y <= grilla.y2:
                    grilla.click(ev.x - MARGEN, ev.y - MARGEN)
                    click_apretado = True

                for botonera in botoneras:
                    if botonera.y1 <= ev.y <= botonera.y2:
                        botonera.click(ev.x - MARGEN,ev.y - MARGEN)


        elif ev.type == gamelib.EventType.ButtonRelease and ev.mouse_button == 1:
            click_apretado = False

        if click_apretado:
            if ev.type == gamelib.EventType.Motion:
                    if MARGEN <= ev.x <= ANCHO_PANTALLA - MARGEN:
                        if grilla.y1 <= ev.y <= grilla.y2:
                            grilla.click(ev.x - MARGEN, ev.y - MARGEN)

gamelib.init(main)
