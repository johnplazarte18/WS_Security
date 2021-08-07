from typing import FrozenSet
from django.http import response
from rest_framework.views import APIView
from rest_framework.response import Response

class Anomalia(APIView):
    def get(self, request, format=None):
        return Response({"mensaje": "holaa get"})
    def post(self, request, format=None):
        return Response({"mensaje": "holaa post"})
