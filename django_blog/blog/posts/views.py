from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from .models import Post
from django.views.generic import DetailView
import sqlite3
from .forms import PostForm
# Create your views here.



def index(request):
    post_list = Post.objects.all().order_by("-id")
    query = request.GET.get('q')

    if query:
        post_list = post_list.filter(Q(title__icontains=query) | Q(content__icontains=query))



    paginator = Paginator(post_list,2)
    page = request.GET.get('page')
    post_list = paginator.get_page(page)

    context = {
        'posts':post_list
    }

    return render(request,'posts/index.html',context)

def detail_view(request,id):
    post = Post.objects.get(id=id)
    context = {
        'post':post
    }

    return render(request,'posts/detail.html',context)

@login_required(login_url='/')
def create_view(request):
    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        post = form.save()
        messages.success(request,"Your post has been saved.")
        return HttpResponseRedirect('/')

    context = {
        'form':form,
    }

    return render(request,'posts/create.html', context)

@login_required(login_url='/')
def delete_view(request,id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    messages.success(request, "Your post has been deleted.")
    return HttpResponseRedirect('/')

@login_required(login_url='/')
def update_view(request,id):
    post = get_object_or_404(Post,id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)

    if form.is_valid():
        form.save()
        return redirect('detail', id=post.id)

    context = {
        'form':form,
    }

    return render(request,'posts/create.html',context)