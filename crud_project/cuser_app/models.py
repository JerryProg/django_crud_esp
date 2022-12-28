from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.urls import reverse
from django.utils import timezone


#Manager for administrators (user admin) model:
class MyCustomManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Los usuarios deben tener email para poder registrarse')
        
        now = timezone.now()

        user = self.model(
            email = self.normalize_email(email),

            date_joined = now,
            last_login = now,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)

        return user


# Create your models here.
class CustomUser(AbstractBaseUser):
    """
    Este es el modelo personalizado de administrator, también se necesita de un manejador (manager) para
    poder ejecutarlo, dicho manager se debe localizar antes del modelo.
    """

    # Fields that contains the needed info of admin:
    email = models.EmailField("Email", max_length=100, unique=True)

    #For admin purposes:
    date_joined = models.DateTimeField("Fecha de ingreso", auto_now_add=True)
    last_login = models.DateTimeField("Ultimo acceso", null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        db_table = "custom_user"

    objects = MyCustomManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.id}, {self.email}" 

    def has_perm(self, perm, obj= None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'pk': self.pk})    

    @property
    def is_staff(self):
        return self.is_admin


# class UserInfo(models.Model):
#     user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     first_name = models.CharField("Nombre", max_length=100, null=True, blank=True)
#     last_name = models.CharField("Apellidos", max_length=100, null=True, blank=True)
#     birth_date = models.DateTimeField("Fecha de Nacimiento", null=True, blank=True)
#     phone_num = models.CharField("Telefono", max_length=20, null=True, blank=True)
#     address = models.CharField("Dirección", max_length=100, null=True, blank=True)
#     city = models.CharField("Ciudad", max_length=100, null=True, blank=True)
#     country = models.CharField("País", max_length=100, null=True, blank=True)
    
#     class Meta:
#         db_table = "user_info"

#     def get_absolute_url(self):
#         return reverse('user-info-detail', kwargs={'pk': self.pk})
