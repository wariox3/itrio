from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from contenedor.models import ConsumoPeriodo, Consumo, UsuarioContenedor
from contenedor.serializers.consumo import ConsumoSerializador
from django.utils import timezone
from datetime import datetime
from django.db.models import Sum, Q, F

class ConsumoViewSet(viewsets.ModelViewSet):
    queryset = Consumo.objects.all()
    serializer_class = ConsumoSerializador    
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny], url_path=r'generar',)
    def generar(self, request):
        raw = request.data
        fechaParametro = raw.get('fecha')
        if fechaParametro:
            if not ConsumoPeriodo.objects.filter().exists():
                usuariosContenedors = UsuarioContenedor.objects.all()
                consumos = []
                for usuarioContenedor in usuariosContenedors:            
                    vrPlan = usuarioContenedor.contenedor.plan.precio
                    vrPlanDia = vrPlan / 30
                    consumo = Consumo(
                        #fecha = timezone.now().date(), 
                        fecha=fechaParametro,
                        contenedor_id=usuarioContenedor.contenedor_id,
                        contenedor=usuarioContenedor.contenedor.nombre,
                        usuarios=usuarioContenedor.contenedor.usuarios,
                        plan=usuarioContenedor.contenedor.plan,
                        usuario=usuarioContenedor.usuario,
                        vr_plan=vrPlanDia,
                        vr_usuario_adicional=0,
                        vr_total=vrPlanDia)
                    consumos.append(consumo)
                Consumo.objects.bulk_create(consumos)
                consumo_periodo = ConsumoPeriodo(fecha=fechaParametro)
                consumo_periodo.save()
                return Response({'proceso':True}, status=status.HTTP_200_OK)
            else: 
                return Response({'Mensaje': 'El periodo ya fue procesado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], url_path=r'consulta-empresa-fecha',)
    def consulta_empresa_fecha(self, request):
        raw = request.data
        empresa_id = raw.get('empresa_id')
        fechaDesde = raw.get('fechaDesde')
        fechaHasta = raw.get('fechaHasta')
        if fechaDesde and fechaHasta and empresa_id:
            fechaDesde = datetime.strptime(fechaDesde, "%Y-%m-%d")
            fechaHasta = datetime.strptime(fechaHasta, "%Y-%m-%d")
            consumos = Consumo.objects.filter(Q(fecha__gte=fechaDesde) & Q(fecha__lte=fechaHasta) & Q(empresa_id=empresa_id)).aggregate(
                vr_plan=Sum('vr_plan'),
                vr_total=Sum('vr_total')
                )
            consumosPlan = Consumo.objects.values('plan_id').filter(Q(fecha__gte=fechaDesde) & Q(fecha__lte=fechaHasta) & Q(empresa_id=empresa_id)).annotate(
                plan_nombre=F('plan__nombre'),
                vr_plan=Sum('vr_plan'),
                vr_total=Sum('vr_total')
                )
            return Response({'consumos':consumos, 'consumosPlan':consumosPlan}, status=status.HTTP_200_OK)
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)    
        
    @action(detail=False, methods=["post"], url_path=r'consulta-usuario-fecha',)
    def consulta_usuario_fecha(self, request):
        raw = request.data
        usuario_id = raw.get('usuario_id')
        fechaDesde = raw.get('fechaDesde')
        fechaHasta = raw.get('fechaHasta')
        if fechaDesde and fechaHasta and usuario_id:
            fechaDesde = datetime.strptime(fechaDesde, "%Y-%m-%d")
            fechaHasta = datetime.strptime(fechaHasta, "%Y-%m-%d")
            consumos = Consumo.objects.filter(Q(fecha__gte=fechaDesde) & Q(fecha__lte=fechaHasta) & Q(usuario_id=usuario_id)).aggregate(
            vr_plan=Sum('vr_plan'),
            vr_total=Sum('vr_total'))
            return Response({'consumos':consumos}, status=status.HTTP_200_OK)
        else:
            return Response({'Mensaje': 'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)            
