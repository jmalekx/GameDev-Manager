from django.shortcuts import render
from django.http import JsonResponse
from .models import Developer, Game


def test_api_view(request):
    return JsonResponse({
        'message': 'Good response!'
    })

def developer_api_view(request):
    return JsonResponse({
        'developers': [
            developer.as_dict() 
            for developer in Developer.objects.all()
        ]
    })

def game_api_view(request):
    return JsonResponse({
        'games': [
            game.as_dict() 
            for game in Game.objects.all()
        ]
    })
