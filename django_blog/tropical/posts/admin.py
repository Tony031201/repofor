from django.contrib import admin
from .models import *
# Register your models here.

class AdminPost(admin.ModelAdmin):
    list_filter = ['price']
    list_display = ['title','price']
    search_fields = ['title','content']

    class Meta:
        model = Post

class AdminComment(admin.ModelAdmin):
    list_filter = ['publishing_date']
    search_fields = ['name','email','content','post__title']

    class Meta:
        model = Comment

admin.site.register(Post,AdminPost)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment,AdminComment)