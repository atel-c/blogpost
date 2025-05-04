from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from blog.models import Post

def index(request):
    posts = Post.objects.values()
   
    return JsonResponse(list(posts), safe=False)