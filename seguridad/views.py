from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.response import Response
from seguridad.models import historial, componentes, evidencias, solicitud
from usuario.models import usuarios
from django.db import transaction
from datetime import datetime
import json, base64

class Anomalia(APIView):

    # GET con parámetros 
    # http://127.0.0.1:8000/api-seguridad/historial-anomalias/?fecha_desde=2019-08-05&fecha_hasta=2021-08-05
    # GET sin parámetros
    # http://127.0.0.1:8000/api-seguridad/historial-anomalias/
    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                json_historial = list()
                if('fecha_desde' in request.GET and 'fecha_hasta' in request.GET):
                    fecha_desde = request.GET['fecha_desde']
                    fecha_hasta = request.GET['fecha_hasta']
                    for h in historial.objects.filter(fecha__range = [fecha_desde, fecha_hasta]):  
                        object_json = self.jsonHistorial(h)
                        if(object_json != None):
                            json_historial.append(object_json)
                        else:
                            raise Exception
                elif('historial_id' in request.GET):
                    unHistorial = historial.objects.get(id = request.GET['historial_id'])
                    object_json = self.jsonHistorial(unHistorial)
                    if(object_json != None):
                            json_historial.append(object_json)
                    else:
                        raise Exception
                else:
                    for h in historial.objects.all():    
                        object_json = self.jsonHistorial(h)
                        if(object_json != None):
                            json_historial.append(object_json)
                        else:
                            raise Exception
                return Response({"historial": json_historial})
            except historial.DoesNotExist:
                return Response({"mensaje": "No existe el historial."})
            except Exception as e:
                return Response({"mensaje": "Sucedió un error al obtener los datos, por favor intente nuevamente."})

    def jsonHistorial(self, historial):
        try:
            json_evidencias = list()
            for e in evidencias.objects.filter(unHistorial_id = historial.id):
                #encoded_string = "data:image/PNG;base64," + str(base64.b64encode(open(str(e.ruta_foto.url)[1:], "rb").read()))[2:][:-1]
                evidencia = {
                    "evidencia_id": e.id,
                    "hora": str(e.hora),
                    "foto": 'encoded_string'
                }
                json_evidencias.append(evidencia)
            un_historial = {
                "historial_id" : historial.id,
                "componente_id": historial.unComponente.id,
                "componente_nombre": historial.unComponente.nombre,
                "sector": historial.unComponente.sector,
                "fecha": str(historial.fecha),
                "tipo_historial": historial.tipo,
                "evidencias": json_evidencias
            }
            return un_historial
        except Exception as e:
            return None

    # http://127.0.0.1:8000/api-seguridad/historial-anomalias/
    def post(self, request, format = None):
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    json_data = json.loads(request.body.decode('utf-8'))
                    unHistorial = historial()
                    unComponente = componentes.objects.get(id = json_data['componente_id'])
                    unHistorial.unComponente = unComponente
                    unHistorial.fecha = json_data['fecha']
                    unHistorial.tipo = json_data['tipo_historial']
                    unHistorial.save()
                    if(json_data['tipo_historial'] == 'Solicitado'):
                        if('solicitud_id' in json_data):
                            unaSolicitud = solicitud.objects.get(id = json_data['solicitud_id'])
                            unaSolicitud.estado = True
                            unaSolicitud.historial_id = unHistorial.id
                            unaSolicitud.save() 
                    for e in range(len(json_data['evidencias'])):
                        unaEvidencia = evidencias()
                        unaEvidencia.unHistorial = unHistorial
                        unaEvidencia.hora = json_data['evidencias'][e]['hora']
                        image_b64 = json_data['evidencias'][e]['foto']
                        format, img_body = image_b64.split(";base64,")
                        extension = format.split("/")[-1]
                        hora = datetime.strptime(unaEvidencia.hora, '%H:%M:%S').hour
                        minutos = datetime.strptime(str(unaEvidencia.hora), '%H:%M:%S').minute
                        segundos = datetime.strptime(str(unaEvidencia.hora), '%H:%M:%S').second
                        img_file = ContentFile(base64.b64decode(img_body), name = "evidencia_f_" + str(unHistorial.fecha) + "-h-" + str(hora) + "-m-" + str(minutos) +"-s-" + str(segundos) + "." + extension)
                        unaEvidencia.ruta_foto = img_file
                        unaEvidencia.save()
                    return Response({"historial_id": unHistorial.id})
            except componentes.DoesNotExist:
                return Response({"mensaje": "No existe el componente."})
            except solicitud.DoesNotExist:
                return Response({"mensaje": "No existe la solicitud."})
            except Exception as e:
                return Response({"mensaje": "Sucedió un error al realizar la transacción, por favor intente nuevamente."})

class Componentes(APIView):

    # GET con parámetro id
    # http://127.0.0.1:8000/api-seguridad/componentes/?id=5
    # GET con parámetro nombre
    # http://127.0.0.1:8000/api-seguridad/componentes/?nombre=Cámara
    # GET sin parámetros
    # http://127.0.0.1:8000/api-seguridad/componentes/
    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                json_componente = list()
                if('id' in request.GET):
                    unComponente = componentes.objects.get(id = request.GET['id'])
                    json_componente.append(self.buildJsonCompo(unComponente))
                    return Response({"componente": json_componente})
                elif('nombre' in request.GET):
                    unComponente = componentes.objects.get(nombre = request.GET['nombre'])
                    json_componente.append(self.buildJsonCompo(unComponente))
                    return Response({"componente": json_componente})
                else:
                    for c in componentes.objects.all():
                        json_componente.append(self.buildJsonCompo(c))
                    return Response({"componente": json_componente})
            except componentes.DoesNotExist:
                return Response({"mensaje": "No existe el componente."}) 
            except Exception as e:  
                return Response({"mensaje": "Sucedió un error al obtener los datos, por favor intente nuevamente." + str(e)})
    
    def buildJsonCompo(self, componente):
        un_componente = {
            "componente_id": componente.id,
            "componente": componente.nombre,
            "sector": componente.sector,
            "estado": componente.estado
        }
        return un_componente

    # http://127.0.0.1:8000/api-seguridad/componentes/
    def put(self, request, format = None):
        if request.method == 'PUT':
            try:
                with transaction.atomic():
                    json_data = json.loads(request.body.decode('utf-8'))
                    unComponente = componentes.objects.get(id = json_data['componente_id'])
                    unComponente.estado = json_data['estado']
                    unComponente.save()
                    return Response({"mensaje": "True"})    
            except componentes.DoesNotExist:
                return Response({"mensaje": "False"})    
            except Exception as e: 
                return Response({"mensaje": "False"})
    
class Sistema(APIView):

    # http://127.0.0.1:8000/api-seguridad/sistema/
    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                with transaction.atomic():
                    estado_sistema = ''
                    all_components = len(componentes.objects.all())
                    components_habili = len(componentes.objects.filter(estado = False)) 
                    if(all_components == components_habili):
                        estado_sistema = 'Deshabilitado'
                    else:
                        estado_sistema = 'Habilitado'
                    return Response({"sistema": estado_sistema})    
            except Exception as e: 
                return Response({"mensaje": "Sucedió un error al realizar la transacción, por favor intente nuevamente."})
    
    # http://127.0.0.1:8000/api-seguridad/sistema/
    def put(self, request, format = None):
        if request.method == 'PUT':
            try:
                with transaction.atomic():
                    json_data = json.loads(request.body.decode('utf-8'))
                    for c in componentes.objects.all():
                        c.estado = json_data['estado']
                        c.save()
                    return Response({"mensaje": "True"})    
            except Exception as e: 
                return Response({"mensaje": "False"})
    
class Solicitud(APIView):
    
    # GET 1 (este es para la app móvil)
    # http://127.0.0.1:8000/api-seguridad/solicitud/?solicitud_id=4
    # GET 2 (este es para el arduino)
    # # http://127.0.0.1:8000/api-seguridad/solicitud/?estado=False
    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                with transaction.atomic():
                    json_solicitud = list()
                    if('solicitud_id' in request.GET):
                        solicitudes = solicitud.objects.get(id = request.GET['solicitud_id'])
                        json_solicitud.append(self.buildJsonSolici(solicitudes))
                        return Response({"solicitudes": json_solicitud})    
                    elif('estado' in request.GET):
                        solicitudes = solicitud.objects.filter(estado = request.GET['estado'])
                        for s in solicitudes:
                            json_solicitud.append(self.buildJsonSolici(s))
                        return Response({"solicitudes": json_solicitud})   
                    else:
                        solicitudes = solicitud.objects.all()
                        for s in solicitudes:
                            json_solicitud.append(self.buildJsonSolici(s))
                        return Response({"solicitudes": json_solicitud})  
            except solicitud.DoesNotExist:
                return Response({"mensaje": "No existen solicitudes."})
            except Exception as e: 
                return Response({"mensaje": "Sucedió un error al realizar la transacción, por favor intente nuevamente."})
    
    def buildJsonSolici(self, solicitud):
        una_solicitud = {
            "solicitud_id": solicitud.id,
            "usuario_id": solicitud.unUsuario.id,
            "historial_id": solicitud.historial_id,
            "estado": solicitud.estado
        }
        return una_solicitud

    # http://127.0.0.1:8000/api-seguridad/solicitud/
    def post(self, request, format = None):
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    json_data = json.loads(request.body.decode('utf-8'))
                    if('usuario_id' in json_data):
                        unaSolicitud = solicitud()
                        unUsuario = usuarios()
                        unUsuario.id = json_data['usuario_id']
                        unaSolicitud.unUsuario = unUsuario
                        unaSolicitud.estado = False
                        unaSolicitud.save()
                        return Response({"solicitud_id": unaSolicitud.id})    
                    else:
                        return Response({"mensaje": "False"})    
            except Exception as e: 
                return Response({"mensaje": "False"})