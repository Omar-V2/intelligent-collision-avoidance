import pygame
from src.game.game_settings import GameSettings, EvolutionSettings
from src.game.create_population import create_population

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
    pygame.draw.circle(SCREEN, (255, 10, 0), TARGET_LOCATION, 10, 0)

agents = create_population(POPULATION_SIZE)

def run():
    """
    Begins the simulation
    """
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        static_environment()
        for agent in agents:
            agent.move()
            agent.update(SCREEN)
        pygame.display.update()


if __name__ == "__main__":
    run()
