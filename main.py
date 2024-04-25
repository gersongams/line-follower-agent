import numpy as np
import pandas as pd
import pygame

CELL_SIZE = 40


class LineFollowerAgent:
    def __init__(self, environment):
        self.data = []
        self.environment = environment
        self.x, self.y = self.find_starting_position()
        self.orientation = '▼'
        self.orientation_map = {
            '▲': {'Rotar +90': '►', 'Rotar -90': '◄'},
            '►': {'Rotar +90': '▼', 'Rotar -90': '▲'},
            '▼': {'Rotar +90': '◄', 'Rotar -90': '►'},
            '◄': {'Rotar +90': '▲', 'Rotar -90': '▼'}
        }
        self.movements = {
            '▲': (-1, 0),
            '►': (0, 1),
            '▼': (1, 0),
            '◄': (0, -1)
        }
        self.orientation_to_letter = {
            '▲': 'N',
            '►': 'E',
            '▼': 'S',
            '◄': 'O'
        }

    def find_starting_position(self):
        # Busca una posición en la línea (1)
        line_positions = np.argwhere(self.environment == 1)

        for position in line_positions:
            # Checkea si es un buen punto de inicio, por ejemplo, no esquina
            x, y = position
            neighbors = self.environment[x - 1:x + 2, y - 1:y + 2]
            if np.sum(neighbors == 1) >= 3:  # Checkea si hay al menos 3 celdas de línea alrededor
                return position

        raise ValueError("No suitable starting line position found.")

    def perceive_environment(self):
        # Establecer percepciones por defecto
        perceptions = ['Piso no Oscuro', 'Borde', 'Borde', 'Borde']  # Valores predeterminados

        # Verificar el piso actual donde está el agente
        if 0 <= self.x < self.environment.shape[0] and 0 <= self.y < self.environment.shape[1]:
            current_floor = self.environment[self.x, self.y]
            perceptions[0] = 'Piso Oscuro' if current_floor == 1 else 'Piso no Oscuro'

        # Definir los movimientos posibles según la orientación
        movements = {
            '▲': ((-1, -1), (-1, 0), (-1, 1)),
            '►': ((-1, 1), (0, 1), (1, 1)),
            '▼': ((1, 1), (1, 0), (1, -1)),
            '◄': ((1, -1), (0, -1), (-1, -1))
        }

        # Obtener las posiciones de las celdas según la orientación
        if self.orientation in movements:
            directions = movements[self.orientation]
            for i, (dx, dy) in enumerate(directions, start=1):
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < self.environment.shape[0] and 0 <= ny < self.environment.shape[1]:
                    cell = self.environment[nx, ny]
                    if cell == 1:
                        perceptions[i] = 'Piso Oscuro'
                    elif cell == 0:
                        perceptions[i] = 'Piso no Oscuro'
                    elif cell == 2:
                        perceptions[i] = 'Borde'
                else:
                    perceptions[i] = 'Borde'  # Considerar fuera de límites como borde

        return perceptions

    def choose_action(self, perceptions):
        current, left, center, right = perceptions

        # Si el agente esta en 'Piso no Oscuro', pero 'Piso Oscuro' está adelante, avanzar
        if current == 'Piso no Oscuro' and center == 'Piso Oscuro':
            return 'Avanzar'

        # Si el agente está en 'Piso Oscuro' y 'Piso Oscuro' también está directamente adelante, continuar hacia adelante
        if current == 'Piso Oscuro' and center == 'Piso Oscuro':
            return 'Avanzar'

        # Si el agente esta en 'Piso Oscuro' pero no hay 'Piso Oscuro' adelante, decidir hacia donde girar
        elif current == 'Piso Oscuro':
            if left == 'Piso Oscuro':
                return 'Rotar -90'
            elif right == 'Piso Oscuro':
                return 'Rotar +90'
            # Si no hay 'Piso Oscuro' a los lados, y el agente estaba en el camino, debe girar
            else:
                return 'Rotar +90'

        # SI el agente no está en el camino, buscar el camino
        else:
            if left == 'Piso Oscuro':
                return 'Rotar -90'
            elif right == 'Piso Oscuro':
                return 'Rotar +90'
            # Si el agente esta rodeado por 'Piso no Oscuro', buscar el camino
            else:
                return 'Rotar +90'  # Sigue rotando hasta encontrar el camino

    def perform_action(self, action):
        if action == 'Avanzar':
            dx, dy = self.movements[self.orientation]
            new_x, new_y = self.x + dx, self.y + dy
            if 0 <= new_x < self.environment.shape[0] and 0 <= new_y < self.environment.shape[1]:
                self.x = new_x
                self.y = new_y
            else:
                print(f"Attempted move out of bounds to ({new_x}, {new_y}). Trying rotation instead.")
                self.orientation = self.orientation_map[self.orientation]['Rotar +90']
        elif action in ['Rotar +90', 'Rotar -90']:
            self.orientation = self.orientation_map[self.orientation][action]

    def draw_environment(self, screen):
        for i in range(self.environment.shape[0]):
            for j in range(self.environment.shape[1]):
                if self.environment[i, j] == 1:
                    color = (0, 0, 0)  # Dark lines
                elif self.environment[i, j] == 2:
                    color = (200, 200, 200)  # Walls
                else:
                    color = (255, 255, 255)  # Clear tiles
                pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def run(self):
        # Initialize pygame
        pygame.init()

        screen = pygame.display.set_mode((self.environment.shape[1] * CELL_SIZE,
                                          self.environment.shape[0] * CELL_SIZE))
        clock = pygame.time.Clock()

        running = True
        iterations = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Dibuja el ambiente
            self.draw_environment(screen)

            # Dibuja al gente
            pygame.draw.rect(screen, (0, 0, 255), (self.y * CELL_SIZE, self.x * CELL_SIZE, CELL_SIZE, CELL_SIZE))

            # Actualiza la pantalla
            pygame.display.flip()

            # Agent's behavior
            perceptions = self.perceive_environment()
            before_orientation = self.orientation
            before_pos = (self.x, self.y)
            action = self.choose_action(perceptions)

            # Debugging
            # print(f"Iteration {iterations}: Position = ({self.x}, {self.y}), Orientation = {self.orientation}")
            # print(f"Perceptions: {perceptions}, Chosen action: {action}")

            self.perform_action(action)

            self.data.append({
                'N': iterations,
                'Pos': before_pos,
                'Orienta': self.orientation_to_letter[before_orientation],
                'Cámara': perceptions[0],  # Camara debajo del agente
                'Contacto': 'No pared' if perceptions[1] != 'Borde' else 'Pared',
                'Regla': perceptions[1:].index('Piso Oscuro') if 'Piso Oscuro' in perceptions[1:] else 'No hay',
                'Acción': action,
                'Pos after': (self.x, self.y),
                'Orie after': self.orientation_to_letter[self.orientation]
            })

            iterations += 1
            if iterations > 100:
                running = False

            clock.tick(3)  # Controla la velocidad de la simulación

        pygame.quit()
        return self.data


# Dibuja un camino circular
def create_round_path_environment(size):
    environment = np.zeros((size, size))

    mid = size // 2
    radius_outer = mid - 1
    radius_inner = mid - 3

    y, x = np.ogrid[-mid:size - mid, -mid:size - mid]
    mask_outer = x ** 2 + y ** 2 <= radius_outer ** 2
    mask_inner = x ** 2 + y ** 2 <= radius_inner ** 2

    environment[mask_outer] = 1
    environment[mask_inner] = 0

    environment[0, :] = 2
    environment[-1, :] = 2
    environment[:, 0] = 2
    environment[:, -1] = 2

    environment[mid, 0:mid - radius_inner] = 0

    return environment


# Crear un ambiente de 25x25
environment = create_round_path_environment(25)

agent = LineFollowerAgent(environment)
table = agent.run()
df = pd.DataFrame(table)
df.to_csv('data.csv', index=False)
