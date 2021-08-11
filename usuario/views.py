from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.response import Response
from usuario.models import usuarios
from django.db import transaction
import json, base64, os

class Usuario(APIView):

    def get(self, request, format = None):
        if request.method == 'GET':
            try:
                if('id' in request.GET):
                    return Response({"usuario": list(usuarios.objects.filter(id = request.GET['id']).values())})
                elif('usuario' in request.GET):
                    return Response({"usuario": list(usuarios.objects.filter(usuario = request.GET['usuario']).values())})
                else:
                    return Response({"usuario": list(usuarios.objects.all().values())})
            except Exception as e:  
                return Response({"mensaje": "Sucedió un error al obtener los datos, por favor intente nuevamente."})
    
    def post(self, request, format = None):
        if request.method == 'POST':
            try:
                with transaction.atomic():
                    json_data = json.loads(request.body.decode('utf-8'))
                    # Cambia el estado del usuario
                    if('usuario_id' in json_data and 'estado' in json_data):
                        unUsuario = usuarios.objects.get(id = json_data['usuario_id'])
                        if(unUsuario != None):
                            unUsuario.save()
                        else:
                            raise Exception
                    # Modificar un usuario  
                    elif('usuario_id' in json_data):
                        unUsuario = usuarios.objects.get(id = json_data['usuario_id'])
                        unUsuario = self.buildUsuario(unUsuario, json_data)
                        if(unUsuario != None):
                            unUsuario.save()
                        else:
                            raise Exception
                    else:
                        # Registrar un usuario
                        unUsuario = usuarios()
                        unUsuario = self.buildUsuario(unUsuario, json_data)
                        if(unUsuario != None):
                            unUsuario.save()
                        else:
                            raise Exception
                return Response({"mensaje": "La transacción fue realizada correctamente"})  
            except Exception as e: 
                return Response({"mensaje": "Sucedió un error al realizar la transacción, por favor intente nuevamente."})

    def buildUsuario(self, unUsuario, json_data):
        try:
            if('nombre' in json_data):
                unUsuario.nombre = json_data['nombre']
            if('rol' in json_data):
                unUsuario.rol = json_data['rol']
            if('usuario' in json_data):
                unUsuario.usuario = json_data['usuario']
            if('clave' in json_data):
                unUsuario.clave = json_data['clave']
            if ('estado' in json_data):
                unUsuario.estado = json_data['estado']
            else:
                unUsuario.estado = True
            if('foto' in json_data):
                imgBorrar = unUsuario.ruta_foto.url
                image_b64 = json_data['foto']
                format, img_body = image_b64.split(";base64,")
                extension = format.split("/")[-1]
                img_file = ContentFile(base64.b64decode(img_body), name = "usuario_" + unUsuario.usuario + "." + extension)
                unUsuario.ruta_foto = img_file
                os.remove(imgBorrar)
            return unUsuario
        except Exception as e: 
            return None

class autenticacion(APIView):

    def post(self, request, format = None):
        if request.method == 'POST':
            try:
                json_data = json.loads(request.body.decode('utf-8'))
                return Response({"usuario": ""})
            except Exception as e:  
                return Response({"mensaje": "Sucedió un error al obtener los datos, por favor intente nuevamente."})
    
    
