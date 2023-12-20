from backend.models import Affaire,Client ,Entreprise,Contrat,Autorisation,ChemiseDeTravaux
from rest_framework import fields,serializers



class AffaireSerializer (serializers.ModelSerializer):
 class Meta:
  model=Affaire
  fields='__all__'
 
 
class ClientSerializer (serializers.ModelSerializer):
 class Meta:
  model=Client
  fields='__all__'
class EntrepriseSerializer (serializers.ModelSerializer):
 class Meta:
  model=Entreprise
  fields='__all__' 
class ContratSerializer (serializers.ModelSerializer):
 class Meta:
  model=Contrat
  fields='__all__' 
class AutorisationSerializer (serializers.ModelSerializer):
 class Meta:
  model=Autorisation
  fields='__all__'
class ChemiseDeTravauxSerializer (serializers.ModelSerializer):
 class Meta:
  model=ChemiseDeTravaux
  fields='__all__'  
      