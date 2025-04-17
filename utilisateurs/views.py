from django.shortcuts import render,get_object_or_404, redirect
from django.contrib import messages
from .models import User, Role
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from .models import User, Category, Product

def inscription(request):
    if request.method == "POST":
        prenom = request.POST.get('prenom')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('mot_de_passe')
        confirmation = request.POST.get('confirmation')
        role_nom = request.POST.get('role')

        if not role_nom:
            messages.error(request, "Veuillez sélectionner un rôle.")
            return redirect('inscription')

        if mot_de_passe != confirmation:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('inscription')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect('inscription')

        try:
            role = Role.objects.get(role_name__iexact=role_nom.strip())
        except Role.DoesNotExist:
            messages.error(request, "Rôle invalide.")
            return redirect('inscription')

        utilisateur = User(
            firstname=prenom,
            lastname=nom,
            email=email,
            password=make_password(mot_de_passe),
            role=role
        )
        utilisateur.save()

        messages.success(request, "Inscription réussie ! Connectez-vous.")
        return redirect('connexion')

    return render(request, 'utilisateurs/inscription.html', {'roles': Role.objects.all()})


def connexion(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        utilisateur = User.objects.filter(email=email).first()

        if utilisateur and check_password(password, utilisateur.password):
            request.session['utilisateur_id'] = utilisateur.id
            request.session['role'] = utilisateur.role.role_name

            if utilisateur.role.role_name.lower() == 'admin':
                return redirect("interface_admin")
            else:
                return redirect("interface_clients")
        else:
            messages.error(request, "Email ou mot de passe incorrect.")

    return render(request, 'utilisateurs/connexion.html')



def accueil(request):
    return render(request, 'utilisateurs/accueil.html')

def interface_clients(request):
    produits = Product.objects.all()  # Récupérer tous les produits
    return render(request, 'utilisateurs/interface_clients.html', {'produits': produits})

def interface_admin(request):
    return render(request, 'admin/interface_admin.html')


def interface_admin(request):
    return render(request, 'admin/interface_admin.html')

def admin_utilisateurs(request):
    utilisateurs = User.objects.all()  # Récupérer tous les utilisateurs
    return render(request, 'admin/admin_utilisateurs.html', {'utilisateurs': utilisateurs})

def admin_categories(request):
    categories = Category.objects.all()  # Récupérer toutes les catégories
    return render(request, 'admin/admin_categories.html', {'categories': categories})

def admin_produits(request):
    produits = Product.objects.select_related('category', 'user')  # Récupérer tous les produits avec leurs catégories et utilisateurs
    return render(request, 'admin/admin_produits.html', {'produits': produits})

def modifier_utilisateur(request, user_id):
    utilisateur = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        utilisateur.firstname = request.POST.get('firstname')
        utilisateur.lastname = request.POST.get('lastname')
        utilisateur.email = request.POST.get('email')
        utilisateur.save()
        messages.success(request, "Utilisateur modifié avec succès.")
        return redirect('admin_utilisateurs')
    return render(request, 'admin/modifier_utilisateur.html', {'utilisateur': utilisateur})

def supprimer_utilisateur(request, user_id):
    utilisateur = get_object_or_404(User, id=user_id)
    utilisateur.delete()
    messages.success(request, "Utilisateur supprimé avec succès.")
    return redirect('admin_utilisateurs')


def admin_categories(request):
    categories = Category.objects.all()  # Récupérer toutes les catégories
    return render(request, 'admin/admin_categories.html', {'categories': categories})

def ajouter_categorie(request):
    if request.method == 'POST':
        cat_name = request.POST.get('cat_name')
        if cat_name:
            Category.objects.create(cat_name=cat_name)
            messages.success(request, "Catégorie ajoutée avec succès.")
            return redirect('admin_categories')
        else:
            messages.error(request, "Le nom de la catégorie est requis.")
    return render(request, 'admin/ajouter_categorie.html')

def modifier_categorie(request, cat_id):
    categorie = get_object_or_404(Category, id=cat_id)
    if request.method == 'POST':
        cat_name = request.POST.get('cat_name')
        if cat_name:
            categorie.cat_name = cat_name
            categorie.save()
            messages.success(request, "Catégorie modifiée avec succès.")
            return redirect('admin_categories')
        else:
            messages.error(request, "Le nom de la catégorie est requis.")
    return render(request, 'admin/modifier_categorie.html', {'categorie': categorie})

def supprimer_categorie(request, cat_id):
    categorie = get_object_or_404(Category, id=cat_id)
    categorie.delete()
    messages.success(request, "Catégorie supprimée avec succès.")
    return redirect('admin_categories')

def admin_produits(request):
    produits = Product.objects.select_related('category', 'user')
    return render(request, 'admin/admin_produits.html', {'produits': produits})

def ajouter_produit(request):
    categories = Category.objects.all()
    utilisateurs = User.objects.all()
    if request.method == 'POST':
        pro_name = request.POST.get('pro_name')
        pro_price = request.POST.get('pro_price')
        pro_desc = request.POST.get('pro_desc')
        category_id = request.POST.get('category')
        user_id = request.POST.get('user')
        pro_image = request.FILES.get('pro_image')  # Récupérer l'image

        if pro_name and pro_price and category_id and user_id:
            category = get_object_or_404(Category, id=category_id)
            user = get_object_or_404(User, id=user_id)
            Product.objects.create(
                pro_name=pro_name,
                pro_price=pro_price,
                pro_desc=pro_desc,
                pro_image=pro_image,
                category=category,
                user=user
            )
            messages.success(request, "Produit ajouté avec succès.")
            return redirect('admin_produits')
        else:
            messages.error(request, "Tous les champs sont requis.")
    return render(request, 'admin/ajouter_produit.html', {'categories': categories, 'utilisateurs': utilisateurs})

def modifier_produit(request, prod_id):
    produit = get_object_or_404(Product, id=prod_id)
    categories = Category.objects.all()
    utilisateurs = User.objects.all()

    if request.method == 'POST':
        produit.pro_name = request.POST.get('pro_name')
        produit.pro_price = request.POST.get('pro_price')
        produit.pro_desc = request.POST.get('pro_desc')
        produit.category = get_object_or_404(Category, id=request.POST.get('category'))
        produit.user = get_object_or_404(User, id=request.POST.get('user'))
        if request.FILES.get('pro_image'):
            produit.pro_image = request.FILES.get('pro_image')  # Mettre à jour l'image si elle est fournie
        produit.save()
        messages.success(request, "Produit modifié avec succès.")
        return redirect('admin_produits')

    return render(request, 'admin/modifier_produit.html', {
        'produit': produit,
        'categories': categories,
        'utilisateurs': utilisateurs
    })

def supprimer_produit(request, prod_id):
    produit = get_object_or_404(Product, id=prod_id)
    produit.delete()
    messages.success(request, "Produit supprimé avec succès.")
    return redirect('admin_produits')