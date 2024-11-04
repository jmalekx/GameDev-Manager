"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import developer_api_view, game_api_view, developer_detail_view, game_detail_view


urlpatterns = [
    #developer api endpoints
    path('developers/', developer_api_view, name='developer api'),
    path('developers/<int:developer_id>/', developer_detail_view, name='developer detail'),
    
    #game api endpoints
    path('games/', game_api_view, name='game api'),
    path('games/<int:game_id>/', game_detail_view, name='game detail'),
]
