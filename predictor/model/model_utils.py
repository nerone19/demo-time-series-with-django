'''
Author: Gabriele Martinero
utils used for training the neural network model
'''


import torch
import torch.nn as nn
import numpy as np
import math	
#from lstm import LSTMModel
from .models import MLP,LSTMModel
from sklearn.preprocessing import MinMaxScaler
import torch.optim as optim
import os


def predict_data(options, file, data, variable, data_headers):
    '''it predict the variable using the model/dataset required by the user.
        parameters:
            -options: Description of the request done by the user
            -file: file containing the dataset used for the prediction
            -variable: variable to predict if the dataset was given with the ground truth
            -data_header = file's headers used for labeling each column in the dataset
            -algorithm: required model for processing the data
        returns:
            -pred_array: it contains the denormalized predicted variable
    '''

    if(options['variable']):
        data, _, scaler = normalize(data, variable)
    else:
        data, scaler = normalize_X(data)

    # add latent_variables for MLP
    if(options['latent_vars']):
        data, data_headers = add_latent_variables(data, data_headers)

    options['offset'] = 20

    hidden_size = 200
    seq_len = 1500
    #num_layers = 1
    batch_size = 1
    output_size = 1
    features_in = np.size(data, 1)

    test_batches = math.floor(len(data) / seq_len*batch_size)
    #print('Nr of test batches: ', test_batches)


    if(options['algo_name'] == 'MLP'):
        model = MLP(features_in, 1)
    elif(options['algo_name'] == 'LSTM'):
        model = LSTMModel(seq_len, test_batches,
                        features_in, hidden_size, output_size)

    criterion = nn.L1Loss()

    model_path = os.path.join(os.path.dirname(__file__),options['model_name']) 
    print(  model_path, flush=True)
    checkpoint  = torch.load(model_path)
    
    model.load_state_dict(checkpoint)

    model.eval()
    predictions = []
    test_error = []

    print('Testing ...')

    if(options['variable_detected'] == False):
        variable = np.zeros((data.shape[0], 1))

    with torch.no_grad():
        # Prepare the sequence and turn it into tensor
        X, Y = prepare_train_no_repeat(
            data, variable, seq_len, test_batches, False)
        # Make predictions
        Y_pred = model(X)

        # If variable was detected, calculate test_error
        if(options['variable_detected']):
            loss = criterion(Y_pred, Y)
            test_error.append(loss.numpy())

        # Save the predictions
        predictions.append(Y_pred.numpy())

    pred_array = np.array(predictions)

    pred_array = pred_array.reshape(-1, 1)
    print(pred_array.shape)
    if(options['variable_detected']):
        pred_array = scaler.inverse_transform(pred_array.reshape(-1, 1))

    print('Finished testing ...')
    return pred_array


def predict_weights(data,variable,headers):
    '''
    it computes the weights used to predict the variable
    parameters: 
    -data: data used for training the neural model
    -variable: ground truth variable data 
    -file's headers used to label each column

    returns:
    -json_data: json document containing 
    '''
    data_scaled, variable_scaled, scaler = normalize(data, variable)

    #hyperparameters
    epochs = 10000
    learning_rate = 0.0003
    hidden_size = 200
    seq_len = 1500
    num_layers = 1
    batch_size = 1
    output_size = 1
    features_in = np.size(data, 1)

    #model
    model = MLP(features_in, 1)

    loss_function = nn.L1Loss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    train_batches = math.floor(len(data) / seq_len)

    training_loss = []
    threshold = 0.0000001
    x_stop_set = False

    for epoch in range(epochs):
        # Clear the gradients
        optimizer.zero_grad()

        # Prepare the input and turn it into tensor
        X, Y = prepare_train_no_repeat(data_scaled, variable_scaled, seq_len, train_batches, False)
        # Run the forward pass
        Y_pred = model(X)
        # Compute the loss
        loss = loss_function(Y_pred, Y)

        loss.backward()
        # Update the parameters
        optimizer.step()
        training_loss.append(loss.item())
        
        if epoch > 0 and x_stop_set == False:
            if(training_loss[epoch-1] - training_loss[epoch] < threshold):
                x_stop = epoch
                x_stop_set = True
                print('Learning stopped at: ', epoch)
                break

        if epoch % 500 == 0:
            print(epoch)

    for param_tensor in model.state_dict():
        weights = model.state_dict()[param_tensor].numpy()
        break

    return weights,headers


def add_latent_variables(data, headers):
    '''it combines features in pairs to augment the data
        parameters: 
        - data: the original dataset
        - header: dataset's headers containing the label for each column of the dataset

        returns: 
        - data: it contains the new dataset containing the appended latent variables' s data

    '''
    n, m = data.shape

    # Tracking variable
    cnt = 0

    # Calculate nr of latent variables
    nr_latent_vars = math.factorial(m)

    # Create the variable
    latent_variables = np.zeros((n, nr_latent_vars))

    new_headers = list()

    # Get the latent variables
    for i in range(m):
        for j in range(i, m):
            latent_variables[:, cnt] = data[:, i] * data[:, j]
            new_headers.append(headers[i] + '*' + headers[j])
            cnt += 1

    data = np.concatenate((data, latent_variables), axis=1)

    return data, (headers + new_headers)

def prepare_train_no_repeat(X, Y, seq_len, batches, shuffle):
    '''it prepares the dataset to be feeded to the model
        parameters: 
        - X: the data to-be-predicted selected by the given dataset
        - y: the ground-truth selected by the given dataset
        - seq_len: the time series's sequence lenght
        - batches: the number of batches decided for splitting the data
    
        returns: 
        - tensor_X: float tensor containing the prepared to-be-predicted data
        - tensor_Y: float tensor containing the prepared ground-truth data
    '''

    #aux_Y = np.concatenate((np.zeros((1,1)), Y))
    #X = np.concatenate((X, aux_Y[:-1]), axis=1)

    array_X = np.zeros((batches, seq_len, X.shape[1]))
    array_Y = np.zeros((batches, seq_len, 1))

    array_X = X[:batches*seq_len, :].reshape((batches, seq_len, X.shape[1]))
    array_Y = Y[:batches*seq_len].reshape((batches, seq_len, 1))
    print('Shape of array_X: ', array_X.shape)
    tensor_X = torch.FloatTensor(array_X)
    tensor_Y = torch.FloatTensor(array_Y)

    return tensor_X, tensor_Y
    # return array_X, array_Y


def normalize_X(X):
    '''it scales only the to-be-predicted data between -1 and 1
    parameters: 
        - X: the data to-be-predicted selected by the given dataset
    returns: 
        - X : the normalized data

    '''
    scaler = MinMaxScaler(feature_range=(-1, 1))
    norm_X = scaler.fit_transform(X)
    return norm_X, scaler


def normalize(X, Y):
    '''it scales the to-be-predicted and the ground-truth data between -1 and 1
    parameters: 
        - X: the data to-be-predicted selected by the given dataset
        - Y: the ground-truth selected by the given dataset
    returns: 
        - X : the normalized to-be-predicted data
        - Y : the normalized ground-truth data

    '''
    scaler = MinMaxScaler(feature_range=(-1, 1))
    norm_X = scaler.fit_transform(X)
    norm_Y = scaler.fit_transform(Y)
    return norm_X, norm_Y, scaler
