from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


#...custom manager ......#
class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
	STATUS_CHOICES = (('draft', 'Draft'),('published', 'Published'),)
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250,unique_for_date='publish')
	author = models.ForeignKey(User,
	on_delete=models.CASCADE,
	related_name='blog_posts')
	body = RichTextField(blank=True, null=True)
	#body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10,choices = STATUS_CHOICES, default='published')
	objects = models.Manager() # The default manager.
	published = PublishedManager() # Our custom manager.
	tags = TaggableManager()

	def get_absolute_url(self):
		return reverse('blog:post_detail',args=[self.publish.year,self.publish.month,self.publish.day, self.slug])

	def get_absolute_url_edit(self):
		return reverse('blog:post_edit',args=[self.publish.year,self.publish.month,self.publish.day, self.slug])

	def get_absolute_url_delete(self):
		return reverse('blog:post_delete',args=[self.publish.year,self.publish.month,self.publish.day, self.slug])

class Meta:
	ordering = ('-publish',)
	

def __str__(self):
 	return self.title

class Comment(models.Model):
	post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ('-created',)
	def __str__(self):
		return f'Comment by {self.name} on {self.post}'
