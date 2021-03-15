'''
Author: Gabriele Martinero
file containing all the Django project's utilities
'''


import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import pandas as pd
from pandas import DataFrame, concat
#from scipy.signal import savgol_filter
import math
import joblib
from .model.model_utils import *
import os
import matplotlib.pyplot as plt
import matplotlib
import base64
import json
from io import BytesIO
from PIL import Image
matplotlib.use('Agg')

def handle_uploaded_file(file, data_type, algorithm_list):
	'''
	it takes the uploaded file and predicts the variable :a
	params: 
		-file: file containing the dataset
		-data type: the dataset type
		-algorithm_list: the list of the required model/models for predicting the data

	returns:
        -json_data: json document containing the results from the model prediction
    '''

	data, variable, data_headers, variable_found = read_data(file)
	prediction_list_as_array = []
	prediction_list = []

	for algorithm in algorithm_list:
		options = dict()

		options['variable_detected'] = variable_found
		options['dataset'] = data_type
		# 'LSTM' or 'MLP'
		options['algo_name'] = algorithm.upper()
		# 'z' or 'minmax'
		options['normalize'] = 'minmax'
		# for MLP use latent variables
		options['latent_vars'] = False
		if(options['algo_name'] == 'MLP'):
			options['latent_vars'] = True
		# the name of the trained model (ex: 'MLP-FBT.pt')
		options['model_name'] = algorithm.upper() + '-' + data_type.upper() +  '.pt'
		# print(  options['model_name'], flush=True)  #debug

		#predict the variable for the provided dataset
		prediction, variable, has_variable = predict_data(options, file,data,variable, data_headers)
		#append the predictions as array
		prediction_list_as_array.append(prediction)
		#append the predictions as list
		prediction_list.append(prediction.tolist())

	if(has_variable):
		#get the average error for each model
		mape_list = compute_average_error(prediction_list,variable)
		#plot data
		image = plot_difference(variable, prediction_list_as_array,options,file.name.split('.')[0],algorithm_list,mape_list)

	else:
		image = plot_variable(prediction_list_as_array[0],options,file.name.split('.')[0])

	json_data = encode_to_base64(image,prediction_list,variable)
	return json_data



def handle_weights_request(file):
	'''
	it takes the dataset file and evaluates how much each features influences the variable's prediction :
	params:
		-file: file containing the dataset used for the prediction

	returns:
        -json_data: json document containing the each feature's weight
    '''

	data, variable, headers, _ = read_data(file)

	weights,headers = predict_weights(data,variable,headers)
	data_for_plot = generate_data_for_plot(weights.tolist()[0])
	# print( data_for_plot, flush=True)
	raw_data = {'weights': weights.tolist()[0], 'headers':headers, 'plot_data': data_for_plot}
	json_data = json.dumps(raw_data, indent=2)
	return json_data


def generate_data_for_plot(weights):
	'''
	it generates data for each model's weight:
		params:
			-weights: the list of the model's weights
		returns:
			- data: the list of generated data for each model's weight
	'''
	data = []
	for weight in weights:
		d = np.linspace(0, 100, num=100)
		d = d * weight
		data.append(d.tolist())
	return data


def concat_data(data1, data2):
	return np.concatenate((data1, data2))

def compute_average_error(prediction_list, ground_truth_variable):
	'''
	it computes the average error for each model' s prediction required by the user: 
		params:
			-prediction_list: the list of prediction done by each model 
			-ground_truth_variable: array containing the gt variable 
		returns:
			- mape_list: list of the mean average percentage errors for each model required
	'''
	mape_list = []
	for _ ,model_prediction in enumerate(prediction_list):
		forecast_error = [ (ground_truth_variable[j]-model_prediction[j])/ground_truth_variable[j] for j in range(len(model_prediction))]
		forecast_error =  [abs(ele[0]) for ele in forecast_error] 
		mape_forecast_error = (sum(forecast_error)/len(forecast_error))*100
		mape_list.append(mape_forecast_error)
	return mape_list


def read_data(filename):
	'''
	it reads the uploaded data file and preprocess it:
		params:
			- filename: the dataset's filename

		returns:
			- data: the preprocessed data
			- variable: the predicted variable
			- options: the data's labels for each dataset's column
			- found_variable: whether the variable was detected or not in the provided dataset
	'''
	df = pd.read_excel(filename)

	# Drop NaN columns
	df.dropna(axis='columns', how='all', inplace=True)

	# Find variable and time column
	headers = list(df)
	used_headers = list()

	found_variable = False

	for i in headers:
    	#we remove the variable to predict  from the provided dataset (if it is found)
		if 'var' in i.lower():
			variable_df = df[[i]].copy()
			df.drop(i, axis=1, inplace=True)
			found_variable = True
		#we drop what is useless for our prediction
		elif 'time' in i.lower():
			df.drop(i, axis=1, inplace=True)
		elif 'cof' in i.lower():
			df.drop(i, axis=1, inplace=True)
		else:
			used_headers.append(i.lower().split()[0])

	# Split into X (features) and Y (labels)
	data = df.to_numpy()
	data = data.astype('float32')

	if(found_variable):
		variable = variable_df.to_numpy()
		variable = variable.astype('float32')
	else:
		variable = None

	return (data, variable, used_headers, found_variable)


def plot_variable(Y,options,filename):
	'''
	it plots and saves the predicted variable: 
		params:
			- Y: the predicted variable
			- options: details about the user's request (dataType, model required)
			- filename: dataset's filename 
		returns:
			- img:image containing the plot with the prediction
	'''
	# print(Y,flush=True)
	time = range(len(Y))
	image = plt.figure()
	plt.plot(time, Y, color='orange')
	plt.legend(['variable'])
	plt.title('variable prediction')


	image.savefig('media/results/prediction-' + str(options['dataset']) + '-'\
	+ str(options['algo_name']) + '-' + str(filename) +  '.png')

	print('Predictions.png saved')
	img = Image.open('media/results/prediction-' + str(options['dataset']) + '-'\
	+ str(options['algo_name']) + '-' + str(filename) +  '.png')

	return img


def plot_difference(Y, Y_pred_list,options,filename,algorithm_list,mape_list):

	'''
	it plots and saves the difference between the predicted variable and the gt variable: 
		- Y: the ground truth variable
		- Y_pred_list: the list of the predicted variable by each chosen model
		- options: details about the user's request (dataType, model required)
		- filename = dataset's filename 
		returns:
			- image containing the plot with the predictions and the ground truth
	'''
	color_list = ['orange','green','pink']
	n_models = len(Y_pred_list)
	# Create and save the image
	image = plt.figure()
	for i in range(n_models):
		time = range(len(Y_pred_list[i]))
		Y = Y[:len(Y_pred_list[i])]

		plt.plot(time, Y_pred_list[i], color=color_list[i])
		plt.title('True data vs prediction')

	plt.plot(time, Y, color='black',alpha=0.6)	
	#show MAPE in plot
	for i in range(len(algorithm_list)):
		algorithm_list[i] += ' (mape:' + str(round(mape_list[i],1)) + '%)'

	algorithm_list.append('True data')
	plt.legend(algorithm_list)

	image.savefig('media/results/prediction-' + str(options['dataset']) + '-'\
	+ str(options['algo_name']) + '-' + str(filename) +  '.png')

	print('Predictions.png saved')
	img = Image.open('media/results/prediction-' + str(options['dataset']) + '-'\
	+ str(options['algo_name']) + '-' + str(filename) +  '.png')
	return img

def encode_to_base64(image,prediction_list,variable):
	'''
	it encodes the prediction plot as a base 64 image before sending it back:
		- image: image to be encoded 
		returns:
			- json containing the image as blob64 file
	'''
	buffer = BytesIO()
	image.save(buffer,format="PNG")                  
	image = buffer.getvalue()  
	encoded_string = base64.b64encode(image)
	base64_string = encoded_string.decode('utf-8')

	raw_data = {'plot': base64_string, 'prediction_list':prediction_list, 'variable': variable.tolist()}
	json_data = json.dumps(raw_data, indent=2)
	return json_data


