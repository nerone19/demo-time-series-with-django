'''
Author: Gabriele Martinero
file which maps the URI request to the APIs
'''
from django.urls import path
from . import views

app_name = 'predictor'

urlpatterns = [
	path('', views.index, name='index'),	
	path('about/', views.index, name='index'),
	path('predict-dataset/', views.predict_dataset),	
	path('show-weights/', views.show_weights),
	path('save-dataset/', views.upload_dataset)
]