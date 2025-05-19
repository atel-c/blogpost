from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext as _
from .models import Category, Author, Post, PostCategory, PostAuthor, Comment, Contact, HomepagePlacement


class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1
    autocomplete_fields = ['category']

class PostAuthorInline(admin.TabularInline):
    model = PostAuthor
    extra = 1
    autocomplete_fields = ['author']
    fields = ['author', 'is_main_author', 'contribution_description']


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ['name', 'email', 'content', 'accepted']
    readonly_fields = ['created_at']
    show_change_link = True
    can_delete = True

class HomepagePlacementInline(admin.TabularInline):
    model = HomepagePlacement
    extra = 1  # Nombre de formulaires vides affichés par défaut

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_name_display', 'slug']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'website']
    search_fields = ['name', 'email']
    list_filter = ['name']
    




@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'created_at', 'get_placement_type','display_categories', 'display_authors', 'has_image']
    list_filter = ['status', 'created_at', 'categories']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    inlines = [PostCategoryInline, PostAuthorInline, CommentInline, HomepagePlacementInline]
    readonly_fields = ['created_at', 'updated_at', 'image_preview']
    fieldsets = [
        (None, {
            'fields': ('title', 'slug', 'status')
        }),
        ('Contenu', {
            'fields': ('content',)
        }),
        ('Image', {
            'fields': ('imgpath', 'imgcaption', 'image_preview'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    ]
    
    def display_categories(self, obj):
        return ", ".join([category.get_name_display() for category in obj.categories.all()[:3]])
    display_categories.short_description = "Catégories"
    
    def display_authors(self, obj):
        authors = PostAuthor.objects.filter(post=obj).order_by('-is_main_author')
        return ", ".join([author.author.name for author in authors[:3]])
    display_authors.short_description = "Auteurs"
    
    def has_image(self, obj):
        return bool(obj.imgpath)
    has_image.boolean = True
    has_image.short_description = "Image"
    
    def image_preview(self, obj):
        if obj.imgpath:
            return format_html('<img src="/media/{}" style="max-height: 200px; max-width: 400px;" /><br/><em>{}</em>', 
                              obj.imgpath, obj.imgcaption)
        return "Aucune image"
    image_preview.short_description = "Aperçu de l'image"

    def get_placement_type(self, obj):
        if hasattr(obj, 'placement'):
            return obj.placement.get_type_display()
        return "-"
    get_placement_type.short_description = _('Placement Type')  # Translated header


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created_at', 'accepted']
    list_filter = ['accepted', 'created_at']
    search_fields = ['name', 'email', 'content', 'post__title']
    list_editable = ['accepted']
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('post')
    

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'responded']
    list_filter = ['responded', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    list_editable = ['responded']
    date_hierarchy = 'created_at'
    fieldsets = [
        (None, {
            'fields': ('name', 'email', 'subject')
        }),
        ('Message', {
            'fields': ('message', 'created_at', 'responded')
        })
    ]










