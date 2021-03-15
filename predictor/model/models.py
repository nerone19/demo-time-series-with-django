'''
    file containing the NN models used for the task
'''

import torch
import torch.nn as nn

class MLP(nn.Module):
    '''
    class containing the multi layer perceptron architecture
    '''
    def __init__(self, input_size = 3, output_size = 1):
        super(MLP, self).__init__()
        # Parameters
        self.input_size = input_size
        self.output_size = output_size

        # Layers
        self.linear1 = nn.Linear(self.input_size, self.output_size)
        self.activation = nn.Tanh()


    def forward(self, x):
        out = self.linear1(x)
        out = self.activation(out)
        return out

class LSTMModel(nn.Module):
    '''
    class containing the long-short term memory architecture
    '''
    def __init__(self, seq_len = 4, batch_size = 64, input_size = 3, hidden_size = 64, output_size = 1, num_layers = 1):
        super(LSTMModel, self).__init__()

        # Parameters
        self.seq_len = seq_len
        self.batch_size = batch_size
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.num_layers = num_layers

        # Initialize hidden and cell state
        self.hidden = torch.randn(num_layers, batch_size, hidden_size)
        self.cell = torch.randn(num_layers, batch_size, hidden_size)

        # Layers
        self.lstm = nn.LSTM(self.input_size, self.hidden_size, self.num_layers, batch_first = True)
        #self.lstm2 = nn.LSTM(self.hidden_size, int(self.hidden_size/4), self.num_layers)
        #self.activation0 = nn.ReLU()
        self.linear = nn.Linear(self.hidden_size, self.output_size)
        self.activation = nn.Tanh()

    def forward(self, inputs):
        output, _ = self.lstm(inputs, (self.hidden, self.cell))
        #output2, _ = self.lstm2(output1)
        #output = self.activation0(output)
        predictions = self.linear(output)
        predictions = self.activation(predictions)

        return predictions
