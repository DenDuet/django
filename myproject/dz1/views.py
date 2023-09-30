from django.shortcuts import render
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    logger.info('Index page accessed')
    return render(request, "base.html", context = {"body": "index page", "title":"Главная страница"})

def about(request):
    logger.info('About page accessed')
    return render(request, "about.html", context = {"body": "about page", "title":"Страница обо мне"})