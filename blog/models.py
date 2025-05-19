from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager


class CategoryChoices(models.TextChoices):
    POLITICS = 'politics', _('Politics')
    ECONOMY = 'economy', _('Economy')
    CULTURE = 'culture', _('Culture')
    PHILOSOPHY = 'philosophy', _('Philosophy')
    TECHNOLOGY = 'technology', _('Technology')
    LIFESTYLE = 'lifestyle', _('Lifestyle')
 

class Category(models.Model):
    name = models.CharField(
        _("name"),
        max_length=20,
        choices=CategoryChoices.choices,
        unique=True
    )
    slug = models.SlugField(_("slug"), max_length=100, unique=True)


    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ["name"]
    
    def __str__(self):
        return self.get_name_display()
    
    
class Author(models.Model):
    name = models.CharField(_("name"), max_length=100)
    email = models.EmailField(_("email"), blank=True)
    bio = models.TextField(_("bio"), blank=True)
    website = models.URLField(_("website"), blank=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=200, unique=True)
    content = models.TextField(_("content"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    imgpath = models.CharField(_("image path"), max_length=255, blank=True)
    imgcaption = models.CharField(_("image caption"), max_length=255, blank=True)

    status = models.CharField(
        max_length=10,
        choices=models.TextChoices("Status", "DRAFT PUBLISHED").choices,
        default="DRAFT",
        verbose_name=_("status")
    )

    categories = models.ManyToManyField(
        Category, 
        through='PostCategory', 
        related_name='posts', 
        verbose_name=_("categories")
    )
    authors = models.ManyToManyField(
        Author, 
        through='PostAuthor', 
        related_name='posts', 
        verbose_name=_("authors")
    )

    tags = TaggableManager(verbose_name=_("tags"), blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:post_detail', args=[self.slug])
    


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_("post"))
    name = models.CharField(_("name"), max_length=100)
    email = models.EmailField(_("email"))
    content = models.TextField(_("content"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    accepted = models.BooleanField(_("accepted"), default=False)
    
    class Meta:
        ordering = ['created_at']
        indexes = [models.Index(fields=['created_at'])]
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
    
    def __str__(self):
        return f"Comment by {self.name} on '{self.post.title[:30]}'"


class Contact(models.Model):
    name = models.CharField(_("name"), max_length=100)
    email = models.EmailField(_("email"))
    subject = models.CharField(_("subject"), max_length=200)
    message = models.TextField(_("message"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    responded = models.BooleanField(_("responded"), default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Contact message")
        verbose_name_plural = _("Contact messages")
    
    def __str__(self):
        return f"Contact from {self.name}: {self.subject}"







class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_("post"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("category"))
    added_at = models.DateTimeField(_("added_at"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Post category")
        verbose_name_plural = _("Post categories")
        unique_together = ('post', 'category')
    
    def __str__(self):
        return f"{self.post.title} — {self.category.get_name_display()}"

class PostAuthor(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_("post"))
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_("author"))
    is_main_author = models.BooleanField(_("is main author"), default=False)
    contribution_description = models.CharField(_("contribution description"), max_length=255, blank=True)
    added_at = models.DateTimeField(_("added at"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Post author")
        verbose_name_plural = _("Post authors")
        unique_together = ('post', 'author')
    
    def __str__(self):
        return f"{self.author.name} on {self.post.title}"
    

# ajout du modèle HomepagePlacement pour les postes mis en exergue et les postes éditoriaux
class HomepagePlacement(models.Model):
    TYPE_CHOICES = [
        ('FEATURED', 'À la une'),
        ('EDITORIAL', 'Éditorial'),
        ('SANS', 'Sans'),
    ]
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='placement')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='SANS')
    
    class Meta:
        verbose_name = _("Placement en page d'accueil")
        verbose_name_plural = _("Placements en page d'accueil")
    
    def __str__(self):
        return f"{self.post.title} - {self.get_type_display()}"