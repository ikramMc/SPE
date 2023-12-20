from django.shortcuts import render
from backend.models import Affaire,Client ,Entreprise,CustomUser ,Contrat,Autorisation,ChemiseDeTravaux
from backend.serializers import AffaireSerializer,ClientSerializer,EntrepriseSerializer,ContratSerializer,AutorisationSerializer,ChemiseDeTravauxSerializer
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db.models import Count
# views.py
# views.py
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status,permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import TokenError, AccessToken
from rest_framework_simplejwt.backends import TokenBackend



def jwt_protected(view_func):
    
    return authentication_classes([TokenAuthentication])(
        permission_classes([IsAuthenticated])(view_func)
    )
@csrf_exempt
@permission_classes([permissions.IsAuthenticated])  
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = CustomUser.objects.get(username=username)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return JsonResponse({'message': 'Login successful', 'access_token': access_token})
        else:
            return JsonResponse({'message': 'Login failed'}, status=401)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    # Blacklist the token to log out the user
    refresh_token = request.data.get('refresh_token')
    token = RefreshToken(refresh_token)
    token.blacklist()
    return Response({'message': 'Logged out'})


@csrf_exempt
def creationAPI(request,pk=0):
  if request.method=='POST':
     affaires_data = JSONParser().parse(request)
     print(affaires_data)
     exist=Client.objects.filter(nom=affaires_data[0]['nom']).exists()
     if exist==False:
       client_serializer=ClientSerializer(data=affaires_data[0])
       if client_serializer.is_valid():
        client_serializer.save()
       elif  client_serializer.is_valid()==False:
         JsonResponse("les informations fournies ne sont pas correctes ou manquantes ", safe=False,status=400)
     ClientID=Client.objects.get(nom=affaires_data[0]['nom']).idClient
     affaires_data[1]['client']=ClientID
     affaires_data[1]['sitAff']="En programmation"
     if(affaires_data[1]['numOET']==''):
        affaires_data[1]['numOET']='MANQUE OET'
     affaires_serializer = AffaireSerializer(data=affaires_data[1] )
     if affaires_serializer.is_valid()  and Affaire.objects.filter(numAFF=affaires_data[1]['numAFF']).exists()==False :
        affaires_serializer.save()
        return JsonResponse("Ajoutée ", safe=False,status=200)
     elif affaires_serializer.is_valid()==False  or Affaire.objects.filter(numAFF=affaires_data[1]['numAFF']).exists() :
        return  JsonResponse("ce numero d'affaire existe déja ", safe=False,status=200)
@permission_classes([permissions.IsAuthenticated])    
def searchAffaire(request):
    # Récupérez les paramètres de requête GET
    numAff = request.GET.get('numAff', '')
    commune = request.GET.get('commune', '')
    nom = request.GET.get('nom', '')
    situation = request.GET.get('situation', '')
    entreprise = request.GET.get('entreprise', '')
   
    # Effectuez la recherche en fonction des paramètres
    affaires = Affaire.objects.filter(
        Q(numAFF__icontains=numAff) &
        Q(commune__icontains=commune) &
        Q(client__nom__icontains=nom) &
        Q(sitAff__icontains=situation) &
        (Q(entreprise__raisonSocial__icontains=entreprise)|Q(entreprise__isnull=True))
    ).distinct()


    results = []
    print(affaires[2].entreprise )
    for affaire in affaires:
        try:
        # Your existing code to get the ChemiseDeTravaux object
         chemise = ChemiseDeTravaux.objects.get(affaire=affaire.idAffaire)
        
        # Rest of your code...

        except ChemiseDeTravaux.DoesNotExist:
        # Handle the case when the ChemiseDeTravaux does not exist
         chemise=None

        result = {
            'id':affaire.idAffaire,
            'numAff': affaire.numAFF if affaire.numAFF is not None else '',
            'commune': affaire.commune if affaire.commune is not None else '',
            'adresse': affaire.adresse if affaire.adresse is not None else '',
            'energie': affaire.energie if affaire.energie is not None else '',
            'objet':affaire.detailObjet if affaire.detailObjet is not None else '',
            'client': affaire.client.nom if affaire.client is not None and affaire.client.nom is not None else '',
            'etat':affaire.sitAff,
            'numOET':affaire.numOET,
            'contrat':affaire.contrat.numContrat if affaire.contrat is not None and affaire.contrat.numContrat is not None else '',
            'entreprise': affaire.entreprise.raisonSocial if affaire.entreprise is not None and affaire.entreprise.raisonSocial is not None else '',
            'montant':affaire.montant if affaire.montant is not None else '',
            'ODS':affaire.numODS if affaire.numODS is not None else '',
            'date_arrivé_DRC':affaire.dateAriveDRS if affaire.dateAriveDRS is not None else '',
            'remarque':affaire.remarque if affaire.remarque is not None else '',
            'date_reception_chemise_travaux':chemise.DRCHT if chemise is not None else '', 
            'MTS': chemise.MTS if chemise is not None else '',
            'BTA': chemise.BTA if chemise is not None else '',
            'MTA': chemise.MTA if chemise is not None else '',
            'BTS': chemise.BTS if chemise is not None else '',
            'TYPE': chemise.TYPE if chemise is not None else '',
            'EQUIP': chemise.EQUIP if chemise is not None else '',
            'PUISS': chemise.PUISS if chemise is not None else '',
            'BRT_2F': chemise.BRT_2F if chemise is not None else '',
            'BRT_4F': chemise.BRT_4F if chemise is not None else '',
            'PE250': chemise.PE250 if chemise is not None else '',
            'PE200': chemise.PE200 if chemise is not None else '',
            'PE125': chemise.PE125 if chemise is not None else '',
            'PE63': chemise.PE63 if chemise is not None else '',
            'PE40': chemise.PE40 if chemise is not None else '',
            'AC': chemise.AC if chemise is not None else '',
            'BRTS': chemise.BRTS if chemise is not None else '',
            'CM': chemise.CM if chemise is not None else ''
        }
        results.append(result)
 
    return JsonResponse({'results': results})
def check_token(request):
     authorization_header = request.META.get('HTTP_AUTHORIZATION')

     if authorization_header and authorization_header.startswith('Bearer '):
        token = authorization_header.split(' ')[1]
       
        # Your token validation logic using TokenBackend
        if is_token_valid(token):
         return JsonResponse({'success': 'valid token'}, status=200)
        else: 
         return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
     else:
        return JsonResponse({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)
def calculate_percentages(request):
    # Access the token from the Authorization header in the request
    authorization_header = request.META.get('HTTP_AUTHORIZATION')

    if authorization_header and authorization_header.startswith('Bearer '):
        token = authorization_header.split(' ')[1]
       
        # Your token validation logic using TokenBackend
        if is_token_valid(token):
            if request.method == 'GET':
                # Your code to calculate percentages goes here
                queryset = Affaire.objects.all()
            sitaff_counts = queryset.values('sitAff').annotate(count=Count('sitAff'))

            total_count = queryset.count()

            # Calculate percentages
            percentages = []
            for item in sitaff_counts:
                sitaff = item['sitAff']
                count = item['count']

                percentages.append({'label': sitaff, 'value': count, 'backgroundColor': '#ffffff'})


                percentages = [{'label': item['sitAff'], 'value': item['count']} for item in sitaff_counts]

                return JsonResponse({'percentages': percentages})
            else:
                return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return JsonResponse({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)

def is_token_valid(token):
    try:
        token_backend = TokenBackend(algorithm='HS256')  # Use the appropriate algorithm
        token_data = token_backend.decode(token, verify=False)  # Verify the token if needed
        return True
    except Exception as e:
        return False

@csrf_exempt
def retounerAffaire(request,pk=0):
     if request.method=='POST':
        data_affaire=JSONParser().parse(request)
        print(data_affaire)
        numAff=data_affaire['numAff']
        affaire=Affaire.objects.get(numAFF=numAff)
        if affaire.sitAff !='Terminée' :
           affaire.sitAff='Retournee'
           affaire.remarque=data_affaire['remarque']
           affaire.save()
           return JsonResponse("l'affaire est annulée avec succés", safe=False)
        elif affaire.sitAff=='Terminée':
           return JsonResponse("l'affaire ne peut pas etre annulé elle est déja terminée ", safe=False)
@csrf_exempt
def relancerAffaire(request,pk=0):
     if request.method=='POST':
        data_affaire=JSONParser().parse(request)
        numAff=data_affaire['numAff']
        affaire=Affaire.objects.get(numAFF=numAff)
        if affaire.sitAff =='Retournee' :
           affaire.sitAff='En programmation'
           affaire.save()
           return JsonResponse("l'affaire est relancer avec succés", safe=False)
        elif affaire.sitAff=='Terminée':
           return JsonResponse("l'affaire ne peut pas etre relancer car elle n'et pas retourneé d'origine ", safe=False)

@csrf_exempt
def creationEntreprise(request,pk=0):
     if request.method=='POST':
        data_affaire=JSONParser().parse(request)
        print(data_affaire)
        numAff=data_affaire['numAff']
        affaire=Affaire.objects.get(numAFF=numAff)
        affaire.montant=data_affaire['montant']
        if(affaire.numOET=='MANQUE OET' and  data_affaire['numOET']!=''):
          affaire.numOET=data_affaire['numOET']
        affaire.sitAff='Etablissement contrat'
        exist=Entreprise.objects.filter(raisonSocial=data_affaire['entreprise']).exists()
        if exist==False:
           Entreprise_serializer=EntrepriseSerializer(data={"raisonSocial":data_affaire['entreprise']})
           if Entreprise_serializer.is_valid():
             Entreprise_serializer.save()
        entrepriseID=Entreprise.objects.get(raisonSocial=data_affaire['entreprise'])
        affaire.entreprise=entrepriseID
        affaire.save()
        return JsonResponse("modifiée", safe=False)
@csrf_exempt
def creationContrat(request,pk=0):
   if request.method=='POST':
      data_contrat=JSONParser().parse(request)
      affaire=Affaire.objects.get(numAFF=data_contrat[0]["numAff"])
      if(affaire.sitAff!='Instance OET'):
       exist=Contrat.objects.filter(numContrat=data_contrat[1]['numContrat']).exists()
       if exist==False:
         contrat_serializer=ContratSerializer(data=data_contrat[1])
         if contrat_serializer.is_valid(): 
          contrat_serializer.save()
      
      possible_values=['manque', 'manque oet','m/oet', 'm/oet+adc', 'm/ost', 'sans oet', 's/oet', 's/numero', 's/oet+s/devis']
      if (affaire.numOET.lower() in possible_values):
         if(affaire.sitAff!='Instance OET'):
          if (data_contrat[1]['numContrat']!=''):
           contratID=Contrat.objects.get(numContrat=data_contrat[1]['numContrat'])
           affaire.contrat=contratID
         if(data_contrat[0]['numOET']!=''):
            affaire.numOET=data_contrat[0]['numOET']
            affaire.sitAff='Etablissement contrat'
         elif(data_contrat[0]['numOET']==''):
            affaire.sitAff='Instance OET'    
         
         
      elif(affaire.numOET.lower() not in possible_values):
         affaire.numODS=data_contrat[0]["numODS"]
         contratID=Contrat.objects.get(numContrat=data_contrat[1]['numContrat'])
         affaire.contrat=contratID
         affaire.sitAff='Instance ADC'
      affaire.save()
      return JsonResponse("contrat enregistrée", safe=False)
@csrf_exempt
def creationAutor(request,pk=0):
   if request.method=='POST':
      data_autor=JSONParser().parse(request)
      affaire=Affaire.objects.get(numAFF=data_autor[0]["numAff"])
      affaire.sitAff='En cours des travaux'
      affaire.save()
      data_autor[1]['affaire']=affaire.idAffaire
      autor_serializer=AutorisationSerializer(data=data_autor[1])
      if autor_serializer.is_valid():
         autor_serializer.save()
         return JsonResponse("autorisation enregistrée", safe=False)
      return JsonResponse("error", safe=False)
@csrf_exempt
def modifierChemise(request):
   if request.method=='POST':
      data_chemise=JSONParser().parse(request)
      print(data_chemise[1])
      affaire=Affaire.objects.get(numAFF=data_chemise[0]['numAff'])
      affaire.remarque=data_chemise[2]['type']
      if (data_chemise[2]['type']=='partiel'):
         print('partiel')
         if(ChemiseDeTravaux.objects.filter(affaire=affaire.idAffaire).exists()):
              print("exist")
              chemise=ChemiseDeTravaux.objects.get(affaire=affaire.idAffaire)
              MTA= data_chemise[1]['MTA']              
              MTS = data_chemise[1]['MTS']
              BTA = data_chemise[1]['BTA']
              BTS = data_chemise[1]['BTS']
              TYPE= data_chemise[1]['TYPE']
              EQUIP = data_chemise[1]['EQUIP'] 
              PUISS = data_chemise[1]['PUISS']
              BRT_2F = data_chemise[1]['BRT_2F']
              BRT_4F = data_chemise[1]['BRT_4F']
              PE250= data_chemise[1]['PE250']
              PE200 = data_chemise[1]['PE200']
              PE125 = data_chemise[1]['PE125']
              PE63 = data_chemise[1]['PE200']
              PE40 = data_chemise[1]['PE40']
              AC= data_chemise[1]['AC']
              BRTS = data_chemise[1]['BRTS']
              CM = data_chemise[1]['CM']
              
    
    # Update the object's attributes with the new values
              if MTA:
                chemise.MTA = MTA
              if MTS:
                 chemise.MTS =MTS
              if BTA:
                chemise.BTA = BTA
              if BTS:
                 chemise.BTS =BTS
              if TYPE:
                chemise.TYPE =TYPE
              if EQUIP :
                 chemise.EQUIP  = EQUIP 
              if PUISS:
                chemise.PUISS = PUISS
              if BRT_2F:
                 chemise.BRT_2F =BRT_2F
              if BRT_4F:
                chemise.BRT_4F =BRT_4F
              if PE250:
                 chemise.PE250 = PE250
              if PE200:
                chemise.PE200= PE200
              if PE125:
                 chemise.PE125 = PE125
              if PE63:
                chemise.PE63 = PE63
              if PE40:
                 chemise.PE40 = PE40
              if AC:
                 chemise.AC = AC
              if BRTS:
                 chemise.BRTS=BRTS
              if CM:
                 chemise.CM = CM  
              chemise.save()          
         elif(ChemiseDeTravaux.objects.filter(affaire=affaire.idAffaire).exists()==False):
             print("non exist")
            
             data_chemise[1]["affaire"]=affaire.idAffaire
             print(data_chemise[1])
             chemiseSerializer=ChemiseDeTravauxSerializer(data=data_chemise[1])
             if chemiseSerializer.is_valid():
               chemiseSerializer.save()
             elif chemiseSerializer.is_valid()==False:
               print("il manque d'infos")
      elif  (data_chemise[2]['type']=='entière'):
          if(ChemiseDeTravaux.objects.filter(affaire=data_chemise[0]['numAff']).exists()):
              chemise=ChemiseDeTravaux.objects.get(affaire=data_autor[0]['numAff'])
              MTA= data_chemise[1]['MTA']              
              MTS = data_chemise[1]['MTS']
              BTA = data_chemise[1]['BTA']
              BTS = data_chemise[1]['BTS']
              TYPE= data_chemise[1]['TYPE']
              EQUIP = data_chemise[1]['EQUIP'] 
              PUISS = data_chemise[1]['PUISS']
              BRT_2F = data_chemise[1]['BRT_2F']
              BRT_4F = data_chemise[1]['BRT_4F']
              PE250= data_chemise[1]['PE250']
              PE200 = data_chemise[1]['PE200']
              PE125 = data_chemise[1]['PE125']
              PE63 = data_chemise[1]['PE200']
              PE40 = data_chemise[1]['PE40']
              AC= data_chemise[1]['AC']
              BRTS = data_chemise[1]['BRTS']
              CM = data_chemise[1]['CM']
              
    
    # Update the object's attributes with the new values
              if MTA:
                chemise.MTA = MTA
              if MTS:
                 chemise.MTS =MTS
              if BTA:
                chemise.BTA = BTA
              if BTS:
                 chemise.BTS =BTS
              if TYPE:
                chemise.TYPE =TYPE
              if EQUIP :
                 chemise.EQUIP  = EQUIP 
              if PUISS:
                chemise.PUISS = PUISS
              if BRT_2F:
                 chemise.BRT_2F =BRT_2F
              if BRT_4F:
                chemise.BRT_4F =BRT_4F
              if PE250:
                 chemise.PE250 = PE250
              if PE200:
                chemise.PE200= PE200
              if PE125:
                 chemise.PE125 = PE125
              if PE63:
                chemise.PE63 = PE63
              if PE40:
                 chemise.PE40 = PE40
              if AC:
                 chemise.AC = AC
              if BRTS:
                 chemise.BRTS=BRTS
              if CM:
                 chemise.CM = CM  
              chemise.save()
          elif(ChemiseDeTravaux.objects.filter(affaire=data_chemise[0]['numAff']).exists()==False):
             chemiseSerializer=ChemiseDeTravauxSerializer(data=data_chemise[1])
             if chemiseSerializer.is_valid():
               chemiseSerializer.save()
          affaire.sitAff='Terminée' 
      affaire.save()
      return JsonResponse("ok", safe=False)    
         

             
             