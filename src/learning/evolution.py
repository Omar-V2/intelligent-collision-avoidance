import random
from bisect import bisect_left
from itertools import accumulate

from src.common.constants import AgentSettings, NeuralNetworkSettings
from src.game.agent import Agent
from src.learning.neural_network import NeuralNetwork


class Evolution:
    """
    This Evolution class is responsible for applying the genetic
    algorithm which will evolve the agents towards a successful solution.
    """

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
        if Agent.death_count >= len(self.population):
            return True
        return False

    def _get_cumulative_fitness(self):
        """
        Returns the cumulative fitnesses of the population,
        these are then treated as the probabilites for selection
        of each agent in the roulette wheel selection strategy.
        """
        self.population.sort(key=lambda x: x.fitness)
        fitness_values = [p.fitness for p in self.population]
        fitness_sum = sum(fitness_values)
        relative_fitness_values = [(v / fitness_sum) for v in fitness_values]
        cumulative_fitness = list(accumulate(relative_fitness_values))
        return cumulative_fitness

    def _choose_parents(self):
        """
        Returns the n fittest members of the population
        where n is the elitism value. Truncation selection
        """
        self.population.sort(key=lambda x: x.fitness)
        fittest = self.population[-self.elitism:]
        return random.choice(fittest)

    def _choose_parents_roulette(self, cumulative_fitness):
        """
        Employes the roulette wheel selection strategy to
        select a parent.
        see: https://en.wikipedia.org/wiki/Fitness_proportionate_selection
        This works poorly when the fitness values are close to one another.
        """
        parent_index = bisect_left(
            cumulative_fitness, random.uniform(0, cumulative_fitness[-1]))
        return self.population[parent_index]

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
        agent = Agent(
            x=AgentSettings.START_X,
            y=AgentSettings.START_Y,
            size=AgentSettings.SIZE,
            field_of_view=AgentSettings.FIELD_OF_VIEW,
            nb_sensors=AgentSettings.NB_SENSORS,
            max_range=AgentSettings.MAX_RANGE,
            manager=None,
            brain=brain
        )
        return agent

    def _create_child(self, first_parent, second_parent):
        """
        Takes two parents and creates a child by applying genetic crossover
        to their genes. Specifically, uniform crossover
        """
        child_genome = []
        first_parent_genome = first_parent.brain.convert_weights_to_genome()
        second_parent_genome = second_parent.brain.convert_weights_to_genome()
        for i in range(len(first_parent_genome)):
            if random.random() > 0.5:
                child_genome.append(first_parent_genome[i])
            else:
                child_genome.append(second_parent_genome[i])
        self._mutate(child_genome)
        child_weights = first_parent.brain.convert_genome_to_weights(child_genome)
        return self._create_agent(child_weights)

    def _mutate(self, genome):
        """
        Iterates through the genome of an individual candidate solution (an Agent)
        and has a chance, equal to the mutation rate, at changing the gene at each index
        to a new value.
        """
        for i in range(len(genome)):
            if random.random() < self.mutation_rate:
                genome[i] = random.gauss(0, 1)

    def make_next_generation(self):
        """
        Creates the next generation, by repeatedly selecting parents,
        creating a child until n children have been created where
        n is the population size.
        """
        # cumulative_fitness = self._get_cumulative_fitness()
        next_generation = []
        for _ in range(self.population_size):
            parent_one = self._choose_parents()
            parent_two = self._choose_parents()
            # parent_one = self._choose_parents_roulette(cumulative_fitness)
            # parent_two = self._choose_parents_roulette(cumulative_fitness)
            child = self._create_child(parent_one, parent_two)
            next_generation.append(child)
        Agent.death_count = 0
        self.population = next_generation
