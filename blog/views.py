from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from blog.models import Post, HomepagePlacement



def index(request):
    # Get all placements with their related posts in a single query
    placements = HomepagePlacement.objects.select_related('post').order_by('-post__created_at')

    featured_post = None
    editorial_post = None
    latest_post = None

    for placement in placements:
        if placement.type == 'FEATURED' and not featured_post:
            featured_post = placement.post
        elif placement.type == 'EDITORIAL' and not editorial_post:
            editorial_post = placement.post
        elif placement.type == 'SANS' and not latest_post:
            latest_post = placement.post

        # Stop once we have all three
        if featured_post and editorial_post and latest_post:
            break
     # Récupération des 5 derniers articles publiés pour lla liste de la barre latérale
    latest_posts = Post.objects.filter(status='PUBLISHED').order_by('-created_at')[:5]

    context = {
        'featured_post': featured_post,
        'editorial_post': editorial_post,
        'latest_post': latest_post,
        'post_list': latest_posts,
    }
    return render(request, 'blog/index.html', context)




# def index(request):
#     posts = Post.objects.all()
#     context = {
#         'posts': posts
#     }
#     return render(request, 'blog/index.html', context)



# def index(request):
#     posts = Post.objects.all()
#     output = "\n".join(['<li>'+(post.title)+'</li>' for post in posts])
#     htm_output = f'<ul>{output}</ul>'
#     return HttpResponse(htm_output, content_type="text/html; charset=utf-8")

# def index(request):
#     posts = Post.objects.all()
#     output = "\n".join([post.title for post in posts])
#     return HttpResponse(output, content_type="text/plain; charset=utf-8")


# def index(request):
#     posts = Post.objects.values()
   
#     return JsonResponse(list(posts), safe=False)

def category_posts(request, slug):
    return HttpResponse(f" Page en construction: Categorie: {slug}")

def post_detail(request, slug):
    return HttpResponse(f" Page en construction: Poste: {slug}")

def about(request):
    return HttpResponse(f" Page en construction: A-propos")

def contact(request):
    return HttpResponse(f" Page en construction: Contact")