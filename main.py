import pygame
import numpy as np
import math
import cmath
import newton_fractal as nw

def f(z):
    return np.cos(z)

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
        pygame.draw.line(screen, colore_assi, (origine_x-3, j), (origine_x+3, j), 1)



scala = 0.1
pygame.init()
w, h = 600, 600
origine_x, origine_y = w/2, h/2
R_x = 1 * math.pi*scala
R_y = 1.5*scala
scala_x = (2.5*R_x)/w
scala_y = (2.5*R_y)/h

# La finestra contiene due immagini
screen = pygame.display.set_mode((w*2, h))
pygame.display.set_caption("Frattale e Lyapunov Newton")

surface_frac = pygame.Surface((w, h))
surface_lyap = pygame.Surface((w, h))

i_arr = np.arange(w)
j_arr = np.arange(h)
x_grid = -((i_arr[:, None] - origine_x) * scala_x)
y_grid = (j_arr[None, :] - origine_y) * scala_y
Z = x_grid + 1j*y_grid

# Frattale di Newton
print("Calcolo frattale...")
array_frac = np.zeros((w, h, 3), dtype=np.uint8)
valori_pixel = nw.valori(f, x_grid, y_grid)
nw.fractal(array_frac, valori_pixel)
pygame.surfarray.blit_array(surface_frac, array_frac)
disegna_assi(surface_frac, origine_x, origine_y, w, h, scala_x, scala_y)
print("Frattale pronto.")

print("Lyapunov...")
ly = nw.lyapunov(f, Z) 
# Tolgo i valori infiniti per la visualizzazione
ly_clean = ly.copy()
ly_clean[np.isinf(ly_clean)] = np.min(ly_clean[~np.isinf(ly_clean)])

# i valori troppo grandi li metto True
threshold = 0.8  # regola in base ai tuoi valori
mask = ly_clean > threshold
rgb_lyap = np.zeros((w, h, 3), dtype=np.uint8)
rgb_lyap[mask] = [255, 255, 255]  # bianco, il resto rimane nero

pygame.surfarray.blit_array(surface_lyap, rgb_lyap)
disegna_assi(surface_lyap, origine_x, origine_y, w, h, scala_x, scala_y)
print("Lyapunov pronto.")

# Stampa le radici
radici_filtrate = nw.filtra_radici()
print("Radici filtrate:", radici_filtrate)
print("Numero di radici trovate: ",len(radici_filtrate))


screen.blit(surface_frac, (0,0))
screen.blit(surface_lyap, (w,0))
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
