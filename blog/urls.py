from django.urls import path
from blog import views

app_name = "blog"


urlpatterns = [
    path("", views.index, name="home"),
    path("category/<str:slug>/", views.category_posts, name="category_posts"),
    path("post/<str:slug>/", views.post_detail, name="post_detail"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]