import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()


from blog.models import Author

#Author.objects.all().delete()
a1 = Author.objects.all()
print(a1)


