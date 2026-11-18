from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required 
from .models import Article
from .forms import ArticleForm 
from .models import Article, Commentaire 
from .forms import ArticleForm, CommentaireForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 


def accueil_view(request):
    tous_les_articles = Article.objects.all().order_by('-date_creation')
    paginator = Paginator(tous_les_articles, 5)
    page_numero = request.GET.get('page')

    try:
        articles_pages = paginator.page(page_numero)
    except PageNotAnInteger:
        articles_pages = paginator.page(1)
    except EmptyPage:
        articles_pages = paginator.page(paginator.num_pages)

    context = {
        'articles_a_afficher': articles_pages,
    }

    return render(request, 'blogapp/accueil.html', context)



def inscription_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Sauvegarde le nouvel utilisateur
            login(request, user)  # Connecte l'utilisateur
            return redirect('blogapp:accueil')
    else:
        form = UserCreationForm()
    return render(request, 'blogapp/inscription.html', {'form': form})



def connexion_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('blogapp:accueil')
    else:
        form = AuthenticationForm()
    return render(request, 'blogapp/connexion.html', {'form': form})



def deconnexion_view(request):
    if request.method == 'POST': # C'est une bonne pratique de faire la déconnexion sur unPOST
     logout(request)
     return redirect('blogapp:accueil')
    logout(request) # Pour une version ultra-simple accessible par un lien GET
    return redirect('blogapp:accueil')



@login_required
def creer_article_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            nouvel_article = form.save(commit=False)
            nouvel_article.auteur = request.user
            nouvel_article.save()
            return redirect('blogapp:detail_article', pk=nouvel_article.pk)
    else:
        form = ArticleForm()

    return render(request, 'blogapp/creer_modifier_article.html', {
        'form': form,
        'action': 'Créer',
    })



def detail_article_view(request, pk):
   article = get_object_or_404(Article, pk=pk) 
   context = {
      'article': article
  }
   return render(request, 'blogapp/detail_article.html', context)


@login_required
def modifier_article_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return redirect('blogapp:detail_article', pk=article.pk)
    if request.method == 'POST':
       form = ArticleForm(request.POST, instance=article) 
       if form.is_valid():
          form.save()
          return redirect('blogapp:detail_article', pk=article.pk)
    else:
      form = ArticleForm(instance=article) 

      context = {
          'form': form,
          'action': 'Modifier', # Pour le template
          'article': article # Pour afficher le titre par exemple
      }
      return render(request, 'blogapp/creer_modifier_article.html', context)



@login_required
def supprimer_article_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.auteur != request.user:
       return redirect('blogapp:detail_article', pk=article.pk) 
    if request.method == 'POST': 
       article.delete()
       return redirect('blogapp:accueil') 

    context = {
      'article': article
   }
    return render(request, 'blogapp/confirmer_suppression_article.html', context)    



@login_required
def ajouter_commentaire_view(request, article_pk): 
   article = get_object_or_404(Article, pk=article_pk)
   if article.auteur == request.user:
      return redirect('blogapp:detail_article', pk=article.pk)
   if request.method == 'POST':
      form = CommentaireForm(request.POST)
      if form.is_valid():
         commentaire = form.save(commit=False)
         commentaire.article = article
         commentaire.auteur = request.user
         commentaire.save()
         return redirect('blogapp:detail_article', pk=article.pk)
      else:
         return redirect('blogapp:detail_article', pk=article.pk)



def detail_article_view(request, pk):
  article = get_object_or_404(Article, pk=pk)
  commentaire_form = CommentaireForm()

  context = {
     'article': article,
     'commentaire_form': commentaire_form,
  }
  return render(request, 'blogapp/detail_article.html', context)




def profil_utilisateur_view(request, username):
  utilisateur_profil = get_object_or_404(User, username=username)
  articles_utilisateur = Article.objects.filter(auteur=utilisateur_profil).order_by('-date_creation')
  context = {
     'utilisateur_profil': utilisateur_profil,
     'articles_utilisateur': articles_utilisateur, }
  return render(request, 'blogapp/profil_utilisateur.html', context)