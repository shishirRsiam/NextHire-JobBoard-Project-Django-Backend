from rest_framework import serializers
from .models import JobPost, Applied
from django.contrib.auth.models import User
from Category_App.serializers import CategorySerializer
from Category_App.models import Category
from Authentication_App.serializers import *



class JobPostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = JobPost
        fields = '__all__'
        read_only_fields = ('user',)
        
class ApplySerializer(serializers.ModelSerializer):
    job = JobPostSerializer()
    user = SimpleUserSerializer()
    class Meta:
        model = Applied
        fields = '__all__'
        read_only_fields = ('user',)



