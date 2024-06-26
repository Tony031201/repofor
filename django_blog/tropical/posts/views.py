from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormMixin
from django.http import JsonResponse

from .models import *
from .forms import *
# Create your views here.
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView

class IndexView(ListView):
    template_name = "posts/index.html"
    model = Post
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context['slider_posts'] = Post.objects.filter(slider_post=True)
        return context

class PostDetail(DetailView,FormMixin):
    template_name = 'posts/detail.html'
    model = Post
    context_object_name = 'single'
    form_class = CreateCommentForm

    def get_context_data(self, **kwargs):
        prev = Post.objects.filter(pk__lt=self.kwargs['pk']).order_by('-pk').first()
        next = Post.objects.filter(pk__gt=self.kwargs['pk']).order_by('pk').first()
        context = super(PostDetail,self).get_context_data(**kwargs)
        context["prev"] = prev
        context["next"] = next
        context['form'] = self.get_form()
        return context

    def get(self,request,*args,**kwargs):
        self.hit = Post.objects.filter(id=self.kwargs['pk']).update(hit=F('hit')+1)
        return super(PostDetail,self).get(request,*args,**kwargs)

    def form_valid(self, form):
        if form.is_valid():
            form.instance.post = self.object
            form.save()
            return super(PostDetail,self).form_valid(form)
        else:
            return super(PostDetail, self).form_invalid(form)

    def post(self,*args,**kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_valid(form)

    def get_success_url(self):
        return reverse('detail',kwargs={"pk":self.object.pk,"slug":self.object.slug})


class CategoryDetail(ListView):
    template_name = "categories/category_detail.html"
    model = Post
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        self.category = get_object_or_404(Category,pk=self.kwargs['pk'])
        return Post.objects.filter(category=self.category).order_by('-id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryDetail,self).get_context_data(**kwargs)
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        context['category'] = self.category
        return context

class TagDetail(ListView):
    template_name = "tags/tag_detail.html"
    model = Post
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        self.tag = get_object_or_404(Tag,slug=self.kwargs['slug'])
        return Post.objects.filter(tag=self.tag).order_by('-id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TagDetail,self).get_context_data(**kwargs)
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        context['tag'] = self.tag
        return context

@method_decorator(login_required(login_url='users/login'),name='dispatch')
class CreatePostView(CreateView):
    template_name = 'posts/create_post.html'
    form_class = PostCreationForm
    model = Post

    def get_success_url(self):
        return reverse('detail',kwargs={'pk':self.object.pk,'slug':self.object.slug})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()

        tags = self.request.POST.get('tag').split(',')

        for tag in tags:
            current_tag = Tag.objects.filter(slug=slugify(tag))
            if current_tag.count() < 1:
                create_tag = Tag.objects.create(title=tag)
                form.instance.tag.add(create_tag)
            else:
                existed_tag = Tag.objects.get(slug=slugify(tag))
                form.instance.tag.add(existed_tag)

        return super(CreatePostView, self).form_valid(form)


class UpdatePostView(UpdateView):
    model = Post
    template_name = 'posts/post-update.html'
    form_class = PostUpdateForm

    def get_success_url(self):
        return reverse('detail',kwargs={'pk':self.object.pk,'slug':self.object.slug})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.tag.clear()

        tags = self.request.POST.get('tag').split(',')

        for tag in tags:
            current_tag = Tag.objects.filter(slug=slugify(tag))
            if current_tag.count() < 1:
                create_tag = Tag.objects.create(title=tag)
                form.instance.tag.add(create_tag)
            else:
                existed_tag = Tag.objects.get(slug=slugify(tag))
                form.instance.tag.add(existed_tag)

        return super(UpdatePostView, self).form_valid(form)

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()

        if self.object.user != request.user:
            return HttpResponseRedirect('/')
        return super(UpdatePostView,self).get(request,*args,**kwargs)

class DeletePostView(DeleteView):
    model = Post
    success_url = '/'
    template_name = 'posts/delete_post.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            self.object.delete()
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect('/')
        else:
            return super(DeletePostView,self).get(request, *args, **kwargs)

class SearchView(ListView):
    model = Post
    template_name = 'posts/search.html'
    paginate_by = 4
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            return Post.objects.filter(Q(title__icontains=query)|
                                       Q(content__icontains=query)|
                                       Q(tag__title__icontains=query)
                                       ).order_by('id').distinct()
        return Post.objects.all().order_by('id')

def update_likes(request):

    if request.method == 'GET':
        post_id=int(request.GET.get('userid'))
        post = get_object_or_404(Post,pk=post_id)

        post.love_point += 1
        post.save()

        return JsonResponse({'new_likes':post.love_point})

    return JsonResponse({'error': 'Invalid request'}, status=400)

class testindex(TemplateView):
    template_name = 'posts/testindex.html'
