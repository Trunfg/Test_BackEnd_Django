from urllib import request
from django.shortcuts import render
from rest_framework.views import APIView

class MainView(APIView):
    def get(self, request, format=None):
        return render(request, 'main.html')

class AboutView(APIView):
    def get(self, request, format=None):
        return render(request, 'about.html')