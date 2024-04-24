import numpy as np
import pandas as pd


class LineFollowerAgent:
    def __init__(self, environment):
        self.data = []
        self.environment = environment
        self.x, self.y = self.find_starting_position()
        self.orientation = '▲'
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

    def find_starting_position(self):
        # Buscar la primera posición que contenga una línea oscura.
        # Asumimos que '1' representa una línea oscura.
        positions = np.argwhere(self.environment == 1)
        if positions.size > 0:
            return positions[0]  # Retorna la primera posición encontrada.
        else:
            raise ValueError("No dark lines found in the environment to start.")

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
            '►': ((0, 1), (1, 1), (2, 1)),
            '▼': ((1, 1), (1, 0), (1, -1)),
            '◄': ((0, -1), (-1, -1), (-2, -1))
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

        # Checkea si el movimiento hacia adelante es posible
        dx, dy = self.movements[self.orientation]
        new_x, new_y = self.x + dx, self.y + dy
        if not (0 <= new_x < self.environment.shape[0] and 0 <= new_y < self.environment.shape[1]):
            # Si moverse hacia adelante está fuera de los límites, considerar rotar en su lugar
            return 'Rotar +90'

        # Existing rules
        if current == 'Piso Oscuro' and center == 'Piso Oscuro':
            return 'Avanzar'
        elif center == 'Piso Oscuro':
            return 'Avanzar'
        elif left == 'Piso Oscuro':
            return 'Rotar -90'
        elif right == 'Piso Oscuro':
            return 'Rotar +90'
        else:
            return 'Avanzar'

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

    def run(self):
        iterations = 0
        while True:
            perceptions = self.perceive_environment()
            action = self.choose_action(perceptions)
            self.perform_action(action)
            print(
                f"Iteracion {iterations}: Posicion = ({self.x}, {self.y}), Orientacion = {self.orientation}, Accion = {action}")

            self.data.append({
                'N': iterations,
                'Pos': (agent.x, agent.y),
                'Orienta': agent.orientation,
                'Cámara': perceptions[0],
                'Contacto': 'No pared' if perceptions[1] != 'Borde' else 'Pared',
                'Regla': '',
                'Acción': action,
                'Pos after': (agent.x, agent.y),
                'Orie after': agent.orientation
            })

            iterations += 1

            if iterations > 100:
                print("Terminating after 100 iterations.")
                break
            # time.sleep(0.5)

        return self.data


def generate_environment(rows, cols):
    # Inicializa el ambiente con todas las celdas limpias (0)
    environment = np.zeros((rows, cols))

    # Agrega algunas celdas oscuras (1) representando las líneas que seguirá el agente
    # Para simplificar, hagamos una línea vertical recta en el medio
    environment[:, cols // 2] = 1

    # Añade paredes (2) alrededor del perímetro
    environment[0, :] = 2
    environment[-1, :] = 2
    environment[:, 0] = 2
    environment[:, -1] = 2

    return environment


# Crear un ambiente de 10x10
environment = generate_environment(10, 10)

agent = LineFollowerAgent(environment)
table = agent.run()
df = pd.DataFrame(table)
df.to_csv('data.csv', index=False)
