import numpy as np


class NeuralNetwork:
    """
    A neural network class for the vanilla feedforward architecture.
    Only forward propagation is implemented as per the needs of this project.
    """

    def __init__(self, input_units, hidden_layers, hidden_units, outputs, new_weights=False):
        self.input_units = input_units
        self.hidden_layers = hidden_layers
        self.hidden_units = hidden_units
        self.outputs = outputs
        if new_weights:
            self.weights = new_weights
        else:
            self.weights = self.create_weights()

    def activation(self, z, tanh=True):
        """
        The activation function used in the neural network
        can be either the hyperbolic tanget or the logistic function.
        """
        if tanh:
            return np.tanh(z)
        else:
            return 1 / (1 + np.exp(-z))

    def forward(self, initial_x):
        """
        Performs forward propagation on an initial given input matrix, x
        """
        new_x = self.activation(np.dot(initial_x, self.weights[0]))
        for i in self.weights[1:]:
            new_x = np.dot(new_x, i)
            new_x = self.activation(new_x)
        return new_x

    def create_weights(self):
        """
        Returns an multi-dimensional np array which serve as the starting weights
        for the neural network, these weights are intiliased randomly
        from a normal distribution.
        """
        w_first = np.random.randn(self.input_units, self.hidden_units)
        w_last = np.random.randn(self.hidden_units, self.outputs)
        weights = [w_first]
        for _ in range(self.hidden_layers - 1):
            weights.append(np.random.randn(
                self.hidden_units, self.hidden_units))
        weights.append(w_last)
        print(weights[0].shape)
        return weights

    def convert_weights_to_genome(self):
        """
        Takes the weights of the network as a mutli-dimensional np array
        and converts them into a single unrolled 1-D array (a genome)
        """
        return self.weights.flatten()

    def convert_genome_to_weights(self, genome):
        """
        Takes a 1-D np array, ther genome, and reshapes it into the n-dimensional
        np array where n is in accordance with the architecture defined by the neural
        network instnace.
        """
        return genome.reshape(self.weights.shape)
