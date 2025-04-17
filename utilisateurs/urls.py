from django.urls import path
from . import views

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'), 
    path('accueil/', views.accueil, name='accueil'),
    path('interface_clients/', views.interface_clients, name='interface_clients'),

    #  Interface Admin
    path('interface_admin/', views.interface_admin, name='interface_admin'),
    path('admin_utilisateurs/', views.admin_utilisateurs, name='admin_utilisateurs'),
    path('admin_utilisateurs/modifier/<int:user_id>/', views.modifier_utilisateur, name='modifier_utilisateur'),
    path('admin_utilisateurs/supprimer/<int:user_id>/', views.supprimer_utilisateur, name='supprimer_utilisateur'),
   
    path('admin_categories/', views.admin_categories, name='admin_categories'),
    path('admin_categories/ajouter/', views.ajouter_categorie, name='ajouter_categorie'),
    path('admin_categories/modifier/<int:cat_id>/', views.modifier_categorie, name='modifier_categorie'),
    path('admin_categories/supprimer/<int:cat_id>/', views.supprimer_categorie, name='supprimer_categorie'),
    
    path('admin_produits/', views.admin_produits, name='admin_produits'),
    path('admin_produits/ajouter/', views.ajouter_produit, name='ajouter_produit'),
    path('admin_produits/modifier/<int:prod_id>/', views.modifier_produit, name='modifier_produit'),
    path('admin_produits/supprimer/<int:prod_id>/', views.supprimer_produit, name='supprimer_produit'),
    
]
