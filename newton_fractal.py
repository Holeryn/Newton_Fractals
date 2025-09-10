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
    z_grid = x + 1j*y

    L = z_grid.copy() ## fa una copia della griglia iniziale
    for i in range(ITERAZIONI):
        L = newton(f,L)
    
    return L

# Inserisce nel punto x,y di array
# il giusto colore
# nero diverge
# bianco converge

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

def fractal(array, valori, tol=TOLLERANZA):
    valori_finali = valori.copy()
    distanze = np.array([np.abs(valori_finali - r) for r in radici])

    indici = np.argmin(distanze, axis=0)
    min_distanze = np.min(distanze, axis=0)


# Utilizzo due mappe diverse a seconda del numero di radici
# perchè con poche radici la mappa continua è brutta :(

    array[:] = (255, 255, 255)  # bianco
    for i, r in enumerate(radici):
        mask = min_distanze < tol
        mask &= (indici == i)
        if len(radici) <= 3:
            array[mask] = colori[i]
        else:
            h = i / max(1, len(radici)-1)
            rgb = cm.hsv(h)[:3]
            array[mask] = (np.array(rgb) * 255).astype(np.uint8)

    for r in radici:
       if np.any(np.abs(valori_finali - r) < tol):
         radici_trovate.append(r)

def filtra_radici(tolleranza=1e-4):
    radici_filtrate = []
    for r in radici_trovate:
        if all(abs(r - rf) > tolleranza for rf in radici_filtrate):
            radici_filtrate.append(r)
    return radici_filtrate


def lyapunov(f, z0, max_iter=100, delta=1e-10):
    Z = z0.copy().astype(np.complex128)  
    sum_log_deriv = np.zeros_like(Z, dtype=np.float64)

    for _ in range(max_iter):
        fZ = f(Z)
        dFZ = derivata(f, Z)

        mask = dFZ != 0
        Z_new = np.where(mask, Z - fZ / dFZ, Z)
        delta_Z = np.abs(Z_new - Z)
        sum_log_deriv = np.where(mask, sum_log_deriv + np.log(np.abs(dFZ)), sum_log_deriv)
        Z = Z_new

        # Convergenza
        if np.all(delta_Z < delta):
            break

    return sum_log_deriv / max_iter
