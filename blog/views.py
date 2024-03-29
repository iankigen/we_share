from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from taggit.models import Tag
from .documents import PostDocument
from .models import Post
from .forms import EmailPostForm, CommentForm, SearchForm


class PostListView(ListView):
	queryset = Post.published.all()
	context_object_name = 'posts'
	paginate_by = settings.PER_PAGE
	template_name = 'blog/post/list.html'

	def get_context_data(self, **kwargs):
		tag = None
		posts = Post.published.all()
		if 'tag' in self.kwargs.keys():
			tag = self.kwargs.get('tag')
			tag_obj = get_object_or_404(Tag, slug=tag)
			posts = Post.published.filter(tags__in=[tag_obj])
		context = super().get_context_data(object_list=posts, **kwargs)
		context['posts'] = posts
		context['tag'] = tag

		return context


def post_detail(request, year, month, day, post):
	post = get_object_or_404(
		Post,
		slug=post,
		status=Post.PUBLISHED,
		publish__year=year,
		publish__month=month,
		publish__day=day
	)
	comments = post.comments.filter(active=True)
	new_comment = None
	if request.method == 'POST':
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.post = post
			new_comment.save()
	else:
		comment_form = CommentForm()

	post_tags_id = post.tags.values_list('id', flat=True)
	similar_posts = Post.published.filter(tags__in=post_tags_id).exclude(id=post.id)
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by(
		'-same_tags', '-publish'
	)[:settings.SUGGESTIONS]
	return render(
		request,
		'blog/post/detail.html',
		{
			'post': post,
			'comment_form': comment_form,
			'comments': comments,
			'new_comment': new_comment,
			'similar_posts': similar_posts
		}
	)


def post_share(request, post_id):
	form = EmailPostForm()
	post = get_object_or_404(Post, id=post_id)
	sent = False
	data = {}
	if request.method == 'POST':
		form = EmailPostForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = "{} ({}) recommends you reading {}".format(data['name'], data['email'], post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(
				post.title, post_url, data['name'], data['comments']
			)
			send_mail(subject, message, data['email'], [data['to']])
			sent = True

	return render(
		request,
		'blog/post/share.html',
		{'post': post, 'form': form, 'sent': sent, 'data': data}
	)


def post_search(request):
	form = SearchForm()
	data = {}
	results = []
	total_results = None
	if 'query' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			data = form.cleaned_data
			results = PostDocument.search().filter("term", body=data['query'])
			total_results = results.count()
			# import pdb; pdb.set_trace()
	return render(
		request,
		'blog/post/search.html',
		{
			'form': form,
			'data': data,
			'results': results,
			'total_results': total_results
		}
	)
