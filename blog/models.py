from django.contrib.auth.models import User
from django.db import models
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
