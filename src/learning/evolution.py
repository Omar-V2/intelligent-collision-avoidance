import numpy as np
import random

from src.game.agent import Agent
from src.common.constants import GameSettings, AgentSettings, NeuralNetworkSettings
from src.learning.neural_network import NeuralNetwork

class Evolution:
    def __init__(self, population, elitism, mutation_rate, population_size):
        self.population = population
        self.elitism = elitism
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        self.generation = 0
        self.best_fitness = 0

    def check_if_all_dead(self):
        """
        Checks if all the members of the population have died.
        """
        agent = self.population[0]
        if agent.death_count == len(self.population):
            return True
        return False

    def choose_parents(self):
        """
        Returns the n fittest members of the population
        where n is the elitism value.
        """
        self.population.sort(key=lambda x: x.fitness)
        return self.population[-self.elitism:]

    def create_child(self, first_parent, second_parent):
        """
        Takes two parents and creates a child by applying genetic crossover
        to their genes
        """
        child_genome = []
        first_parent_genome = first_parent.brain.convert_weights_to_genome()
        second_parent_genome = second_parent.brain.convert_weights_to_genome()
        for i in range(len(first_parent_genome)):
            if random.random > 0.5:
                child_genome.append(first_parent_genome[i])
            else:
                child_genome.append(second_parent_genome[i])
        child_weights = first_parent.brain.convert_genome_to_weights(child_genome)
        return self._create_agent(child_weights)

    def _create_agent(self, weights):
        """
        Returns an agent with a NN that matches with the rest of
        the population but with weights passed by argument.
        """
        brain = NeuralNetwork(
            input_units=NeuralNetworkSettings.INPUT_UNITS,
            hidden_layers=NeuralNetworkSettings.HIDDEN_LAYERS,
            hidden_units=NeuralNetworkSettings.HIDDEN_UNITS,
            outputs=NeuralNetworkSettings.OUTPUTS,
            new_weights=weights
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
        return starting_agent
