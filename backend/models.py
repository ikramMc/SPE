from django.db import models
# models.py
# backend/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.contrib.auth.hashers import make_password

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("The Username field must be set")
        print(password)
        # Hash the password using Django's make_password function
        hashed_password = make_password(password)
        
        user = self.model(username=username, password=hashed_password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    # Other fields you may have in your user model
    print("here1")
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
# Create your models here.
class Client (models.Model):
    idClient=models.AutoField(primary_key=True)
    nom=models.CharField(max_length=150,unique=True,null=False )
class Entreprise (models.Model):
    idEntreprise=models.AutoField(primary_key=True)
    raisonSocial=models.CharField(max_length=100,unique=True)
class Contrat (models.Model):
    idContrat=models.AutoField(primary_key=True,null=False)
    numContrat=models.CharField(max_length=40,null=True,unique=True)#a modifier
    
    
class Affaire (models.Model):
   class Energie (models.TextChoices):
     ELEC='ELEC'
     GAZ='GAZ'
   class Communes (models.TextChoices):
     AT='AIN TAYA'
     BEZ='BAB EZZOUAR'
     BEB='BORDJ EL BAHRI'
     DEB='DAR EL BEIDA'
     MDA='MOHAMMADIA'
     BEK='BORDJ EL KIFFAN'
     DER='DERGANA'
     EL_HAMIZ='EL HAMIZ'
     EL_MARSA='EL MARSA'


   idAffaire=models.AutoField(primary_key=True) 
   energie=models.CharField(max_length=15,choices=Energie.choices,null=True)
   remarque=models.CharField(max_length=300,null=True)
   numAFF=models.CharField(max_length=20)
   numOET=models.CharField(max_length=50,null=True)

   detailObjet=models.CharField(max_length=300,null=True)
   adresse=models.CharField(max_length=150,null=True)
   commune=models.CharField(max_length=40,choices=Communes.choices,null=True)
   montant=models.CharField(max_length=40,null=True )
   #ODSAnnule=models
   dateAriveDRS=models.DateField(default=None,null=True)
   dateEnvoiAPC=models.DateField(default=None,null=True)
   dateEnvoiADCAPC=models.DateField(null=True,default=None)
   sitAff=models.CharField(max_length=180,null=True)
   numODS=models.CharField(max_length=60,null=True)
   client=models.ForeignKey(Client,on_delete=models.CASCADE,default=None,null=True)
   entreprise=models.ForeignKey(Entreprise,on_delete=models.CASCADE,default=None ,null=True)
   contrat=models.ForeignKey(Contrat,on_delete=models.CASCADE,default=None ,null=True)

class Autorisation(models.Model):
    idAutorisation=models.AutoField(primary_key=True)
    numAutor=models.CharField(max_length=60,null=True)
    dateAutor=models.DateField(null=True)
    numDemAutor=models.CharField(max_length=60,null=True)
    dateDEmendaAuto=models.DateField(null=True)
    affaire=models.ForeignKey(Affaire,on_delete=models.CASCADE,default=None)
   
class ChemiseDeTravaux(models.Model):
    idChemise=models.AutoField(primary_key=True)
    DRCHT=models.DateField(null=True)
    affaire=models.ForeignKey(Affaire,on_delete=models.CASCADE,default=None)
    MTA=models.CharField(max_length=60,null=True)
    MTS=models.CharField(max_length=60,null=True)
    BTA=models.CharField(max_length=60,null=True)
    BTS=models.CharField(max_length=60,null=True)
    TYPE=models.CharField(max_length=60,null=True)
    EQUIP=models.CharField(max_length=60,null=True)
    PUISS=models.CharField(max_length=60,null=True)
    BRT_2F=models.CharField(max_length=60,null=True)
    BRT_4F=models.CharField(max_length=60,null=True)
    PE250=models.CharField(max_length=60,null=True)
    PE200=models.CharField(max_length=60,null=True)
    PE125=models.CharField(max_length=60,null=True)
    PE63=models.CharField(max_length=60,null=True)
    PE40=models.CharField(max_length=60,null=True)
    AC=models.CharField(max_length=60,null=True)
    BRTS=models.CharField(max_length=60,null=True)
    CM=models.CharField(max_length=60,null=True)
    