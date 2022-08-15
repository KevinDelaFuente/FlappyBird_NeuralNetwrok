import numpy as np
import scipy.special

class Nnet:

    def __init__(self, num_input, num_hidden, num_output):
        self.num_input = num_input
        self.num_hidden = num_hidden
        self.num_output = num_output
        self.weight_input_hidden = np.random(-.5,.5, size = (self.num_hidden, self.num_input))
        self.weight_hidden_output = np.random(-.5,.5, size = (self.num_output, self.num_hidden))
        self.activation_function = lambda x: scipy.special.expit(x)

    def get_outputs(self, inputs_list):
        inputs = np.array(inputs_list, ndmin = 2).T
        print('inputs', inputs, sep = '\n')
        hidden_inputs = np.dot(self.weight_input_hidden, inputs)
        print('hidden inputs', hidden_inputs, sep = '\n')
        hidden_outputs = self.activation_function(hidden_inputs)
        print('hidden outputs', hidden_outputs, sep = '\n')
        final_inputs = np.dot(self.weight_hidden_output, hidden_outputs)
        print('final inputs', final_inputs, sep = '\n')
        final_outputs = self.activation_function(final_inputs)
        print('final outputs', final_outputs, sep = '\n')
        return final_outputs

    def get_max_value(self, inputs_list):
        outputs = self.get_outputs(inputs_list)
        return np.max(outputs)

