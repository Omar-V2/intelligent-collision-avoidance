import pygame
from src.common.constants import GameSettings, EvolutionSettings
from src.game.create_population import create_population
from src.game.create_map import create_map
from src.game.obstacle import Rectangle, Circle
from src.learning.evolution import Evolution

# game settings
pygame.init()
BACKGROUND_COLOUR = GameSettings.BACKGROUND_COLOUR
(WIDTH, HEIGHT) = GameSettings.WIDTH, GameSettings.HEIGHT
TARGET_LOCATION = GameSettings.TARGET_LOCATION
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GameSettings.CAPTION)
SCREEN.fill(BACKGROUND_COLOUR)

# GA hyperparameters
POPULATION_SIZE = EvolutionSettings.POPULATION_SIZE
ELITISM = EvolutionSettings.ELITISM


def static_environment():
    """
    Sets up some static elements in the pygame environment
    such as the background colour, the map boundary and the target.
    """
    SCREEN.fill(BACKGROUND_COLOUR)
    pygame.draw.rect(SCREEN, (255, 255, 255),
                     (10, 10, WIDTH - 20, HEIGHT - 20), 1)
    pygame.draw.circle(SCREEN, (255, 10, 0), TARGET_LOCATION, 10, 0)

agents = create_population(POPULATION_SIZE)
evolution = Evolution(agents, 10, 0.01, len(agents))
obstacles = create_map()

def run():
    """
    Begins the simulation
    """
    x_change = 0
    y_change = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -1
                elif event.key == pygame.K_RIGHT:
                    x_change = 1
                elif event.key == pygame.K_DOWN:
                    y_change = 1
                elif event.key == pygame.K_UP:
                    y_change = -1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
        static_environment()
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            # obstacle.move(x_change, y_change)
        for agent in evolution.population:
            agent.move(x_change, y_change)
            agent.update(SCREEN, obstacles)
        #     agent.evaluate_fitness()
        # if evolution.check_if_all_dead():
        #     evolution.make_next_generation()
        pygame.display.update()


if __name__ == "__main__":
    run()
