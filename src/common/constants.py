class GameSettings:
    BACKGROUND_COLOUR = (0, 0, 0)
    (WIDTH, HEIGHT) = (1000, 600)
    TARGET_LOCATION = (800, 300)
    CAPTION = "Evolution Simulation"

class AgentSettings:
    START_X = 175
    START_Y = 300
    SIZE = 10
    FIELD_OF_VIEW = 360
    NB_SENSORS = 9
    MAX_RANGE = 75

class EvolutionSettings:
    POPULATION_SIZE = 100
    ELITISM = int(POPULATION_SIZE / 10)
    MUTATION_RATE = 0.005

class NeuralNetworkSettings:
    INPUT_UNITS = AgentSettings.NB_SENSORS
    HIDDEN_UNITS = 16
    HIDDEN_LAYERS = 3
    OUTPUTS = 2
