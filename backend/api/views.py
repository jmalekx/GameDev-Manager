from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Developer, Game
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def test_api_view(request):
    """Handle test API requests.
    Returns a simple JSON response indicating the API is responsive.
    """
    return JsonResponse({
        'message': 'Good response!'
    })

@csrf_exempt
def developer_api_view(request):
    """Handle API requests for Developer model
    Supports GET (list all), POST (create new),
    PUT (update existing), and DELETE (to delete).
    """
    if request.method == 'GET':
        return JsonResponse({
            'developers': [
                developer.as_dict() 
                for developer in Developer.objects.all()
            ]
        })
    
    elif request.method == 'POST':
        #creating new dev
        data = json.loads(request.body)
        new_developer = Developer.objects.create(
            name=data['name'],
            about=data['about'],
            experience_years=data['experience_years'],
            available_to_hire=data['available_to_hire'],
            join_date=data['join_date'],
        )
        return JsonResponse(new_developer.as_dict(), status=201)
    
    elif request.method == 'PUT':
        #update existing
        data = json.loads(request.body)
        developer = get_object_or_404(Developer, pk=data['id'])
        developer.name = data.get('name', developer.name)
        developer.about = data.get('about', developer.about)
        developer.experience_years = data.get('experience_years', developer.experience_years)
        developer.available_to_hire = data.get('available_to_hire', developer.available_to_hire)
        developer.join_date = data.get('join_date', developer.join_date)
        developer.save()
        return JsonResponse(developer.as_dict())
    
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        developer = get_object_or_404(Developer, pk=data['id'])
        developer.delete()
        return JsonResponse({'message': 'Developer deleted'}, status=204)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def developer_detail_view(request,developer_id):
    """Handle API requests for specific developer
    """
    developer = get_object_or_404(Developer, id=developer_id)

    if request.method == 'GET':
        return JsonResponse(developer.as_dict())
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        developer.name = data.get('name', developer.name)
        developer.bio = data.get('bio', developer.bio)
        developer.experience_years = data.get('experience_years', developer.experience_years)
        developer.available_for_hire = data.get('available_for_hire', developer.available_for_hire)
        developer.join_date = data.get('join_date', developer.join_date)
        developer.save()
        return JsonResponse({'message': 'Developer updated successfully'})

    elif request.method == 'DELETE':
        developer.delete()
        return JsonResponse({'message': 'Developer deleted successfully'}, status=204)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def game_api_view(request):
    """Handle API requests for Game model.
    """
    if request.method == 'GET':
        return JsonResponse({
            'games': [
                game.as_dict() 
                for game in Game.objects.all()
            ]
        })
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        new_game = Game.objects.create(
            title=data['title'],
            description=data['description'],
            release_date=data['release_date'],
            platform=data['platform'],
        )
        return JsonResponse(new_game.as_dict(), status=201)
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        game = get_object_or_404(Game, pk=data['id'])
        game.title = data.get('title', game.title)
        game.description = data.get('description', game.description)
        game.release_date = data.get('release_date', game.release_date)
        game.platform = data.get('platform', game.platform)
        game.save()
        return JsonResponse(game.as_dict())
    
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        game = get_object_or_404(Game, pk=data['id'])
        game.delete()
        return JsonResponse({'message': 'Game deleted'}, status=204)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
