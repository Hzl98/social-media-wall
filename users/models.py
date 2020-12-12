from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from wall.models import *

# Create your models here.
class User_additional_info(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	is_premium = models.IntegerField(default=0)
	image = models.ImageField(upload_to='profile_pic', blank=True)

	def __str__(self):
		return str(self.user)

@receiver(post_save, sender=User)
def create_addInfo(sender, instance, created, **kwargs):
	if created:
		User_additional_info.objects.create(user=instance)

class Friends(models.Model):
	requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requester')
	target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target')
	status = models.IntegerField(default=0)

class Friend_request(models.Model):
	requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requester_r')
	requester_username = models.CharField(max_length=100)
	target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target_r')
	target_username = models.CharField(max_length=100)
	status = models.IntegerField(default=0)

class Friend_acc(models.Model):
	u1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requester_t')
	u1_username = models.CharField(max_length=100)
	u2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target_t')
	u2_username = models.CharField(max_length=100)

class logs(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	log_str = models.CharField(max_length=200)

# @receiver(post_save, sender=wall)
# def log_wall_creation(sender, instance, created, **kwargs):
# 	if created:
		