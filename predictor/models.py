'''
Author: Gabriele Martinero
file containing the fields and behaviors of the data we are going to store
'''

from django.db import models
from dateutil import parser
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone
import datetime

def user_directory_path(instance, filename):
    '''
    it returns the user's path where to save files
    '''
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class CustomUser(AbstractUser):
    '''
    class for storing the custom user (which uses the email as key) 
    '''
    username = models.CharField(max_length=50, null=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return "%s" % (self.email)

class Dataset(models.Model):
    '''
    class for storing the uploaded dataset by the user
    '''
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=False)
    filename = models.CharField(max_length=50, unique=True)
    #field for distinguishing whether the dataset has variable as ground_truth or not
    ground_truth = models.BooleanField(default = False) 
    data = models.FileField(blank=True,upload_to = user_directory_path)
    date = models.DateTimeField('date published')
    data_type = models.CharField(max_length=50, blank=True)


    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date <= now


    def __str__(self):
        return "%s %s %s" % (self.data_type,self.filename,self.user)

class MlModel(models.Model):
    '''
    class which stores the ml model for future usages. It is uploaded by the admin user
    '''
    id = models.AutoField(primary_key=True)
    short_name = models.CharField(max_length=10,unique=True)
    long_name = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField('date deployed')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date <= now

    def __str__(self):
        return "%s " % (self.short_name)
   
class PredictedDataset(models.Model):
    '''
    class which stores predicted variable
    '''
    
    id = models.AutoField(primary_key=True)
    #the prediction depends on the ml model 
    ml_model = models.ForeignKey(MlModel,on_delete=models.PROTECT)
    #the prediction used the features 
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    data = models.FileField(upload_to = user_directory_path)
    date = models.DateTimeField('date predicted')
    
    def __str__(self):
        return "%s %s" % (self.dataset,self.ml_model)


