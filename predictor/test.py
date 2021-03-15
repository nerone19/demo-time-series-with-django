'''
Author: Gabriele Martinero
file containing the unit test for the project
'''
#TESTS TO-DO:

#the uploaded file exists in server-side OK
#the prediction for the required dataset was successfully created
#datasets with only 4 columns are without any ground-truth
#check whether the data inserted was correctly processed
#if the dataset was already predicted with the same model, don't store the predicted dataset again
#can t predict a dataset containing the ground truth
#check whether tha dataset containing the ground truth was labeled in the database 

from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import *
import sys,os


#test over the customuser class
class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)

#test over the dataset creation
class DatasetTests(TestCase):


    def test_create_dataset(self):
        #sys.stderr.write(os.getcwd() + '\n')
        User = get_user_model()
        upload_file = open('./predictor/file_test/dataset.xlsx', 'rb')
        user = User.objects.create_user(email='normal@user.com', password='foo')
        dataset = Dataset(user=user, filename='test1', date=timezone.now(), data =upload_file )

        self.assertTrue(user is not None)
        self.assertEqual(dataset.user, user)
        self.assertEqual(dataset.filename, 'test1')
        self.assertTrue(upload_file is not None)
        self.assertFalse(dataset.ground_truth)
        self.assertEqual(dataset.data_type,'')
        self.assertIs(dataset.was_published_recently(), True)
        #old dataset with publishing date later than 1 day
        old_dataset = Dataset(user=user, filename='test1', date=timezone.now() - datetime.timedelta(days=1, seconds=1), data =upload_file,ground_truth = True )
        self.assertIs(old_dataset.was_published_recently(), False)
        self.assertTrue(old_dataset.ground_truth)
        recent_dataset = Dataset(user=user, filename='test1',date = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59), data =upload_file )
        #recent dataset with publishing date less than 1 day
        self.assertIs(recent_dataset.was_published_recently(), True)


#test over the predicted dataset creation
class PredictedDataset(TestCase):

    def create_predicted_dataset(self):
        User = get_user_model()
        user = User.objects.create_user(email='normal@user.com', password='foo')
        upload_file = open('./predictor/file_test/dataset.xlsx', 'rb')
        dataset = Dataset(user=user, filename='test1', date=timezone.now(), data =upload_file )
        ml_model = MlModel(short_name='MLP', long_name='multi-layer-perceptron', date=timezone.now() )
        #the line is only for testing(in the real case I should open the xslx or whatever extension file for opening the prediction before plotting the result )
        upload_predicted_file = open('./predictor/file_test/dataset.xlsx', 'rb')
        predicted_dataset = PredictedDataset(date=timezone.now(), data= upload_predicted_file, dataset = dataset, ml_model = ml_model)
        self.assertTrue(upload_predicted_file is not None)
        self.assertTrue(user is not None)
        self.assertTrue(dataset is not None)
        self.assertEqual(predicted_dataset.dataset, dataset)
        self.assertEqual(predicted_dataset.ml_model, ml_model)
        self.assertTrue(predicted_dataset.date > dataset.date)


#test over the ml model creation
class MlModel(TestCase):
    def create_ml_model(self):
        ml_model = MlModel(short_name='MLP', long_name='multi-layer-perceptron', date=timezone.now() )
        self.assertEqual(dataset.short_nameer, 'MLP')
        self.assertEqual(dataset.long_name, 'multi-layer-perceptron')
        self.assertIs(dataset.was_published_recently(), True)
        self.assertTrue(upload_file is not None)

        #old model with publishing date later than 1 day
        old_ml_model = MlModel(short_name='MLP', long_name='multi-layer-perceptron', date=timezone.now() - datetime.timedelta(days=1, seconds=1) )
        self.assertIs(old_ml_model.was_published_recently(), False)
        recent_ml_model = MlModel(short_name='MLP', long_name='multi-layer-perceptron', date=timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59) )
        #recent model with publishing date less than 1 day
        self.assertIs(recent_ml_model.was_published_recently(), True)

