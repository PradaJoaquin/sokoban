import soko
import gamelib
import os
from pila import Pila
from cola import Cola

OESTE = (-1, 0)
ESTE = (1, 0)
NORTE = (0, -1)
SUR = (0, 1)

CARPETA = os.path.dirname(os.path.realpath(__file__))

ACCIONES_POSIBLES = (OESTE, ESTE, NORTE, SUR)

TECLAS = os.path.join(CARPETA, "teclas.txt")
NIVELES = os.path.join(CARPETA, "niveles.txt")

PISO = os.path.join(CARPETA, "img/ground.gif")
PARED = os.path.join(CARPETA, "img/wall.gif")
CAJA = os.path.join(CARPETA, "img/box.gif")
JUGADOR = os.path.join(CARPETA, "img/player.gif")
OBJETIVO = os.path.join(CARPETA, "img/goal.gif")

CELDA = 64

def juego_actualizar(juego, accion, pistas, acciones_hechas):
    """Actualiza el nivel actual segun la accion recibida."""
    if accion == "PISTA":
        if pistas.esta_vacia():
            juego_mostrar(juego, pistas, buscando_pistas=True)
            solucion_encontrada, acciones = buscar_solucion(juego)
            if solucion_encontrada:
                apilar_acciones(acciones, pistas)
            return juego
        
        acciones_hechas.apilar(juego)
        return soko.mover(juego, pistas.desapilar())
    
    if accion == "DESHACER":
        if acciones_hechas.esta_vacia():
            return juego
        vaciar_pistas(pistas)
        return acciones_hechas.desapilar()
    
    juego_movido = juego_mover(juego, accion)
    if juego != juego_movido:
        acciones_hechas.apilar(juego)
        vaciar_pistas(pistas)

    return juego_movido

def juego_mover(juego, accion):
    """Mueve al jugador segun la accion recibida."""
    if accion == "NORTE":
        return soko.mover(juego, NORTE)
    if accion == "SUR":
        return soko.mover(juego, SUR)
    if accion == "ESTE":
        return soko.mover(juego, ESTE)
    if accion == "OESTE":
        return soko.mover(juego, OESTE)

def buscar_solucion(estado_inicial):
    """Busca y devuelve la serie de pasos que lleva a la solucion del nivel actual"""
    visitados = {}
    return backtrack(estado_inicial, visitados)

def backtrack(estado, visitados):
    """Devuelve, si encontro, la serie de movimientos para resolver el nivel"""
    visitados[convertir_inmutable(estado)] = True
    if soko.juego_ganado(estado):
        # ¡encontramos la solución!
        return True, Cola()
    for accion in ACCIONES_POSIBLES:
        nuevo_estado = soko.mover(estado, accion)
        if convertir_inmutable(nuevo_estado) in visitados:
            continue
        solucion_encontrada, acciones = backtrack(nuevo_estado, visitados)
        if solucion_encontrada:
            acciones.encolar(accion)
            return True, acciones
    return False, None

def convertir_inmutable(estado):
    """Recibe un tipo de dato y devuelve una forma inmutable del mismo"""
    return "".join(estado)

def apilar_acciones(acciones, pistas):
    """Apila a una pila una serie de acciones"""
    while not acciones.esta_vacia():
        pistas.apilar(acciones.desencolar())

def vaciar_pistas(pistas):
    """Vacia la pila de pistas"""
    while not pistas.esta_vacia():
        pistas.desapilar()

def cargar_teclas():
    """Devuelve un diccionario con todas las teclas con sus respectivas acciones"""
    teclas_cargadas = {}
    with open(TECLAS) as teclas:
        for linea in teclas:
            linea = linea.rstrip()
            if not linea:
                continue
            tecla, accion = linea.split(" = ")
            teclas_cargadas[tecla] = accion
    return teclas_cargadas

def cargar_niveles():
    """Devuelve una lista con todos los niveles del juego."""
    lista_niveles = []
    with open(NIVELES) as niveles:
        nivel_actual = []
        for linea in niveles:
            if linea[0].isalpha() or linea[0] == "'":
                continue
            if linea == "\n":
                nivel_actual = agregar_espacios(nivel_actual)
                lista_niveles.append(nivel_actual)
                nivel_actual = []
            nivel_actual.append(linea.rstrip())        

    return lista_niveles

def agregar_espacios(nivel):
    """Agrega espacios, a los niveles que lo requieran, para que queden rectangulares."""
    dimension_max_fila = len(max(nivel, key=len))
    for i in range(len(nivel)):
        if len(nivel[i]) < dimension_max_fila:
            nivel[i] = nivel[i] + " " * (dimension_max_fila - len(nivel[i]))
    return nivel

def juego_mostrar(juego, pistas, buscando_pistas=False):
    """Muestra el juego en la pantalla segun las dimensiones del nivel."""
    gamelib.draw_begin()

    dimensiones = soko.dimensiones(juego)
    gamelib.resize(CELDA * dimensiones[0], CELDA * dimensiones[1])
    dibujar_piso(dimensiones)
    dibujar_objetos(juego, dimensiones)

    if not pistas.esta_vacia():
        gamelib.draw_text("Pista Disponible!", 65, 10, fill="black")
    elif buscando_pistas:
        gamelib.draw_text("Buscando Pistas...", 65, 10, fill="black")

    gamelib.draw_end()

def dibujar_piso(dimensiones):
    """Dibuja el piso en todo el nivel."""
    for f in range(dimensiones[1]):
        for c in range(dimensiones[0]):
            gamelib.draw_image(PISO, c * CELDA, f * CELDA)  

def dibujar_objetos(juego, dimensiones):
    """Dibuja los objetos que hayan en el nivel."""
    for f in range(dimensiones[1]):
        for c in range(dimensiones[0]):
            if soko.hay_pared(juego, c, f):
                dibujar_imagen(c, f, PARED)
            if soko.hay_jugador(juego, c, f):
                dibujar_imagen(c, f, JUGADOR)
            if soko.hay_caja(juego, c, f):
                dibujar_imagen(c, f, CAJA)
            if soko.hay_objetivo(juego, c, f):
                dibujar_imagen(c, f, OBJETIVO)

def dibujar_imagen(c, f, imagen):
    """Dibuja una imagen en la columna y fila recibida."""
    gamelib.draw_image(imagen, c * CELDA, f * CELDA)

def main():
    niveles = cargar_niveles()
    teclas = cargar_teclas()
    juego = soko.crear_grilla(niveles[0])
    nivel_actual = 0

    acciones_hechas = Pila()
    pistas = Pila()

    while gamelib.is_alive():
        juego_mostrar(juego, pistas)

        ev = gamelib.wait(gamelib.EventType.KeyPress)
        if not ev:
            break

        tecla = ev.key
        if not tecla in teclas:
            continue
        if teclas[tecla] == "SALIR":
            break
        if teclas[tecla] == "REINICIAR":
            juego = soko.crear_grilla(niveles[nivel_actual])
        else:
            juego = juego_actualizar(juego, teclas[tecla], pistas, acciones_hechas)

        if soko.juego_ganado(juego):
            acciones_hechas = Pila()
            pistas = Pila()
            nivel_actual += 1
            if nivel_actual == len(niveles):
                break
            juego = niveles[nivel_actual]

gamelib.init(main)