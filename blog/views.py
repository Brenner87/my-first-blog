from django.shortcuts import render, get_object_or_404
from datetime import datetime
from .models import Post, Comment
from .forms import PostForm, LoginForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse


def post_list(request):
    posts = Post.objects.filter(published_date__lte=datetime.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_draft_list(request):
    posts=Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts':posts})

@login_required
def post_publish(request, pk):
    post=get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post=get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')



def post_detail(request, pk):
    post=get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

@login_required
def post_new(request):
    if request.method=="POST":
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form=PostForm()
    return render(request, 'blog/post_edit.html', {'form':form})

@login_required
def post_edit(request, pk):
    post=get_object_or_404(Post, pk=pk)
    if request.method=="POST":
        form=PostForm(request.POST, instance=post)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.published_date=datetime.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form=PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def user_login(request):
    errors=[]
    if request.method =='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('post_list')
                else:
                    errors.append('User is not active.')
#                    return render (request, 'registration/login.html', {'form': form})
            else:
                errors.append('User name or password is incorrect.')
#                return render (request, 'registration/login.html', {'form': form})
    else:
        form=LoginForm()
    return render(request, 'registration/login.html', {'form': form, 'errors': errors})

@login_required
def user_logout(request):
    logout(request)
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post=get_object_or_404(Post, pk=pk)
    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form=CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


