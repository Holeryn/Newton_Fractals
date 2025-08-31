import pygame
import numpy as np
import math
import cmath
import newton_fractal as nw


def f(z):
    return z**3-1

def disegna_assi(screen, origine_x, origine_y, w, h, scala_x, scala_y, passo_pixel=50):
    colore_assi = (255, 255, 255)
    spessore = 1
    font = pygame.font.SysFont('Arial', 14)

    pygame.draw.line(screen, colore_assi, (0, origine_y), (w, origine_y), spessore)
    pygame.draw.line(screen, colore_assi, (origine_x, 0), (origine_x, h), spessore)

    screen.blit(font.render("Re", True, colore_assi), (w-30, origine_y-20))
    screen.blit(font.render("Im", True, colore_assi), (origine_x+5, 5))

    for i in range(0, w, passo_pixel):
        x_val = (i - origine_x) * scala_x
        screen.blit(font.render(f"{x_val:.2f}", True, colore_assi), (i-10, origine_y+5))
        pygame.draw.line(screen, colore_assi, (i, origine_y-3), (i, origine_y+3), 1)

    for j in range(0, h, passo_pixel):
        y_val = (origine_y - j) * scala_y
        screen.blit(font.render(f"{y_val:.2f}", True, colore_assi), (origine_x+5, j-7))
        pygame.draw.line(screen, colore_assi, (origine_x-3, j), (origine_x+3, j), 1)


scala = 1
pygame.init()
w, h = 600, 600
origine_x, origine_y = w/2, h/2
R_x = 1 * math.pi*scala
R_y = 1.5*scala
scala_x = (2.5*R_x)/w
scala_y = (2.5*R_y)/h

screen = pygame.display.set_mode((w, h))
array = np.zeros((w, h, 3), dtype=np.uint8)

def wait():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

i_arr = np.arange(w)
j_arr = np.arange(h)

# Questa è una hack della vetorializazzione calcolo direttamente tutte
# le combinazioni in 600X600 (OVVIAMENTE dilatate e traslate correttamente)
# cambio il segno perchè euristicamente altrimenti mi trovo una figura specchiata
x_grid = -((i_arr[:, None] - origine_x) * scala_x)  
y_grid = (j_arr[None, :] - origine_y) * scala_y

print("Inizio...")
valori_pixel = nw.valori(f, x_grid, y_grid)
nw.fractal(array, valori_pixel)
print("Fine.")

radici_filtrate = nw.filtra_radici()
print("Radici filtrate:", radici_filtrate)
print("Numero di radici trovate: ",len(radici_filtrate))
pygame.surfarray.blit_array(screen, array)

disegna_assi(screen, origine_x, origine_y, w, h, scala_x, scala_y)

pygame.display.flip()
pygame.image.save(screen, "sin(z).png")

wait()
pygame.quit()
