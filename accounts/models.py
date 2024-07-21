from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    username = models.CharField('ID', 
                    max_length=8, 
                    unique=True, 
                    null=False,
                    validators=[RegexValidator(r'^[0-9]{8}$')],
                )
    email = models.EmailField('メールアドレス', max_length=254, unique=True, null=False)
    first_name = models.CharField('名前', max_length=30, blank=False, null=False)
    last_name = models.CharField('苗字', max_length=30, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"