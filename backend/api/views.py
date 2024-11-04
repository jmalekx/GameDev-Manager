from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Developer, Game, GameDeveloper
from django.views.decorators.csrf import csrf_exempt
import json

#implementing DRY method
def update_instance(instance, data):
    """Update model instance with provided data."""
    for attr, value in data.items():
        if hasattr(instance, attr):
            setattr(instance, attr, value)
    instance.save()
    return instance

def delete_instance(instance):
    """Delete model instance."""
    instance.delete()

@csrf_exempt
def developer_api_view(request):
    """Handle API requests for Developer model"""
    if request.method == 'GET':
        return JsonResponse({
            'developers': [developer.as_dict() for developer in Developer.objects.all()]
        })
    
    elif request.method == 'POST':
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
        data = json.loads(request.body)
        developer = get_object_or_404(Developer, pk=data.get('id'))
        updated_developer = update_instance(developer, data)
        return JsonResponse(updated_developer.as_dict())
    
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        developer = get_object_or_404(Developer, pk=data['id'])
        delete_instance(developer)
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
        updated_developer = update_instance(developer, data)
        return JsonResponse(updated_developer.as_dict())

    elif request.method == 'DELETE':
        developer.delete()
        return JsonResponse({'message': 'Developer deleted successfully'}, status=204)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def game_api_view(request):
    """Handle API requests for Game model."""
    if request.method == 'GET':
        return JsonResponse({
            'games': [game.as_dict() for game in Game.objects.all()]
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
        updated_game = update_instance(game, data)
        return JsonResponse(updated_game.as_dict())
    
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        game = get_object_or_404(Game, pk=data['id'])
        delete_instance(game)
        return JsonResponse({'message': 'Game deleted'}, status=204)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def game_detail_view(request, game_id):
    """Handle API requests for a specific Game."""
    game = get_object_or_404(Game, id=game_id)

    if request.method == 'GET':
        return JsonResponse(game.as_dict())

    elif request.method == 'PUT':
        data = json.loads(request.body)
        updated_game = update_instance(game, data)

        if 'developers' in data:
            game.gamedeveloper_set.all().delete()  # Clear existing developers
            for dev in data['developers']:
                GameDeveloper.objects.create(
                    game=game,
                    developer_id=dev['developer_id'],  # Ensure this matches the structure
                    role=dev['role']
                )

        return JsonResponse(updated_game.as_dict())

    elif request.method == 'DELETE':
        game.delete()
        return JsonResponse({'message': 'Game deleted successfully'}, status=204)

    return JsonResponse({'error': 'Method not allowed'}, status=405)