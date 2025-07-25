from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    def _create_user(self, username, correo, nombre, apellido, numero_identificacion, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            correo = correo,
            nombre = nombre,
            apellido = apellido,
            numero_identificacion = numero_identificacion,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, correo, nombre, apellido, password=None, **extra_fields):
        return self._create_user(username, correo, nombre, apellido, password, False, False, **extra_fields)

    def create_superuser(self, username, correo, nombre, apellido, password=None, **extra_fields):
        return self._create_user(username, correo, nombre, apellido, password, True, True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.EmailField(max_length = 255, unique = True)
    correo = models.EmailField(max_length = 255, unique = True)
    nombre = models.CharField(max_length = 255, null = True)
    apellido = models.CharField(max_length = 255, null = True)
    nombre_corto = models.CharField(max_length = 255, null = True)
    numero_identificacion = models.CharField(max_length=20, null = True)
    cargo = models.CharField(max_length=255, null = True)
    telefono = models.CharField(max_length = 50, null = True)
    idioma = models.CharField(max_length = 2, default='es')
    imagen = models.TextField(null=True)
    vr_saldo = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    vr_credito = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    vr_abono = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    fecha_limite_pago = models.DateField(null=True)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    verificado = models.BooleanField(default = False)
    cortesia = models.BooleanField(default = False)
    es_socio = models.BooleanField(default = False)
    socio_id = models.IntegerField(null = True)
    fecha_creacion = models.DateTimeField(null=True, auto_now_add=True)
    dominio = models.CharField(max_length = 50, null = True)
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['correo','nombre','apellido']

    def __str__(self):
        return f'{self.nombre} {self.apellido}'   
        