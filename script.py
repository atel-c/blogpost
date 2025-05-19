import django
import os
# Initialisation de l'environnement Django en dehors d'une commande ou d'un serveur web
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection


from blog.models import Post, HomepagePlacement


# On récupère tous les placements pour la page d'accueil, avec les objets Post associés
# grâce à `select_related('post')` pour éviter une requête par article
placements = HomepagePlacement.objects.select_related('post').order_by('-post__created_at')
 
# Préparation des variables pour les trois types d’emplacements
featured_post = None       # Article "À la une"
editorial_post = None      # Article éditorial
latest_post = None         # Article classique (non mis en avant)

# Parcours des placements pour attribuer les articles à leur zone d’affichage
for placement in placements:
    if placement.type == 'FEATURED' and not featured_post:
        featured_post = placement.post
    elif placement.type == 'EDITORIAL' and not editorial_post:
        editorial_post = placement.post
    elif placement.type == 'SANS' and not latest_post:
        latest_post = placement.post

    # On s'arrête dès qu'on a trouvé les trois
    if featured_post and editorial_post and latest_post:
        break

# Récupération des 5 derniers articles publiés, pour affichage dans la sidebar
# Cette requête est indépendante de la précédente
latest_posts = Post.objects.filter(status='PUBLISHED').order_by('-created_at')[:5]

# Affichage du nombre total de requêtes SQL effectuées
# Cela permet de vérifier que le code est optimisé (idéalement : une seule requête pour les placements)
print(f"Number of queries: {len(connection.queries)}")



# placements = HomepagePlacement.objects.select_related('post').all()
# for placement in placements:
#     print(placement.post, placement.type)

 
 
# posts_without_placement = Post.objects.filter(placement__isnull=True)
# for post in posts_without_placement:
#     HomepagePlacement.objects.create(post=post, type='SANS')




