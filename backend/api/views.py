from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from .models import Developer, Game


def test_api_view(request):
    return JsonResponse({
        'message': 'Good response!'
    })

def developer_api_view(request):
    if request.method == 'GET':
        return JsonResponse({
            'developers': [
                developer.as_dict() 
                for developer in Developer.objects.all()
            ]
        })
    
    if request.method == 'POST':
        pass

    return HttpResponse(status=405)

def developer_detail_view(request,developer_id):
    developer = get_object_or_404(Developer, id=developer_id)

    if request.method == 'GET':
        return JsonResponse(developer.as_dict())
    
    if request.method == 'PUT':
        #handle put to update developer
        pass

    if request.method == 'DELETE':
        developer.delete()
        return HttpResponse(status=204)
    
    return HttpResponse(status=405)

def game_api_view(request):
    return JsonResponse({
        'games': [
            game.as_dict() 
            for game in Game.objects.all()
        ]
    })
