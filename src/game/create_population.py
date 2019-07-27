from src.game.agent import Agent
from src.learning.neural_network import NeuralNetwork

def create_population(population_size):
    """
    Creates the starting generation/population of agents.
    """
    population = []
    for _ in range(population_size):
        brain = NeuralNetwork(
            input_units=9,
            hidden_layers=2,
            hidden_units=5,
            outputs=2,
            new_weights=False
        )
        starting_agent = Agent(
            x=175,
            y=300,
            size=10,
            field_of_view=360,
            nb_sensors=9,
            max_range=75,
            manager=None,
            brain=brain
        )
        population.append(starting_agent)
    return population
    