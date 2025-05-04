import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from blog.models import Post

posts = Post.objects.values()

for post in posts:
    print(post.title)


