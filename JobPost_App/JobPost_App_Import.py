from rest_framework import serializers, viewsets
from django.contrib.auth.models import User
from .response import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from Category_App.models import Category

from django.db.models import Q

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView