import os
import random
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.text import slugify
from faker import Faker
from blog.models import Category, Author, Post, PostCategory, PostAuthor, Comment, CategoryChoices

class Command(BaseCommand):
    help = "Peuple la base de données du blog avec des articles, auteurs, catégories et commentaires"
    
    def add_arguments(self, parser):
        # Ajout d'une option pour supprimer les données existantes
        parser.add_argument(
            '--reset', 
            action='store_true', 
            help='Supprime toutes les données existantes avant de peupler la base'
        )
    
    def generate_content(self, fake, num_paragraphs=5, sentences_per_paragraph=5):
        """Génère du contenu HTML avec des paragraphes"""
        paragraphs = [
            f"<p>{fake.paragraph(nb_sentences=sentences_per_paragraph)}</p>"
            for _ in range(num_paragraphs)
        ]
        return "\n".join(paragraphs)
    
    def handle(self, *args, **kwargs):
        # Récupération de l'option reset
        reset = kwargs.get('reset', False)
        
        # Si reset est activé, supprimer toutes les données existantes
        if reset:
            self.stdout.write(self.style.WARNING("Suppression de toutes les données existantes..."))
            # Supprimer dans l'ordre pour respecter les contraintes de clé étrangère
            Comment.objects.all().delete()
            PostAuthor.objects.all().delete()
            PostCategory.objects.all().delete()
            Post.objects.all().delete()
            Author.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Toutes les données ont été supprimées."))
        
        fake = Faker(['fr_FR'])  # Utilisation du français


        # Création des catégories à partir de l'énumération
        self.stdout.write(self.style.NOTICE("Création des catégories..."))
        for category_choice in CategoryChoices:
            Category.objects.get_or_create(
                name=category_choice.value,
                defaults={"slug": slugify(category_choice.name)}
            )


        # Création de 10 auteurs
        self.stdout.write(self.style.NOTICE("Création des auteurs..."))
        
        for _ in range(10):
            name = fake.name()
            Author.objects.get_or_create(
                name=name,
                defaults={
                    "email": fake.email(),
                    "bio": fake.text(max_nb_chars=200),
                    "website": fake.url()
                }
            )
        
        authors = list(Author.objects.all())
        categories = list(Category.objects.all())
        

        # Récupération des images
        images_dir = os.path.join(settings.MEDIA_ROOT, 'blog', 'images')
        image_files = []
        
        # Vérification si le répertoire existe
        if os.path.exists(images_dir):
            image_files = [f for f in os.listdir(images_dir)
                           if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            self.stdout.write(self.style.SUCCESS(f"Trouvé {len(image_files)} images dans media/blog/images"))
        else:
            self.stdout.write(self.style.WARNING(f"Le répertoire {images_dir} n'existe pas"))
        
        # S'assurer qu'il y a assez d'images
        if len(image_files) < 30:
            self.stdout.write(self.style.WARNING(f"Seulement {len(image_files)} images trouvées, certains articles n'auront pas d'image"))


        # Création de 30 articles
        self.stdout.write(self.style.NOTICE("Création des articles..."))
        for i in range(30):
            title = fake.sentence(nb_words=6)[:-1]  # Enlever le point final
            slug = slugify(title)
            
            # Sélection d'une image si disponible
            imgpath = ""
            imgcaption = ""
            if image_files and i < len(image_files):
                imgpath = f"blog/images/{image_files[i]}"
                imgcaption = fake.sentence(nb_words=8)
            
            # Création de l'article
            post = Post.objects.create(
                title=title,
                slug=f"{slug}-{i}",  # Assurer l'unicité
                content=self.generate_content(fake),
                status="PUBLISHED" if random.random() > 0.2 else "DRAFT",
                imgpath=imgpath,
                imgcaption=imgcaption
            )
            
            # Association avec 1 à 3 catégories
            selected_categories = random.sample(categories, random.randint(1, min(3, len(categories))))
            for category in selected_categories:
                PostCategory.objects.create(
                    post=post,
                    category=category
                )
            
            # Association avec 1 à 2 auteurs
            selected_authors = random.sample(authors, random.randint(1, min(2, len(authors))))
            for idx, author in enumerate(selected_authors):
                PostAuthor.objects.create(
                    post=post,
                    author=author,
                    is_main_author=(idx == 0),  # Le premier auteur est l'auteur principal
                    contribution_description=fake.sentence()
                )
            
            # Ajout de 0 à 5 commentaires
            num_comments = random.randint(0, 5)
            for _ in range(num_comments):
                Comment.objects.create(
                    post=post,
                    name=fake.name(),
                    email=fake.email(),
                    content=fake.paragraph(),
                    accepted=random.random() > 0.3  # 70% des commentaires sont acceptés
                )
            
            self.stdout.write(self.style.SUCCESS(f"Créé article {i+1}: {title} {' avec image' if imgpath else ''}"))
        
        # Statistiques finales
        self.stdout.write(self.style.SUCCESS(f"Base de données peuplée avec succès !"))
        self.stdout.write(self.style.NOTICE(f"- {Post.objects.count()} articles créés"))
        self.stdout.write(self.style.NOTICE(f"- {Post.objects.filter(status='PUBLISHED').count()} articles publiés"))
        self.stdout.write(self.style.NOTICE(f"- {Comment.objects.count()} commentaires ajoutés"))
        self.stdout.write(self.style.NOTICE(f"- {Comment.objects.filter(accepted=True).count()} commentaires acceptés"))
