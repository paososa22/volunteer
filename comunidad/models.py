from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class ExtendedData(models.Model):
    TYPE_CHOICES = [("V","Voluntario"),("R","Representante")]
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    user_type = models.CharField(max_length=1,choices=TYPE_CHOICES,blank=False,null=False)

class PreferredLanguage(models.Model):
    LANGUAGE_CHOICES = [
        ('es', 'Español'),
        ('en', 'Inglés'),
        ('fr', 'Francés'),
        ('it', 'Italiano'),
        ('ru', 'Ruso'),
    ]
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    preferred_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null=True) 

class Organization1(models.Model):
    TYPES_CHOICES = [
        ('Derechos Humanos','Derechos Humanos'),
        ('Medio Ambiente','Medio Ambiente'),
        ('Salud','Salud'),
        ('Educación','Educación'),
        ('Animales','Animales'),
        ('Cultural y Arte','Cultural y Arte'),
        ('Alivio de la Pobreza','Alivio de la Pobreza'),
        ('Derechos de los Refugiados','Derechos de los Refugiados')
    ]
    VOLUNTEER_CHOICES = [
        ('1-10', '1 a 10'),
        ('10-30', '10 a 30'),
        ('30-50', '30 a 50'),
        ('+ 50', '+ 50'),
    ]
    organization_name = models.CharField(max_length=500, validators=[RegexValidator(r'^[a-zA-Z0-9\s,.]*$', 'Ingresa un nombre válido')])
    organization_mail = models.EmailField(max_length=300, unique=True)
    organization_address = models.CharField(max_length=800)
    organization_web = models.CharField(max_length=400)
    organization_description = models.TextField(max_length=2000)
    organization_type = models.CharField(max_length=300, choices=TYPES_CHOICES)
    volunteer_count = models.CharField(max_length=10, choices=VOLUNTEER_CHOICES,null=True)
    created_date = models.DateTimeField(default=timezone.now,blank=True , null=True)
    deleted_date = models.DateTimeField(blank=True , null=True)
    user_type = models.ForeignKey(ExtendedData, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization1, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    preferred_language = models.ForeignKey(PreferredLanguage,on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f'Comment by {self.user.username} on {self.organization.organization_name}'



class Interesados(models.Model):
    organizacion = models.ForeignKey(Organization1, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_interes = models.DateTimeField(auto_now_add=True)
    confirmado = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.voluntario.username} está interesado en {self.organizacion.organization_name}"

    