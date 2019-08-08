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
    POPULATION_SIZE = 1
    ELITISM = 0
    MUTATION_RATE = 0

class NeuralNetworkSettings:
    INPUT_UNITS = AgentSettings.NB_SENSORS
    HIDDEN_UNITS = 5
    HIDDEN_LAYERS = 2
    OUTPUTS = 2
