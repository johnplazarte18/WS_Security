from django.urls import path
from seguridad import views

urlpatterns = [
    path('historial-anomalias/', views.Anomalia.as_view()),
    path('componentes/', views.Componentes.as_view()),
    path('sistema/', views.Sistema.as_view()),
    path('solicitud/', views.Solicitud.as_view()),
]