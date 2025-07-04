from .JobPost_App_Import import *
from django.db import models

class JobPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobposts')
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=500) 
    description = models.TextField() 
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200) 
    salary = models.CharField(max_length=220) 
    type = models.CharField(max_length=50)
    deadline = models.DateField() 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Applied(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applied")
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name="job_applied")
    resume = models.TextField(null=1)
    description = models.TextField(null=1)
    is_accepted = models.BooleanField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)