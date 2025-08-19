## Autore: Francesco Maria Celentano
# Per ogni funzione che si vuole graficare si  deve modificare 
# la definizione di f e il vettore degli zeri in newton_fractal.py.
# Fattio ciò si devono modificare anche i range del grafico.

import pygame
import numpy as np
import newton_fractal as nw
import cmath
import math

c = 1
def f(z): # Funzione su cui eseguire l'alogirtmo
    return z**3 - c 
    
def wait():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


pygame.init()
w, h = 600, 600
origine_x = w // 2
origine_y = h // 2
R_x = 1 * math.pi   # range orizzontale
R_y = 1.5             # range verticale
scala_x = (2*R_x) / w
scala_y = (2*R_y) / h

screen = pygame.display.set_mode((w, h))

array = np.zeros((w, h, 3), dtype=np.uint8)

## (i,j) rappresenterà il numero complesso i + Ij
print("Inizio")
for i in range(w):
    for j in range(h):
        x = (i - origine_x) * scala_x
        y = (j - origine_y) * scala_y
        valori = nw.valori(f,x,y)
        nw.fractal(array,valori,i,j)
print("Fine")    


## Copia la matrice su schermo e lo aggiorna
pygame.surfarray.blit_array(screen, array)
pygame.display.flip()

pygame.image.save(screen, "asas.png")
wait()

pygame.quit()
