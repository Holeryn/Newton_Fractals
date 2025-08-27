import math
import numpy as np
import matplotlib.cm as cm

ITERAZIONI = 50
TOLLERANZA = 1e-7

def derivata(f,x,h=TOLLERANZA):
    try:
        return ((f(x+h) - f(x)))/h
    except ValueError:
        print("Derivata failed")
        return 1

def newton(f,z):
    try:
        return z - f(z)/derivata(f,z)
    except ZeroDivisionError:
        print("divisione per zero")
        return 0
    except:
        return 0
    
def valori(f,x,y):
    z = complex(x,y)

    L = [z]
    for i in range(ITERAZIONI):
        L.append(newton(f,L[i]))
    
    return L

# Inserisce nel punto x,y di array
# il giusto colore
# nero diverge
# bianco converge
# colori ciclo

"""
# z^2 - 1
radici = [1,-1]
"""

"""
# z^3 - 1
radici = [(1+0j), (-0.5+0.8660254j), (-0.5-0.8660254j)]
"""


# cos(z)
N = 10
radici = [np.pi*(k-1/2) for k in range(-N,N+1)]


"""
# sin(z)
N = 10  # prendi k da -N a N
radici = [k*np.pi for k in range(-N, N+1)]
"""

"""
# sin(z) - 1
N = 10  # prendi k da -N a N
radici = [np.pi/2 + 2*np.pi*k for k in range(-N, N+1)]
"""

"""
# z^2sin(z)-1
radici = [-28.2755847, -25.1311579, -21.993216, -18.8467406, -15.712014,
 -12.5600316, -9.4360093, -6.257645, -3.2371649, 1.0682235,
  3.0326454, 6.3083168, 9.4134928, 12.5726969, 15.7039083,
 18.8523696, 21.9890804, 25.1343242, 28.2730829]
"""

radici_trovate = []
colori = [(255,0,0), (0,255,0), (0,0,255)]  # rosso, verde, 

def fractal(array, valori, x, y, tol=TOLLERANZA):
    zf = valori[-1]  # ultimo valore della lista

    if abs(zf) > 1e6:   # divergenza numerica
        array[x, y] = (0, 0, 0)
        return
    
    # Faccio il controllo qua per evitare di inserire
    # nella lista valori di divergenza
    if((zf in radici_trovate) == False):
        radici_trovate.append(zf)

# Applico un algoritmo di colorazione diverso
# quando la lunghezza di radici è piccola perchè
# l'algoritmo di colorazione basato su mappa continua
# genera un grafico noioso per poche radici tipo monocolore

    if(len(radici) <= 3):
        # Controlla a quale radice è vicino
        for r, c in zip(radici, colori):
            if abs(zf - r) < tol:
                array[x, y] = c
                return
    else:
        # Controlla a quale radice è vicino
        for i, r in enumerate(radici):
            if abs(zf - r) < tol:
                # scegli colore in base a indice radice
                h = i / max(1, len(radici)-1)   # normalizza [0,1]
                rgb = cm.hsv(h)[:3]             # colormap continua
                array[x, y] = tuple(int(255*v) for v in rgb)
                return

    # Se non converge a nessuna radice conosciuta
    array[x, y] = (255, 255, 255)


def filtra_radici(tolleranza=1e-4):
    radici_filtrate = []
    for r in radici_trovate:
        if all(abs(r - rf) > tolleranza for rf in radici_filtrate):
            radici_filtrate.append(r)
    return radici_filtrate

