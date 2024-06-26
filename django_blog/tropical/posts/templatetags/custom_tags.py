from django import template
from posts.models import *

register = template.Library()

@register.simple_tag(name="categories")
def all_categories():
    return Category.objects.all()

@register.simple_tag(name="tags")
def all_tags():
    return Tag.objects.all()

@register.simple_tag(name="hit_post")
def hit_post():
    return Post.objects.order_by('-hit')[:5]
