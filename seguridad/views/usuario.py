import secrets
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from seguridad.models import User
from contenedor.models import CtnVerificacion
from contenedor.models import CtnInformacionFacturacion
from seguridad.serializers import UserSerializer, UserUpdateSerializer
from contenedor.serializers.verificacion import CtnVerificacionSerializador
from contenedor.serializers.informacion_facturacion import CtnInformacionFacturacionSerializador
from datetime import datetime, timedelta
from utilidades.zinc import Zinc
from decouple import config
from utilidades.space_do import SpaceDo

class UsuarioViewSet(GenericViewSet, UpdateModelMixin):
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def list(self, request):        
        queryset = User.objects.all()
        serializer_class = UserSerializer(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        raw = request.data
        user_serializer = self.serializer_class(data=raw)
        if user_serializer.is_valid():
            usuario = user_serializer.save()
            token = secrets.token_urlsafe(20)                           
            raw["usuario_id"] = usuario.id
            raw["token"] = token
            raw["vence"] = datetime.now().date() + timedelta(days=1)             
            verificacion_serializer = CtnVerificacionSerializador(data = raw)
            if verificacion_serializer.is_valid():                                             
                verificacion_serializer.save()
                dominio = config('DOMINIO_FRONTEND')                
                url = 'https://' + dominio + '/auth/verificacion/' + token
                html_content = """
                                <h1>¡Hola {usuario}!</h1>
                                <p>Estamos comprometidos con la seguridad de tu cuenta, por esta razón necesitamos que nos valides 
                                que eres tú, por favor verifica tu cuenta haciendo clic en el siguiente enlace.</p>
                                <a href='{url}' class='button'>Verificar cuenta</a>
                                """.format(url=url, usuario=usuario.nombre_corto)
                correo = Zinc()  
                correo.correo_reddoc(usuario.correo, 'Verificar cuenta de RedDoc', html_content)  
                return Response({'usuario': user_serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'mensaje':'Errores en el registro de la verificacion', 'codigo':3, 'validaciones': verificacion_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'mensaje':'Errores en el registro del usuario', 'codigo':2, 'validaciones': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = self.serializer_class(user)
        return Response(user_serializer.data)

    def update(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = UserUpdateSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'actualizacion': True, 'usuario': user_serializer.data}, status=status.HTTP_201_CREATED)            
        return Response({'mensaje':'Errores en la actualizacion del usuario', 'codigo':10, 'validaciones': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'verificar',)
    def verificar(self, request):
        tokenUrl = request.data.get('token')
        if tokenUrl:
            verificacion = CtnVerificacion.objects.filter(token=tokenUrl).first()
            if verificacion:
                if verificacion.estado_usado == False:
                    fechaActual = datetime.now().date()                
                    if fechaActual <= verificacion.vence:
                        verificacion.estado_usado = True
                        verificacion.save()
                        usuario = User.objects.get(id = verificacion.usuario_id)
                        usuario.verificado = True
                        usuario.save()
                        verificacionSerializer = CtnVerificacionSerializador(verificacion)                
                        return Response({'verificado': True, 'verificacion': verificacionSerializer.data}, status=status.HTTP_200_OK)
                    return Response({'mensaje':'El token de la verificacion esta vencido', 'codigo': 6, 'codigoUsuario': verificacion.usuario_id}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'mensaje':'La verificacion ya fue usada', 'codigo': 5, 'codigoUsuario': verificacion.usuario_id}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'mensaje':'No se ha encontrado la verificacion', 'codigo': 4}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'mensaje':'Faltan parametros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], url_path=r'cambio-clave-solicitar',)
    def cambio_clave_solicitar(self, request):
        try:
            raw = request.data            
            username = raw.get('username')
            if username:
                usuario = User.objects.get(username = username)
                token = secrets.token_urlsafe(20)            
                raw["token"] = token
                raw["vence"] = datetime.now().date() + timedelta(days=1)                                    
                raw["usuario_id"] = usuario.id
                raw["accion"] = "clave"
                verificacion_serializer = CtnVerificacionSerializador(data = raw)
                if verificacion_serializer.is_valid():                                             
                    verificacion_serializer.save()
                    dominio = config('DOMINIO_FRONTEND')                
                    url = 'https://' + dominio + '/auth/clave/cambiar/' + token
                    html_content = """
                                    <h1>¡Hola {usuario}!</h1>
                                    <p>Recibimos una solicitud para cambiar tu clave, puedes cambiarla haciendo clic en 
                                    el siguiente enlace.</p>
                                    <a href='{url}' class='button'>Cambiar clave</a>
                                    """.format(url=url, usuario=usuario.nombre_corto)
                    correo = Zinc()  
                    correo.correo_reddoc(usuario.correo, 'Solicitud cambio clave RedDoc', html_content)
                    return Response({'verificacion': verificacion_serializer.data}, status=status.HTTP_201_CREATED)
                return Response({'mensaje':'Errores en el registro de la verificacion', 'codigo':3, 'validaciones': verificacion_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)            
        except User.DoesNotExist:
            return Response({'mensaje':'El usuario no existe', 'codigo':8}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=["post"], url_path=r'cambio-clave-verificar',)
    def cambio_clave_verificar(self, request):
        raw = request.data
        try:
            token = raw.get('token')
            clave = raw.get('password')
            if token and clave:
                verificacion = CtnVerificacion.objects.filter(token=token).first()
                if verificacion:
                    if verificacion.estado_usado == False:
                        fechaActual = datetime.now().date()                
                        if fechaActual <= verificacion.vence:
                            usuario = User.objects.get(pk=verificacion.usuario_id)
                            verificacion.estado_usado = True
                            verificacion.save()
                            usuario.set_password(clave)
                            usuario.save()
                            return Response({'cambio': True}, status=status.HTTP_200_OK)
                        return Response({'mensaje':'El token de la verificacion esta vencido', 'codigo': 6, 'codigoUsuario': verificacion.usuario_id}, status=status.HTTP_400_BAD_REQUEST)
                    return Response({'mensaje':'La verificacion ya fue usada', 'codigo': 5, 'codigoUsuario': verificacion.usuario_id}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'mensaje':'No se ha encontrado la verificacion', 'codigo': 4}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'mensaje':'Faltan parametros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)                
        except User.DoesNotExist:
            return Response({'mensaje':'El usuario no existe', 'codigo':8}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'cambio-clave',)
    def cambio_clave(self, request):
        raw = request.data
        try:
            usuario_id = raw.get('usuario_id')
            clave = raw.get('password')
            if usuario_id and clave:                            
                usuario = User.objects.get(pk=usuario_id)
                usuario.set_password(clave)
                usuario.save()
                return Response({'cambio': True}, status=status.HTTP_200_OK)                
            return Response({'mensaje':'Faltan parametros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)                
        except User.DoesNotExist:
            return Response({'mensaje':'El usuario no existe', 'codigo':8}, status=status.HTTP_400_BAD_REQUEST)       

    @action(detail=False, methods=["post"], url_path=r'cargar-imagen',)
    def cargar_imagen(self, request):
        try:
            raw = request.data
            usuario_id = raw.get('usuario_id')
            imagenB64 = raw.get('imagenB64')
            if usuario_id and imagenB64:
                usuario = User.objects.get(pk=usuario_id)
                arrDatosB64 = imagenB64.split(",")
                base64Crudo = arrDatosB64[1]
                arrTipo = arrDatosB64[0].split(";")
                arrData = arrTipo[0].split(":")
                contentType = arrData[1]
                archivo = f"itrio/{config('ENV')}/usuario/imagen_{usuario_id}.jpg"
                spaceDo = SpaceDo()
                spaceDo.putB64(archivo, base64Crudo, contentType)
                usuario.imagen = archivo
                usuario.save()
                return Response({'cargar':True, 'imagen':f"https://{config('DO_BUCKET')}.{config('DO_REGION')}.digitaloceanspaces.com/{archivo}"}, status=status.HTTP_200_OK)                  
            else: 
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'mensaje':'El usuario no existe', 'codigo':15}, status=status.HTTP_404_NOT_FOUND)  

    @action(detail=False, methods=["post"], url_path=r'limpiar-imagen',)
    def limpiar_imagen(self, request):
        try:
            raw = request.data
            usuario_id = raw.get('usuario_id')    
            if usuario_id:
                usuario = User.objects.get(pk=usuario_id)                
                spaceDo = SpaceDo()
                spaceDo.eliminar(usuario.imagen)
                usuario.imagen = f"itrio/usuario_defecto.jpg"
                usuario.save()
                return Response({'limpiar':True, 'imagen':f"https://{config('DO_BUCKET')}.{config('DO_REGION')}.digitaloceanspaces.com/{usuario.imagen}"}, status=status.HTTP_200_OK)                  
            else: 
                return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'mensaje':'El usuario no existe', 'codigo':15}, status=status.HTTP_404_NOT_FOUND)  

    @action(detail=False, methods=["get"], url_path=r'saldo/(?P<id>\d+)')
    def saldo(self, request, id=None):        
        usuario = User.objects.get(id=id)
        if usuario:
            return Response({'saldo': usuario.vr_saldo, 'credito': usuario.vr_credito}, status=status.HTTP_200_OK)
        return Response({'mensaje':'El usuario no existe', 'codigo': 4}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], url_path=r'estado-verificado',)
    def estado_verificado(self, request):
        raw = request.data
        try:
            usuario_id = raw.get('usuario_id')
            if usuario_id:                            
                usuario = User.objects.get(pk=usuario_id)
                return Response({'verificado': usuario.verificado}, status=status.HTTP_200_OK)                
            return Response({'mensaje':'Faltan parametros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)                
        except User.DoesNotExist:
            return Response({'mensaje':'El usuario no existe', 'codigo':8}, status=status.HTTP_400_BAD_REQUEST)   

    @action(detail=False, methods=["post"], url_path=r'lista-socio')
    def lista_socio(self, request):        
        raw = request.data
        socio_id = raw.get('socio_id')  
        if socio_id:
            usuarios = User.objects.filter(socio_id=socio_id)
            usuariosSerializer = UserSerializer(usuarios, many=True)                
            return Response({'usuarios': usuariosSerializer.data}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Faltan parametros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)      

    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny], url_path=r'detalle/(?P<id>\d+)')
    def detalle(self, request, id=None):        
        usuario = User.objects.get(id=id)
        if usuario:
            usuarioSerializador = UserSerializer(usuario)
            informacionesFacturaciones = CtnInformacionFacturacion.objects.filter(usuario_id=id)
            informacionesFacturacionesSerializador = CtnInformacionFacturacionSerializador(informacionesFacturaciones, many=True)
            return Response({
                'usuario': usuarioSerializador.data, 
                'informaciones_facturaciones': informacionesFacturacionesSerializador.data}, status=status.HTTP_200_OK)
        return Response({'mensaje':'El usuario no existe', 'codigo': 4}, status=status.HTTP_400_BAD_REQUEST)          

        