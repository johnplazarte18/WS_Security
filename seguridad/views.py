from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.response import Response
from seguridad.models import historial, componentes, evidencias
from django.db import transaction
from datetime import datetime
import json, base64

class Anomalia(APIView):
    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                json_historial = list()
                for h in historial.objects.all():    
                    json_evidencias = list()
                    for e in evidencias.objects.filter(unHistorial_id=h.id):
                        encoded_string = base64.b64encode(open(str(e.ruta_foto.url)[1:], "rb").read())                        
                        encoded_string = "data:image/jpeg;base64," + str(encoded_string)[2:][:-1]
                        evidencia = {
                            "evidencia_id": e.id,
                            "hora": str(e.hora),
                            "foto": str(encoded_string)
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
            except Exception as e:
                return Response({"mensaje": "Sucedió un error al obtener los datos, por favor intente nuevamente " + str(e)})

    def post(self, request, format = None):
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    json_data = json.loads(request.body.decode('utf-8'))
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
                        image_b64 = json_data[0]['evidencias'][e]['foto']
                        format, img_body = image_b64.split(";base64,")
                        extension = format.split("/")[-1]
                        hora = datetime.strptime(unaEvidencia.hora, '%H:%M:%S').hour
                        minutos = datetime.strptime(str(unaEvidencia.hora), '%H:%M:%S').minute
                        segundos = datetime.strptime(str(unaEvidencia.hora), '%H:%M:%S').second
                        img_file = ContentFile(base64.b64decode(img_body), name = "evidencia_h_" + str(hora) + "_m_" + str(minutos) +"_s_" + str(segundos) + "." + extension)
                        unaEvidencia.ruta_foto = img_file
                        unaEvidencia.save()
                    return Response({"mensaje": "La transacción fue realizada correctamente"})
            except Exception as e:
                return Response({"mensaje": "Sucedió un error al realizar la transacción, por favor intente nuevamente."})

class Componentes(APIView):
    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                return Response({"componentes": list(componentes.objects.all().values())})
            except Exception as e:
                return Response({"mensaje": "Sucedió un error al obtener los datos, por favor intente nuevamente."})
    
    def post(self, request, format = None):
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    json_data = json.loads(request.body.decode('utf-8'))
                    unComponente = componentes.objects.get(id=int(json_data[0]['componente']['componente_id']))
                    unComponente.estado = json_data[0]['componente']['estado']
                    unComponente.save()
                    return Response({"mensaje": "La transacción fue realizada correctamente"})    
            except Exception as e: 
                return Response({"mensaje": "Sucedió un error al realizar la transacción, por favor intente nuevamente."})
