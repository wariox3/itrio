from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from contenedor.models import CtnConsumoPeriodo, CtnConsumo, UsuarioContenedor, CtnMovimiento
from contenedor.serializers.consumo import CtnSerializador
from seguridad.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum, Q, F, Count
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
                    if usuario_contenedor.contenedor.plan_id >= 9 and usuario_contenedor.contenedor.plan_id <= 11:
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
                fecha__range=(fechaDesde,fechaHasta), usuario_id=usuario_id, cortesia=False
                ).values(
                    'usuario_id', 'contenedor_id', 'contenedor', 'subdominio', 'plan_id', 'plan__nombre', 'plan__precio'
                ).annotate(
                    vr_total=Sum('vr_total'),
                    dias=Count('id')
                )
            total_consumo = sum(item['vr_total'] for item in consumos) if consumos else 0
            total_consumo_redondeado = round(total_consumo, 0)
            plan_precio = sum(item['plan__precio'] for item in consumos) if consumos else 0
            plan_precio = round(plan_precio, 0)            
            return Response({'consumos':consumos, 'total_consumo': total_consumo_redondeado, 'plan_precio': plan_precio}, status=status.HTTP_200_OK)
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny], url_path=r'resumen',)
    def resumen_action(self, request):
        raw = request.data
        fecha_desde = raw.get('fecha_desde')
        fecha_hasta = raw.get('fecha_hasta')        
        if fecha_desde and fecha_hasta:
            query = f'''            
                select
                    ct.id,
                    ct.nombre,
                    ct.numero_identificacion,
                    ct.fecha,
                    ct.usuarios,
                    ct.plan_id,
                    p.nombre as plan_nombre,
                    p.precio as plan_precio,
                    ct.reddoc,
                    ct.ruteo,
                    ct.usuario_id,
                    u.username as usuario_username,                   
                    ct.fecha_ultima_conexion,
                    ct.cortesia,
                    ct.precio,
                    (	select
                            coalesce(SUM(c.vr_total), 0)
                        from
                            cnt_consumo c
                        where
                            c.contenedor_id = ct.id and c.fecha >= '{fecha_desde}' and fecha <= '{fecha_hasta}' and cortesia=false) as vr_consumo
                from
                    cnt_contenedor ct
                    left join seguridad_user u on ct.usuario_id = u.id
                    left join cnt_plan p on ct.plan_id = p.id 
                order by ct.id
            '''
            resultados = CtnConsumo.objects.raw(query) 
            consumos = []
            for item in resultados:
                consumos.append({
                    'id': item.id,
                    'nombre': item.nombre,
                    'numero_identificacion': item.numero_identificacion,
                    'fecha': item.fecha,
                    'usuarios': item.usuarios,
                    'plan_id': item.plan_id,
                    'plan_nombre': item.plan_nombre,
                    'plan_precio': item.plan_precio,
                    'reddoc': item.reddoc,
                    'ruteo': item.ruteo,
                    'usuario_id': item.usuario_id,
                    'usuario_username': item.usuario_username,
                    'fecha_ultima_conexion': item.fecha_ultima_conexion,
                    'cortesia': item.cortesia,
                    'precio': item.precio,
                    'vr_consumo': item.vr_consumo  # Campo calculado
                })                       
            return Response({'consumos':consumos}, status=status.HTTP_200_OK)
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                    
