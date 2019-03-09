from django.conf import settings
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = settings.PER_PAGE
	template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
	post = get_object_or_404(
		Post,
		slug=post,
		status=Post.PUBLISHED,
		publish__year=year,
		publish__month=month,
		publish__day=day
	)
	return render(
		request,
		'blog/post/detail.html',
		{'post': post}
	)
