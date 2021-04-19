from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class wall(models.Model):
	name = models.CharField(max_length=100)
	date_posted = models.DateField(default=timezone.now)
	owner = models.CharField(max_length=100, default='')
	visibility_choices = [(1, 'Public'), (2, 'Private')]
	visibility = models.IntegerField(default=1, choices=visibility_choices)
	design_choices = [(1, 'Grid'), (2, 'Carousel')]
	design = models.IntegerField(default=1, choices=design_choices)
	logo = models.CharField(max_length=1000, default="")

	def get_absolute_url(self):
		return reverse('wall-details', kwargs={'pk' : self.pk})

class post(models.Model):
	title = models.CharField(max_length=100, default="")
	date_posted = models.DateField(default=timezone.now)
	content = models.CharField(max_length=300)
	posted_on = models.ForeignKey(wall, on_delete=models.CASCADE)
	visibility = models.IntegerField(default=1)
	author = models.CharField(default="", max_length=20)
	platform = models.CharField(default="", max_length=20)

class Sources(models.Model):
	source_choices = [('Twitter', 'Twitter'), ('Tumblr', 'Tumblr')]
	source = models.CharField(max_length=15, choices=source_choices)
	wall = models.ForeignKey(wall, on_delete=models.CASCADE)
	tag = models.CharField(max_length=100)
	last_id = models.BigIntegerField(default = 0)

class moderators(models.Model):
	wall = models.ForeignKey(wall, on_delete=models.CASCADE)
	user = models.CharField(max_length=100, default='')
	username = models.CharField(max_length=100, default='')
	status = models.IntegerField(default = 0)

	# def get_absolute_url(self):
	# 	return reverse('wall-details', kwargs={'pk' : self.pk})