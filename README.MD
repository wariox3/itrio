# Backend ERP - Itrio

API backend construida en Django + Django REST Framework, con arquitectura **multi-tenant** (`django-tenants`, un esquema de PostgreSQL por cliente/contenedor).

## Requisitos previos

- Python **3.10.12** (ver `runtime.txt`)
- PostgreSQL (obligatorio: `django_tenants.postgresql_backend` no funciona con SQLite ni otros motores)
- `pip` y `venv`

## 1. Clonar el repositorio

```sh
git clone <url-del-repositorio>
cd itrio
```

## 2. Crear y activar el entorno virtual

```sh
python3.10 -m venv ~/.venvs/itrio
source ~/.venvs/itrio/bin/activate
```

## 3. Instalar dependencias

```sh
pip install -r requirements.txt
```

## 4. Crear la base de datos

Crea una base de datos PostgreSQL vacía (el nombre debe coincidir con `DATABASE_NAME` del `.env`):

```sh
createdb bditrio
```

## 5. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto (mismo nivel que `manage.py`). Las variables se leen con `python-decouple` (ver `itrioapp/settings.py`):

```env
# Base de datos
DATABASE_USER='tu_usuario'
DATABASE_CLAVE='tu_clave'
DATABASE_HOST='localhost'
DATABASE_NAME='bditrio'
DATABASE_PORT='5432'

# Entorno
ENV='dev'
DOMINIO_BACKEND='localhost'
DOMINIO_FRONTEND='localhost'

# Sendgrid (correo)
KEY_SENDGRID='xyz'

# DigitalOcean Spaces (almacenamiento S3)
DO_CLAVE_ACCESO='xyz'
DO_CLAVE_SECRETA='xyz'
DO_REGION='xyz'
DO_BUCKET='xyz'

# Backblaze B2 (almacenamiento alternativo)
B2_APP_KEY_ID='xyz'
B2_APP_KEY='xyz'
B2_BUCKET_NAME='xyz'
B2_REGION='xyz'

# Cloudflare Turnstile (captcha) por proyecto
CF_TURNSTILE_SECRET_KEY_REDDOC='xyz'
CF_TURNSTILE_SECRET_KEY_RUTEO='xyz'
CF_TURNSTILE_SECRET_KEY_POS='xyz'

# Google Maps
GOOGLE_MAPS_API_KEY='xyz'

# Pasarela de pago Wompi
WOMPI_SECRETO_INTEGRIDAD='xyz'

# Facturación electrónica (contenedor de pruebas)
FACTURACION_CONTENEDOR='demo'
FACTURACION_USUARIO='tu_correo@ejemplo.com'
FACTURACION_CLAVE='xyz'

AUT_INTERNA=
```

> Las claves reales (Sendgrid, DigitalOcean, Backblaze, Google Maps, Wompi, etc.) las entrega el equipo por un canal seguro — **nunca las subas al repositorio**, `.env` ya está en `.gitignore`.

## 6. Migrar la base de datos (multi-tenant)

Este proyecto usa `django-tenants`, así que las migraciones se corren en dos pasos: primero el esquema compartido (`SHARED_APPS`), luego los esquemas de cada tenant (`TENANT_APPS`):

```sh
python manage.py migrate_schemas --shared
```

Crea el tenant público (esquema `public`) y su dominio, por ejemplo desde el shell de Django:

```sh
python manage.py shell
```

```python
from contenedor.models import Contenedor, Dominio

tenant = Contenedor(schema_name='public', nombre='Público')
tenant.save()

Dominio.objects.create(domain='localhost', tenant=tenant, is_primary=True)
```

Luego migra los esquemas de los tenants:

```sh
python manage.py migrate_schemas
```

## 7. Crear un superusuario

```sh
python manage.py createsuperuser
```

## 8. Levantar el servidor de desarrollo

```sh
python manage.py runserver
```

La API quedará disponible en `http://localhost:8000/`. La documentación interactiva (drf-yasg) suele estar en `/swagger/` o `/redoc/` (ver `itrioapp/urls.py`).

## Notas adicionales

- **VS Code**: `.vscode/settings.json` ya apunta el intérprete al venv (`~/.venvs/itrio/bin/python`); ajusta la ruta si usas otro nombre de entorno.
- **Apps compartidas vs. por tenant**: `contenedor`, `seguridad` y `vertical` viven en el esquema `public` (`SHARED_APPS`); `general`, `contabilidad`, `cartera`, `transporte`, `humano`, `inventario`, `crm` y `ruteo` se replican por cada tenant (`TENANT_APPS`).
- **Autenticación**: JWT vía `djangorestframework-simplejwt`.
- **Zona horaria**: `America/Bogota`.
