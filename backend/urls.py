from django.urls.resolvers import URLPattern
from backend import views

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


urlpatterns = [
   
     path('creationAffaire/', views.creationAPI),
     path('creationEntreprise/', views.creationEntreprise),
     path('creationContrat/', views.creationContrat),
     path('creationAutor/', views.creationAutor),
     path('search/',views.searchAffaire),
     path('stats/',views.calculate_percentages),
     path('annulation/',views.retounerAffaire),
     path('relancement/',views.relancerAffaire),
     path('chemise/',views.modifierChemise),
     path('login/', views.login_view, name='login'),
     path('logout/', views.logout_view, name='logout'),
     path('token/', views.check_token),
    
  
     ]