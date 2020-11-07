from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Cource

# Create your views here.

def index(request):
    cources = Cource.objects.order_by('-id')
    context = {
        'title':'Главная страница сайта',
        'cources': cources,
    }
    return render(request, 'cource/index.html', context)

def cource(request, cource_id):
    try:
        cource = Cource.objects.get(id=cource_id)
    except:
        raise Http404("Курс не найден")
    
    schedule = cource.schedule_set.all()
    topics = cource.topic_set.all()
    context = {
        'cource':cource,
        'schedule': schedule,
        'topics': topics,
    }
    return render(request, 'cource/cource.html', context)