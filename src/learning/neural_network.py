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
            self.weights = self._create_weights()

    def _activation(self, z, tanh=True):
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
        new_x = self._activation(np.dot(initial_x, self.weights[0]))
        for i in self.weights[1:]:
            new_x = np.dot(new_x, i)
            new_x = self._activation(new_x)
        return new_x

    def _create_weights(self):
        """
        Returns a list of np arrays which serve as the starting weights
        for the neural network, these weights are intiliased randomly
        from a normal distribution with mean 0.
        """
        w_first = np.random.randn(self.input_units, self.hidden_units)
        w_last = np.random.randn(self.hidden_units, self.outputs)
        weights = [w_first]
        for _ in range(self.hidden_layers - 1):
            weights.append(np.random.randn(
                self.hidden_units, self.hidden_units))
        weights.append(w_last)
        return weights

    def convert_weights_to_genome(self):
        """
        Takes the weights of the network as a list of np arrays
        and converts them into a single unrolled 1-D np array (a genome)
        """
        flattened_weights = [w.flatten() for w in self.weights]
        genome = np.concatenate(flattened_weights)
        return genome

    def convert_genome_to_weights(self, genome):
        """
        Takes a 1-D np array, the genome, and reshapes it into the a list of
        np arrays.
        """
        shapes = [np.shape(s) for s in self.weights]
        products = [i[0]*i[1] for i in shapes]
        weights = []
        start_idx = 0
        for i in range(len(products)):
            stop_idx = sum(products[:i+1])
            # reshape such that each weight matrix matches the original NN dimensions
            weight = np.reshape(genome[start_idx:stop_idx], shapes[i])
            weights.append(weight)
            start_idx += products[i]
        return weights
