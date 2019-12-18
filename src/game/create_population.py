from src.game.agent import Agent
from src.learning.neural_network import NeuralNetwork
from src.common.constants import NeuralNetworkSettings, AgentSettings

def create_population(population_size):
    """
    Creates the starting generation/population of agents.
    """
    population = []
    for _ in range(population_size):
        brain = NeuralNetwork(
            input_units=NeuralNetworkSettings.INPUT_UNITS,
            hidden_layers=NeuralNetworkSettings.HIDDEN_LAYERS,
            hidden_units=NeuralNetworkSettings.HIDDEN_UNITS,
            outputs=NeuralNetworkSettings.OUTPUTS,
            new_weights=False
        )
        starting_agent = Agent(
            x=AgentSettings.START_X,
            y=AgentSettings.START_Y,
            size=AgentSettings.SIZE,
            field_of_view=AgentSettings.FIELD_OF_VIEW,
            nb_sensors=AgentSettings.NB_SENSORS,
            max_range=AgentSettings.MAX_RANGE,
            manager=None,
            brain=brain
        )
        population.append(starting_agent)
    return population
    