from json.decoder import JSONDecodeError
from rest_framework.views import APIView
from rest_framework.response import Response
from seguridad.models import historial, componentes, evidencias
from django.http import JsonResponse
import json

class Anomalia(APIView):
    def get(self, request, format = None):
        json_historial = list()
        for h in historial.objects.all():    
            json_evidencias = list()
            for e in evidencias.objects.filter(unHistorial_id=h.id):
                evidencia = {
                    "evidencia_id": e.id,
                    "hora": str(e.hora),
                    "foto": "e.ruta_foto"
                }
                json_evidencias.append(evidencia)
            anomalia = {
                "historial_id" : h.id,
                "componente_id": h.unComponente.id,
                "componente_nombre": h.unComponente.nombre,
                "tipo_historial": h.tipo,
                "evidencias": json_evidencias
            }
            json_historial.append(anomalia)
        return Response({"historial": json_historial})

    def post(self, request, format = None):
        json_data = json.loads(request.body)
        return Response({"mensaje": json_data})
