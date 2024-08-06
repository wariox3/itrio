from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.sessions.models import Session
from django.utils import timezone
from django_tenants.utils import tenant_context
from contenedor.serializers.sesion import CtnSessionSerializador


class CtnSessionView(APIView):
    def get(self, request, format=None):
        current_tenant = request.tenant
        with tenant_context(current_tenant):
            sessions = Session.objects.filter(expire_date__gt=timezone.now())
            serializer = CtnSessionSerializador(sessions, many=True)
            return Response(serializer.data)