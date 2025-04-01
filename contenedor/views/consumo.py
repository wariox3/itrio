from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from contenedor.models import CtnConsumoPeriodo, CtnConsumo, UsuarioContenedor, CtnMovimiento
from contenedor.serializers.consumo import CtnSerializador
from seguridad.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum, Q, F
import calendar

class ConsumoViewSet(viewsets.ModelViewSet):
    queryset = CtnConsumo.objects.all()
    serializer_class = CtnSerializador    
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny], url_path=r'generar',)
    def generar(self, request):
        raw = request.data
        fecha_parametro = raw.get('fecha')
        if fecha_parametro:            
            fecha_obj = datetime.strptime(fecha_parametro, '%Y-%m-%d').date()            
            anio, mes = fecha_obj.year, fecha_obj.month            
            cantidad_dias = calendar.monthrange(anio, mes)[1]
            if not CtnConsumoPeriodo.objects.filter(fecha=fecha_parametro).exists():
                usuarios_contenedores = UsuarioContenedor.objects.filter(rol='propietario')
                consumos = []
                for usuario_contenedor in usuarios_contenedores:      
                    if usuario_contenedor.contenedor.plan_id == 9:
                        vrPlan = usuario_contenedor.contenedor.precio
                    else:
                        vrPlan = usuario_contenedor.contenedor.plan.precio
                    vrPlanDia = vrPlan / cantidad_dias
                    consumo = CtnConsumo(                        
                        fecha=fecha_parametro,
                        contenedor_id=usuario_contenedor.contenedor_id,
                        contenedor=usuario_contenedor.contenedor.nombre,
                        subdominio=usuario_contenedor.contenedor.schema_name,
                        usuarios=usuario_contenedor.contenedor.usuarios,
                        plan=usuario_contenedor.contenedor.plan,
                        usuario=usuario_contenedor.usuario,
                        vr_plan=vrPlanDia,
                        vr_usuario_adicional=0,
                        vr_total=vrPlanDia,
                        cortesia=usuario_contenedor.contenedor.cortesia)
                    consumos.append(consumo)
                CtnConsumo.objects.bulk_create(consumos)
                consumo_periodo = CtnConsumoPeriodo(fecha=fecha_parametro)
                consumo_periodo.save()
                return Response({'proceso':True}, status=status.HTTP_200_OK)
            else: 
                return Response({'Mensaje': 'El periodo ya fue procesado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny], url_path=r'consulta-empresa-fecha',)
    def consulta_empresa_fecha(self, request):
        raw = request.data
        empresa_id = raw.get('empresa_id')
        fechaDesde = raw.get('fechaDesde')
        fechaHasta = raw.get('fechaHasta')
        if fechaDesde and fechaHasta and empresa_id:
            fechaDesde = datetime.strptime(fechaDesde, "%Y-%m-%d")
            fechaHasta = datetime.strptime(fechaHasta, "%Y-%m-%d")
            consumos = CtnConsumo.objects.filter(Q(fecha__gte=fechaDesde) & Q(fecha__lte=fechaHasta) & Q(empresa_id=empresa_id)).aggregate(
                vr_plan=Sum('vr_plan'),
                vr_total=Sum('vr_total')
                )
            consumosPlan = CtnConsumo.objects.values('plan_id').filter(Q(fecha__gte=fechaDesde) & Q(fecha__lte=fechaHasta) & Q(empresa_id=empresa_id)).annotate(
                plan_nombre=F('plan__nombre'),
                vr_plan=Sum('vr_plan'),
                vr_total=Sum('vr_total')
                )
            return Response({'consumos':consumos, 'consumosPlan':consumosPlan}, status=status.HTTP_200_OK)
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny], url_path=r'consulta-usuario-fecha',)
    def consulta_usuario_fecha(self, request):
        raw = request.data
        usuario_id = raw.get('usuario_id')
        fechaDesde = raw.get('fechaDesde')
        fechaHasta = raw.get('fechaHasta')
        if fechaDesde and fechaHasta and usuario_id:
            fechaDesde = datetime.strptime(fechaDesde, "%Y-%m-%d")
            fechaHasta = datetime.strptime(fechaHasta, "%Y-%m-%d")
            consumos = CtnConsumo.objects.filter(
                fecha__range=(fechaDesde,fechaHasta), usuario_id=usuario_id
                ).values(
                    'usuario_id', 'contenedor_id', 'contenedor', 'subdominio', 'plan_id', 'plan__nombre'
                ).annotate(
                    vr_total=Sum('vr_total')
                )
            return Response({'consumos':consumos}, status=status.HTTP_200_OK)
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)            
