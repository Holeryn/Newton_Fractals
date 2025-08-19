import math

ITERAZIONI = 50
TOLLERANZA = 0.01

def derivata(f,x,h=TOLLERANZA):
    return ((f(x+h) - f(x)))/h


def newton(f,z):
    try:
        return z - f(z)/derivata(f,z)
    except ZeroDivisionError:
        print("divisione per zero")
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
radici = [
    1,
    complex(-0.5, math.sqrt(3)/2),
    complex(-0.5, -math.sqrt(3)/2)
]
colori = [(255,0,0), (0,255,0), (0,0,255)]  # rosso, verde, blu

def fractal(array, valori, x, y, tol=TOLLERANZA):
    zf = valori[-1]  # ultimo valore della lista
    
    if abs(zf) > 1000:   # diverge
        array[x, y] = (0, 0, 0)
        return
    
    # Controlla a quale radice è vicino
    for r, c in zip(radici, colori):
        if abs(zf - r) < tol:
            if(x > 300):
                array[-x, y] = c
            else:
                array[x, y] = c
            return
        
    # Se non è vicino a nessuna radice (oscilla/ciclo)
    array[x, y] = (255, 255, 255)
