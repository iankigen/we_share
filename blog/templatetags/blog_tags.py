from django import template
from django.conf import settings
from django.db.models import Count
from django.utils.safestring import mark_safe
from markdown import markdown

from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
	return Post.published.count()


@register.inclusion_tag('blog/post/latest.html')
def show_latest_posts(count=None):
	latest_posts = Post.published.order_by('-publish')[:count or settings.LATEST_POST_COUNT]
	return {
		'latest_posts': latest_posts
	}


@register.simple_tag
def get_most_commented_posts(count=5):
	return Post.published.annotate(total_comments=Count('comments')).order_by(
		'-total_comments'
	).exclude(total_comments=0)[:count]


@register.filter(name='markdown')
def markdown_format(text):
	return mark_safe(markdown(text))
