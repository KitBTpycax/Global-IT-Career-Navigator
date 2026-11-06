from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('career/<slug:slug>/', views.career_detail, name='career_detail'),
    path('career/<slug:slug>', views.career_detail),
    path('api/match/', views.api_match, name='api_match'),
    path('api/match', views.api_match),
    path('api/trends/', views.api_trends, name='api_trends'),
    path('api/trends', views.api_trends),
]
