from django.urls import path
from usuario import views

urlpatterns = [
    path('usuario/', views.Usuario.as_view()),
    path('login/', views.Login.as_view()),
]