from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.hashers import make_password

from .models import Affaire, Client, Entreprise, Contrat, Autorisation, ChemiseDeTravaux, CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'password']  # Define the fields you want to display in the admin panel

    def save_model(self, request, obj, form, change):
        # Hash the password before saving the record
        print("ok")
        if obj.password:
            obj.password = make_password(obj.password)
        obj.save()

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Affaire)
admin.site.register(Client)
admin.site.register(Entreprise)
admin.site.register(Contrat)
admin.site.register(Autorisation)
admin.site.register(ChemiseDeTravaux)
