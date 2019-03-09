from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class PublishedManager(models.Manager):

	def get_queryset(self):
		return super(PublishedManager, self).get_queryset().filter(status=Post.PUBLISHED)


class Post(models.Model):
	DRAFT = 'D'
	PUBLISHED = 'P'
	SUSPENDED = 'S'
	STATUS_CHOICES = (
		(DRAFT, 'Draft'),
		(PUBLISHED, 'Published'),
		(SUSPENDED, 'Suspended'),
	)

	title = models.CharField(max_length=255)
	slug = models.SlugField(max_length=255, unique_for_date='publish')
	author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=DRAFT)

	objects = models.Manager()
	published = PublishedManager()

	class Meta:
		ordering = ('-publish',)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse(
			'blog:post_detail',
			kwargs={
				'year': self.publish.year, 'month': self.publish.month,
				'day': self.publish.day, 'post': self.slug
			}
		)


class Comment(models.Model):
	post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
	name = models.CharField(max_length=80, blank=False)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ('created',)

	def __str__(self):
		return "by {} on {}".format(self.name, self.post)
