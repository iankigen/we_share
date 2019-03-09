from django.contrib import admin
from .models import Comment, Post


class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug', 'author', 'publish', 'status')
	list_filter = ('status', 'created', 'publish', 'author')
	search_fields = ('title', 'slug')
	prepopulated_fields = {'slug': ('title',)}
	raw_id_fields = ('author',)
	date_hierarchy = 'publish'
	ordering = ('status', 'publish')


class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'post', 'created', 'active')
	list_filter = ('created', 'active', 'updated')
	search_fields = ('name', 'email', 'post', 'body')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
