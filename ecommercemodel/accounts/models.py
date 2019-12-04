# coding=utf-8

import re

from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin

class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField("Usuário", max_length=30, unique=True, validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'), "Informe um nome de usuário válido. Este valor pode conter apenas letras, números e os seguintes caracteres @/./+/-/_.", 'invalid')], help_text="Obrigatório. Insira aqui um nome de usuário com 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.")
    email = models.EmailField("E-mail", unique=True, help_text="Obrigatório. Insira aqui um e-mail válido.")
    name = models.CharField("Nome completo", blank=False, max_length=100, help_text="Obrigatório. Insira aqui seu nome completo.")
    is_active = models.BooleanField("Ativo", blank=True, default=True, help_text="Indica que este usuário está ativo para logar.")
    is_staff = models.BooleanField("Membro da equipe", blank=True, default=False, help_text="Indica que este usuário é membro da equipe de administradores.")
    date_joined = models.DateTimeField("Data do Registro", auto_now_add=True)
    avatar = models.ImageField("Imagem de Perfil", upload_to="accounts/profile_avatar", null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.name or self.username

    def get_full_name(self):
        return str(self)

    def get_short_name(self):
        return str(self).split(' ')[0]