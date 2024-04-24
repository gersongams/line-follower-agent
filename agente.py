import sys
import time

import numpy as np
import pygame

# Initialize pygame
pygame.init()

# Inicializar el ambiente
VACIO = '0'
BASURA = 'B'
OBSTACULO = 'O'
PARED = 'P'
AGENTE = 'A'  # Usaremos 'A' para representar al agente

# Crear un ambiente de 9x9 con paredes alrededor
ambiente = np.array([
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'O', '0', 'B', '0', 'B', 'O', 'A', 'P'],
    ['P', 'B', 'B', '0', 'B', 'O', '0', 'B', 'P'],
    ['P', 'B', '0', 'B', 'B', '0', '0', '0', 'P'],
    ['P', 'O', '0', '0', 'O', '0', 'O', 'O', 'P'],
    ['P', '0', 'O', '0', '0', '0', '0', '0', 'P'],
    ['P', '0', 'B', 'B', 'O', 'O', '0', '0', 'P'],
    ['P', 'B', 'O', 'O', '0', '0', 'B', 'O', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
])

# Posición inicial del agente
x, y = 1, 7  # Posición (1, 7) en términos de índice cero
orientacion = 'R'  # Orientado hacia la derecha

# Set up some constants
CELL_SIZE = 50  # Size of each cell in pixels
WIDTH, HEIGHT = ambiente.shape[1] * CELL_SIZE, ambiente.shape[0] * CELL_SIZE  # Window size
WHITE = (255, 255, 255)  # Color for empty cells
BLACK = (0, 0, 0)  # Color for obstacles
RED = (255, 0, 0)  # Color for obstacles
BROWN = (165, 42, 42)  # Color for garbage
BLUE = (0, 0, 255)  # Color for the agent

screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Función para detectar basura
def detectar_basura(x, y):
    return ambiente[x, y] == 'B'


# Función para detectar contacto
def detectar_contacto(x, y, orientacion):
    movimientos = {'R': (0, 1), 'L': (0, -1), 'T': (-1, 0), 'B': (1, 0)}
    dx, dy = movimientos[orientacion]
    nuevo_x, nuevo_y = x + dx, y + dy
    if 0 <= nuevo_x < ambiente.shape[0] and 0 <= nuevo_y < ambiente.shape[1]:
        return ambiente[nuevo_x, nuevo_y] in ('P', 'O')
    else:
        return True  # Consider out of bounds as a contact


# Function to draw the grid
def draw_grid():
    for i in range(ambiente.shape[0]):
        for j in range(ambiente.shape[1]):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if ambiente[i, j] == 'P':
                pygame.draw.rect(screen, BLACK, rect)
            elif ambiente[i, j] == 'O':
                pygame.draw.rect(screen, BLACK, rect)
            elif ambiente[i, j] == 'B':
                pygame.draw.rect(screen, BROWN, rect)
            elif ambiente[i, j] == 'A':
                pygame.draw.rect(screen, BLUE, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)


# Ciclo de operaciones del agente
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    ambiente[x, y] = '0'  # Set current position to empty
    if detectar_basura(x, y):
        print("Succionar basura")
        ambiente[x, y] = '0'  # Limpia la basura
    elif detectar_contacto(x, y, orientacion):
        print("Rotar -90 grados")
        orientacion = {'R': 'B', 'B': 'L', 'L': 'T', 'T': 'R'}[orientacion]
    else:
        print("Avanzar")
        movimientos = {'R': (0, 1), 'L': (0, -1), 'T': (-1, 0), 'B': (1, 0)}
        dx, dy = movimientos[orientacion]
        x += dx
        y += dy

    ambiente[x, y] = 'A'  # Set new position to agent
    # Mostrar estado actual del agente
    print(f"Posición: ({x}, {y}), Orientación: {orientacion}")

    draw_grid()
    pygame.display.flip()
    time.sleep(0.5)  # Pause after each action
