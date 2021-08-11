from django.urls import path
from seguridad import views

urlpatterns = [
    path('historial/', views.Anomalia.as_view()),
    path('componentes/', views.Componentes.as_view()),
]