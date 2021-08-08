from rest_framework.views import APIView
from rest_framework.response import Response
from seguridad.models import historial, componentes, evidencias
from django.db import transaction
import json

class Anomalia(APIView):
    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                json_historial = list()
                for h in historial.objects.all():    
                    json_evidencias = list()
                    for e in evidencias.objects.filter(unHistorial_id=h.id):
                        # aquí obtener la img y codificarla a binario
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
            except:
                return Response({"mensaje": "Sucedió un error al obtener los datos, por favor intente nuevamente"})
    def post(self, request, format = None):
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    json_data = json.loads(request.body)
                    unHistorial = historial()
                    unComponente = componentes()
                    unComponente.id = json_data[0]['historial']['componente_id']
                    unHistorial.unComponente = unComponente
                    unHistorial.fecha = json_data[0]['historial']['fecha']
                    unHistorial.tipo = json_data[0]['historial']['tipo']
                    unHistorial.save()
                    for e in range(len(json_data[0]['evidencias'])):
                        unaEvidencia = evidencias()
                        unaEvidencia.unHistorial = unHistorial
                        unaEvidencia.hora = json_data[0]['evidencias'][e]['hora']
                        unaEvidencia.ruta_foto = json_data[0]['evidencias'][e]['foto']
                        unaEvidencia.save()
                    return Response({"mensaje": "Transacción efectuada correctamente"})
            except Exception as e:
                return Response({"mensaje": e})
                #return Response({"mensaje": "Sucedió un error al realizar la transacción, por favor intente nuevamente"})
