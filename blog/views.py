from django.shortcuts import render
from datetime import datetime
from .models import Post

def post_list(request):
    posts = Post.objects.filter(published_date__lte=datetime.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
