from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from seguridad.views.seguridad import Login

schema_view = get_schema_view(
   openapi.Info(
      title="Documentacion ERP",
      default_version='v1',
      description="Documentacion backend ERP",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="maestradaz3@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [    
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('admin/', admin.site.urls),
   path('general/', include("general.urls")), 
   path('contabilidad/', include("contabilidad.urls")),
   path('cartera/', include("cartera.urls")),
   path('seguridad/', include("seguridad.urls")),
   path('vertical/', include("vertical.urls")),
   path('transporte/', include("transporte.urls")),
   path('contenedor/', include("contenedor.urls")),
   path('humano/', include("humano.urls")),   
   path('inventario/', include("inventario.urls")),
   path('ruteo/', include("ruteo.urls")),
   path('seguridad/login/', Login.as_view(), name='login'),
   path('seguridad/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('seguridad/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
] 
