import secrets
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from seguridad.models import User
from contenedor.models import Contenedor, UsuarioContenedor, CtnVerificacion
from contenedor.serializers.contenedor import ContenedorSerializador
from contenedor.serializers.usuario_contenedor import UsuarioContenedorSerializador, UsuarioContenedorListaSerializador, UsuarioContenedorConfiguracionSerializador
from contenedor.serializers.verificacion import CtnVerificacionSerializador
from contenedor.serializers.invitacion import CntInvitacionSerializador
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from contenedor.filters.usuario_contenedor import UsuarioContenedorFilter
from datetime import datetime, timedelta
from decouple import config
from utilidades.zinc import Zinc
from django.conf import settings
from rest_framework.pagination import PageNumberPagination

class UsuarioContenedorViewSet(viewsets.ModelViewSet):
    queryset = UsuarioContenedor.objects.all()
    serializer_class = UsuarioContenedorSerializador    
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = UsuarioContenedorFilter 
    serializadores = {
        'lista': UsuarioContenedorListaSerializador,
        'configuracion': UsuarioContenedorConfiguracionSerializador
    }

    def get_serializer_class(self):
        serializador_parametro = self.request.query_params.get('serializador', None)
        if not serializador_parametro or serializador_parametro not in self.serializadores:
            return UsuarioContenedorSerializador
        return self.serializadores[serializador_parametro]

    def get_queryset(self):
        page_size = self.request.query_params.get('page_size')
        if page_size:
            if page_size != '0':
                self.pagination_class = PageNumberPagination
                self.pagination_class.page_size = int(page_size)
        queryset = super().get_queryset()
        serializer_class = self.get_serializer_class()        
        select_related = getattr(serializer_class.Meta, 'select_related_fields', [])
        if select_related:
            queryset = queryset.select_related(*select_related)        
        campos = serializer_class.Meta.fields        
        if campos and campos != '__all__':
            queryset = queryset.only(*campos) 
        return queryset 
    
    def list(self, request, *args, **kwargs):
        if request.query_params.get('excel'):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        usuarioEmpresa = self.get_object()
        if usuarioEmpresa.rol == 'invitado':
            self.perform_destroy(usuarioEmpresa)
            empresa = Contenedor.objects.get(pk=usuarioEmpresa.contenedor_id)
            empresa.usuarios -= 1
            empresa.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'mensaje':"El usuario propietario no se puede eliminar", 'codigo': 22}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'invitar',)
    def invitar(self, request):        
        raw = request.data
        invitado = raw.get('invitado', None)
        contenedor_id = raw.get('contenedor_id', None)
        usuario_id = raw.get('usuario_id', None)
        aplicacion = raw.get('aplicacion', None)
        if invitado and contenedor_id and usuario_id and aplicacion:
            try:
                contenedor = Contenedor.objects.get(pk=contenedor_id)
            except Contenedor.DoesNotExist:
                return Response({'mensaje':'El contenedor no existe', 'codigo':8}, status=status.HTTP_400_BAD_REQUEST)                 
            try:
                usuario = User.objects.get(pk=usuario_id)
            except User.DoesNotExist:
                return Response({'mensaje':'El usuario no existe', 'codigo':8}, status=status.HTTP_400_BAD_REQUEST)
            
            usuario_invitado = User.objects.filter(username = invitado).first()
            if usuario_invitado:                
                if usuario_invitado.id == usuario.id:
                    return Response({'mensaje':'El usuario no se puede invitar a el mismo', 'codigo':18}, status=status.HTTP_400_BAD_REQUEST)
                
                if UsuarioContenedor.objects.filter(usuario_id=usuario_invitado.id, contenedor_id=contenedor.id).exists():
                    return Response({'mensaje':'El usuario ya esta invitado o confirmado para este contenedor', 'codigo':20}, status=status.HTTP_400_BAD_REQUEST)
            aplicaciones = settings.APLICACIONES
            if aplicacion in aplicaciones:
                '''if contenedor.plan:
                    if contenedor.plan.limite_usuarios > 0:
                        if contenedor.plan.limite_usuarios >= contenedor.usuarios:
                            return Response({'mensaje':'La empresa supera el numero de usuarios segun el plan, si quiere invitar nuevos usuarios debe incrementar el plan', 'codigo':20}, status=status.HTTP_400_BAD_REQUEST)'''
                aplicacion_datos = aplicaciones[aplicacion]
                token = secrets.token_urlsafe(20)
                data = {
                    'token': token,
                    'vence': datetime.now().date() + timedelta(days=1),
                    'contenedor_id': contenedor_id,
                    'usuario_invitado_username': invitado
                }
                serializador = CtnVerificacionSerializador(data = data)                
                if serializador.is_valid():                                                                 
                    serializador.save() 
                    data = {
                        'usuario': usuario_id,                    
                        'contenedor': contenedor_id,
                        'usuario_invitado': invitado
                    }
                    serializador_invitacion = CntInvitacionSerializador(data = data)                
                    if serializador_invitacion.is_valid():                                                                 
                        serializador_invitacion.save() 
                    url = f"https://app.{aplicacion_datos['dominio']}/auth/login/" + token
                    if config('ENV') == "test":
                        url = f"http://app.{aplicacion_datos['dominio_test']}/auth/login/" + token
                    if config('ENV') == "dev":
                        url = f"http://{aplicacion_datos['dominio_dev']}/auth/login/" + token                    
                    html_content = """
                                <h1>¡Hola {usuario}!</h1>
                                <p>Te han invitado para que seas parte de un equipo de trabajo en {aplicacion_nombre}. Clic en el siguiente enlace 
                                para aceptar la invitacion</p>
                                <a href='{url}' class='button'>Aceptar invitacion</a>
                                """.format(url=url, usuario=invitado, aplicacion_nombre=aplicacion_datos['nombre'])
                    correo = Zinc()  
                    correo.correo(invitado, f'Invitacion a {aplicacion_datos["nombre"]}', html_content, aplicacion)
                    return Response({'verificacion': serializador.data}, status=status.HTTP_201_CREATED)
                return Response({'mensaje':'Errores en el registro de la verificacion', 'codigo':3, 'validaciones': serializador.errors}, status=status.HTTP_400_BAD_REQUEST)                    
            else:
                return Response({'mensaje':'La aplicacion no existe', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                
        else:
            return Response({'mensaje':'Faltal parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                

    @action(detail=False, methods=["post"], url_path=r'confirmar',)
    def confirmar(self, request):
        usuarioSesion = request.user
        try:
            raw = request.data
            token = raw.get('token')
            verificacion = CtnVerificacion.objects.get(token=token)
            if verificacion.estado_usado == False:
                if User.objects.filter(username=verificacion.usuario_invitado_username).exists():
                    usuario = User.objects.get(username=verificacion.usuario_invitado_username)                
                    if not UsuarioContenedor.objects.filter(usuario_id=usuario.id, contenedor_id=verificacion.contenedor_id).exists():
                        if usuario.id == usuarioSesion.id:
                            data = {'usuario': usuario.id, 'contenedor': verificacion.contenedor_id, 'rol':'invitado'}
                            usuarioContenedorSerializador = UsuarioContenedorSerializador(data=data)            
                            if usuarioContenedorSerializador.is_valid():
                                usuarioContenedorSerializador.save()
                                verificacion.estado_usado = True
                                verificacion.save()
                                contenedor = Contenedor.objects.get(pk=verificacion.contenedor_id) 
                                contenedor.usuarios += 1
                                contenedor.save()
                                return Response({'confirmar': True}, status=status.HTTP_200_OK)
                            return Response({'mensaje':'Errores en el registro de la verificacion', 'codigo':19, 'validaciones': usuarioContenedorSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({'mensaje':"El usuario que ha iniciado sesión no corresponde al usuario invitado.", 'codigo': 21}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'mensaje':'El usuario ya está confirmado para esta empresa', 'codigo':20}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'mensaje':"El usuario invitado no existe", 'codigo': 15}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'mensaje':"El token ya fue usado", 'codigo': 6}, status=status.HTTP_400_BAD_REQUEST)
        except CtnVerificacion.DoesNotExist:
            return Response({'mensaje':"La verificacion no existe", 'codigo': 15}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["post"], url_path=r'validar',)
    def validar(self, request):
        raw = request.data
        usuario_id = raw.get('usuario')
        contenedor_id = raw.get('contenedor_id')
        if usuario_id and contenedor_id:            
            if UsuarioContenedor.objects.filter(usuario_id=usuario_id, contenedor_id=contenedor_id).exists():                
                contenedor = Contenedor.objects.get(pk=contenedor_id)
                contenedorSerializador = ContenedorSerializador(contenedor)
                return Response({'validar': True, 'empresa': contenedorSerializador.data}, status=status.HTTP_200_OK)                
            else:
                return Response({'validar': False}, status=status.HTTP_200_OK) 
        else:
            return Response({'mensaje':"Faltan parametros", 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)        