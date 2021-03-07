PARED = "#"
CAJA = "$"
JUGADOR = "@"
OBJETIVO = "."
OBJETIVO_CAJA = "*"
OBJETIVO_JUGADOR = "+"

def crear_grilla(desc):
    '''Crea una grilla a partir de la descripción del estado inicial'''
    return desc

def dimensiones(grilla):
    '''Devuelve una tupla con la cantidad de columnas y filas de la grilla.'''
    filas = len(grilla)
    columnas = len(max(grilla, key=len))
    return (columnas, filas)

def hay_pared(grilla, c, f):
    '''Devuelve True si hay una pared en la columna y fila (c, f).'''
    return grilla[f][c] == PARED

def hay_objetivo(grilla, c, f):
    '''Devuelve True si hay un objetivo en la columna y fila (c, f).'''
    return grilla[f][c] == OBJETIVO or grilla[f][c] == OBJETIVO_CAJA or grilla[f][c] == OBJETIVO_JUGADOR

def hay_caja(grilla, c, f):
    '''Devuelve True si hay una caja en la columna y fila (c, f).'''
    return grilla[f][c] == CAJA or grilla[f][c] == OBJETIVO_CAJA

def hay_jugador(grilla, c, f):
    '''Devuelve True si el jugador está en la columna y fila (c, f).'''    
    return grilla[f][c] == JUGADOR or grilla[f][c] == OBJETIVO_JUGADOR

def juego_ganado(grilla):
    '''Devuelve True si el juego está ganado.'''
    for fila in grilla:
        for columna in fila:
            if OBJETIVO in columna or OBJETIVO_JUGADOR in columna:
                return False    
    return True

def mover(grilla, direccion):
    '''Mueve el jugador en la dirección indicada.'''
    c_jugador, f_jugador = econtrar_jugador(grilla)
    grilla_movida = grilla[:]
    
    if not puede_moverse(grilla, direccion, c_jugador, f_jugador):
        return grilla

    grilla_movida[f_jugador] = remover_jugador(grilla[f_jugador], c_jugador)

    grilla_movida[f_jugador + direccion[1]] = agregar_jugador(grilla_movida, f_jugador + direccion[1], c_jugador + direccion[0])

    if hay_caja(grilla, c_jugador + direccion[0], f_jugador + direccion[1]):
        grilla_movida[f_jugador + direccion[1] + direccion[1]] = agregar_caja(grilla_movida, f_jugador + direccion[1] + direccion[1], c_jugador + direccion[0] + direccion[0])
    
    return grilla_movida

def remover_jugador(fila, c_jugador):
    """Recibe la fila y la posicion donde esta el jugador y lo remueve de la misma"""
    cambio_fila = ""
    for i in range(len(fila)):
        if i != c_jugador:
            cambio_fila += fila[i]
            continue
        elif fila[i] == JUGADOR:
            cambio_fila += " "
        else: 
            cambio_fila += OBJETIVO
    return cambio_fila

def agregar_jugador(grilla, f, c):
    """Agrega al jugador a la fila y columna recibida"""
    cambio_fila = ""
    for i in range(len(grilla[f])):
        if i != c:
            cambio_fila += grilla[f][i]
            continue
        elif hay_objetivo(grilla, c, f):
            cambio_fila += OBJETIVO_JUGADOR
        else:
            cambio_fila += JUGADOR
    return cambio_fila

def agregar_caja(grilla, f, c):
    """Agrega una caja a la fila y columna recibida"""
    cambio_fila = ""
    for i in range(len(grilla[f])):
        if i != c:
            cambio_fila += grilla[f][i]
            continue
        elif hay_objetivo(grilla, c, f):
            cambio_fila += OBJETIVO_CAJA
        else:
            cambio_fila += CAJA
    return cambio_fila

def puede_moverse(grilla, direccion, c, f):
    """Devuelve True si el jugador puede moverse en la dirección indicada."""
    c_posible = c + direccion[0]
    f_posible = f + direccion[1]
    if hay_pared(grilla, c_posible, f_posible):
        return False
    elif hay_caja(grilla, c_posible, f_posible) and hay_caja(grilla, c_posible + direccion[0], f_posible + direccion[1]):
        return False
    elif hay_caja(grilla, c_posible, f_posible) and hay_pared(grilla, c_posible + direccion[0], f_posible + direccion[1]):
        return False
    return True

def econtrar_jugador(grilla):
    """Devuelve una tupla con la posición del jugador en la grilla."""
    for fila in range(len(grilla)):
        for columna in range(len(grilla[fila])):
            if hay_jugador(grilla, columna, fila):
                return (columna, fila)