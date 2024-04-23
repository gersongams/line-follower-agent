import numpy as np

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


# Ciclo de operaciones del agente
while True:
    if detectar_basura(x, y):
        print("Succionar basura")
        ambiente[x, y] = '0'  # Limpia la basura
    elif detectar_contacto(x, y, orientacion):
        print("Rotar -90 grados")
        orientacion = {'R': 'T', 'T': 'L', 'L': 'B', 'B': 'R'}[orientacion]
    else:
        print("Avanzar")
        movimientos = {'R': (0, 1), 'L': (0, -1), 'T': (-1, 0), 'B': (1, 0)}
        dx, dy = movimientos[orientacion]
        x += dx
        y += dy

    # Mostrar estado actual del agente
    print(f"Posición: ({x}, {y}), Orientación: {orientacion}")
    input("Presione Enter para continuar...")  # Pausa después de cada acción
