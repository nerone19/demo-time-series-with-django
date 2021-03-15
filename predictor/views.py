'''
Author: Gabriele Martinero
file containing the APIs used by the project.

'''
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .models import *
from .utils import *
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_dataset(request):

	if request.method == 'POST':
		if(request.FILES['dataset-file'] is not None):
			file = request.FILES['dataset-file']

		data_type = request.POST.get('data-type',"")
		algorithm_list = request.POST.get('model-type',"").split(",")


		User = get_user_model()
		user_obj = User.objects.get(id=request.user.id)
		print(file.name , flush = True)  #debug
		dataset = Dataset(user=user, filename='test1', date=timezone.now(), data =upload_file )
		return HttpResponse("Dataset uploaded")


#TODO: handle the login by the user
#TODO: register the user and add it to th db
def login(request):
    '''
	it handles the first user's request after the login: 
	- request: request done by the user
	returns:
        - context: the current algorithms, datasets available to the user
    '''
    ml_algorithm_list = MlModel.objects.all()

    User = get_user_model()
    print(request.user.id)  #debug
    user_obj = User.objects.get(id=request.user.id)
    print(user_obj) #debug
    dataset_list = Dataset.objects.all().filter(user__email = user_obj)
    print(ml_algorithm_list) #debug
    context = {'model_list':ml_algorithm_list, 'dataset_list': dataset_list}
    return render(request, 'index.html', context)

@csrf_exempt
def predict_dataset(request):
	'''
	it handles every variable prediction request by the user and it gives back results.
	params:
		- request: prediction request done by the user
	returns:
		- json: document containing the plot which show the variable prediction
	'''
	if request.method == 'POST':
		if(request.FILES['dataset-file'] is not None):
			file = request.FILES['dataset-file']
		else:
			return HttpResponse(status=404,message = 'no file uploaded')

		is_gt_present = request.POST.get('is-gt-present',False)
		data_type = request.POST.get('data-type',"")
		algorithm_list = request.POST.get('model-type',"").split(",")
		print(algorithm_list, flush=True)
		return HttpResponse(handle_uploaded_file(file, data_type, algorithm_list, is_gt_present ), content_type='application/json')

@csrf_exempt
def show_weights(request):
	'''
	handles any request for showing the weights of the dataset's variables.
	params:
		- request: prediction request done by the user
	returns:
		- json: document containing the dataset's weights
	'''
	file = request.FILES['dataset-file']
	return HttpResponse( handle_weights_request(file), content_type='application/json')