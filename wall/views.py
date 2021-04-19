from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import wall, post, Sources, moderators
from users.models import User_additional_info, Friend_acc
from .forms import SourceForm, wallUpdateForm
from django.urls import reverse_lazy
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
import json
import pyrebase

# Create your views here.
def index(request):
	form = UserCreationForm()
	return render(request, 'wall/index.html', {'form': form})

class WallListView(ListView):
	model = wall
	template_name = 'wall/home.html'
	context_object_name = 'walls'

	def get_queryset(self):
		return wall.objects.filter(owner = self.request.user.username)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		walls_as_mod = moderators.objects.filter(username = self.request.user.username).values('wall')
		context['mod_walls'] = wall.objects.filter(pk__in = walls_as_mod)
		return context

class WallDetailView(DetailView):
	model = wall
	template_name = 'wall/walldetails.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['post_list'] = post.objects.filter(posted_on_id = self.object.id).filter(visibility = 1)
		return context
	
class WallCreateView(CreateView):
	model = wall
	fields = ['name']

	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super().form_valid(form)

class WallUpdateView(UpdateView):
	model = wall
	form_class = wallUpdateForm
	template_name = 'wall/wall_settings.html'

	def form_valid(self, form):
		form.instance.owner = self.request.user.username
		return super().form_valid(form)

def upload_logo(request, pk):
	config = {
			"apiKey" : "AIzaSyD1teLmwDHaJ4vWUPdI-QqywM4vsb9HVG4",
			"authDomain" : "nodejs-learning-b6d94.firebaseapp.com",
			"databaseURL" : "https://nodejs-learning-b6d94.firebaseio.com",
			"projectId" : "nodejs-learning-b6d94",
			"storageBucket" : "nodejs-learning-b6d94.appspot.com",
			"messagingSenderId" : "972133840846",
			"appId" : "1:972133840846:web:93dc363cb3084da8439d9f",
			"measurementId" : "G-YEJHCFK7SN"
		}
	firebase = pyrebase.initialize_app(config)
	storage = firebase.storage()
	file = request.FILES['logo']
	filename = request.FILES['logo'].name
	fileformat = filename[-4:]
	dest = "img/wall/" + str(pk) + fileformat
	upload_img = storage.child(dest).put(file)
	img_url = storage.child(dest).get_url(upload_img['downloadTokens'])
	wall_upload = wall.objects.get(pk = pk)
	wall_upload.logo = img_url
	wall_upload.save()
	return redirect('wall-details', pk = pk)

class SourceAddView(CreateView):
	model = Sources
	form_class = SourceForm
	template_name = 'wall/add_source.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['source_list'] = Sources.objects.filter(wall_id = self.kwargs['pk'])
		context['wall'] = wall.objects.get(pk = self.kwargs['pk'])
		return context

	def form_valid(self, form):
		form.instance.wall_id = self.kwargs['pk']
		return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy('source-add', kwargs={'pk' : self.kwargs['pk']})

class PostCreateView(CreateView):
	model = post
	fields = ['title', 'content']
	template_name = 'wall/post_create.html'

	def form_valid(self, form):
		form.instance.posted_on_id = self.kwargs['pk']
		return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy('post-list', kwargs={'pk' : self.kwargs['pk']})

class PostListView(ListView):
	model = post
	template_name = 'wall/post_list.html'
	context_object_name = 'posts'

	def get_queryset(self):
		return post.objects.filter(posted_on_id = self.kwargs['pk'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['wall'] = wall.objects.get(pk = self.kwargs['pk'])
		return context

def get_posts(request):
	wall = request.GET.get('wall')
	posts = post.objects.filter(posted_on_id = wall)
	data = {
		'posts' : serializers.serialize('json', posts),
	}
	json_res = json.dumps(data)
	return HttpResponse(json_res, content_type="application/json")

def get_posts_display(request):
	wall = request.GET.get('wall')
	posts = post.objects.filter(posted_on_id = wall).filter(visibility = 1)
	data = {
		'posts' : serializers.serialize('json', posts),
	}
	json_res = json.dumps(data)
	return HttpResponse(json_res, content_type="application/json")

def showPost(request, pk, returnpoint):
	selectedPost = post.objects.get(pk=pk)
	selectedPost.visibility = 1
	selectedPost.save()
	return redirect('post-list', pk=returnpoint)

def hidePost(request, pk, returnpoint):
	selectedPost = post.objects.get(pk=pk)
	selectedPost.visibility = 0
	selectedPost.save()
	return redirect('post-list', pk=returnpoint)

def p_show(request):
	post_id = request.GET.get('post')
	selectedPost = post.objects.get(pk=post_id)
	selectedPost.visibility = 1
	selectedPost.save()
	wall_id = selectedPost.posted_on_id
	posts = post.objects.filter(posted_on_id = wall_id)
	data = {
		'posts' : serializers.serialize('json', posts),
	}
	json_res = json.dumps(data)
	return HttpResponse(json_res, content_type="application/json")

def p_hide(request):
	post_id = request.GET.get('post')
	selectedPost = post.objects.get(pk=post_id)
	selectedPost.visibility = 0
	selectedPost.save()
	wall_id = selectedPost.posted_on_id
	posts = post.objects.filter(posted_on_id = wall_id)
	data = {
		'posts' : serializers.serialize('json', posts),
	}
	json_res = json.dumps(data)
	return HttpResponse(json_res, content_type="application/json")

def filter(request):
	plat = request.GET.get('plat')
	per = request.GET.get('per')
	wall_id = request.GET.get('wall')
	posts = post.objects.filter(posted_on_id = wall_id)
	if plat != "" :
		posts = posts.filter(platform = plat)
	if per == "This Year" :
		posts = posts.filter(date_posted__year = timezone.now().year)
	elif per == "This Month" :
		posts = posts.filter(date_posted__month = timezone.now().month)
	elif per == "This Week" :
		last_week = datetime.today() - timedelta(days=7)
		posts = posts.filter(date_posted__gte = last_week)
	data = {
		'posts' : serializers.serialize('json', posts),
	}
	json_res = json.dumps(data)
	return HttpResponse(json_res, content_type="application/json")

def check_premium_status(wall_id):
	wallobj = wall.objects.get(pk=wall_id)
	wall_owner = User.objects.get(username = wallobj.owner)
	owner_info = User_additional_info.objects.get(user = wall_owner)
	if owner_info.is_premium == 1:
		return True
	else:
		return False

class wall_display(ListView):
	model = post
	template_name = 'wall/wall_display.html'
	context_object_name = 'posts'

	def get_queryset(self):
		return post.objects.filter(posted_on_id = self.kwargs['pk'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['wall'] = wall.objects.get(pk = self.kwargs['pk'])
		context['premium_status'] = check_premium_status(context['wall'].id)
		return context

class mod_list(ListView):
	model = moderators
	template_name = 'wall/moderation.html'
	context_object_name = 'mods'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['friends'] = Friend_acc.objects.filter(u1_id = self.request.user.id)
		# context['friends'] = Friend_acc.objects.filter(u1 = self.request.user)
		context['wall'] = wall.objects.get(pk = self.kwargs['pk'])
		return context

def get_mods(request):
	wall = request.GET.get('wall')
	mods = moderators.objects.filter(wall = wall)
	data = {
		'mods' : serializers.serialize('json', mods)
	}
	json_res = json.dumps(data)
	return HttpResponse(json_res, content_type="application/json")

class reset(DetailView):
	model = wall
	template_name = "wall/wall_reset.html"
	context_object_name = 'wall'

class wall_chart(DetailView):
	model = wall
	template_name = "wall/wall_chart.html"
	context_object_name = 'wall'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['wall'] = wall.objects.get(pk = self.kwargs['pk'])
		context['tumblr'] = post.objects.filter(platform="Tumblr")
		context['twitter'] = post.objects.filter(platform="Twitter")
		return context

def wall_chart(request, pk):
	wall_get = wall.objects.get(pk = pk)
	qset_tw = post.objects.filter(posted_on = wall_get).filter(platform = "Twitter").count()
	qset_tu = post.objects.filter(posted_on = wall_get).filter(platform = "Tumblr").count()
	context = {
		'wall' : wall.objects.get(pk = pk),
		'tw_c' : qset_tw,
		'tu_c' : qset_tu
	}
	return render(request, 'wall/wall_chart.html', context)

def delete_all(request, pk):
	selectedWall = wall.objects.get(pk=pk)
	Sources.objects.filter(wall = selectedWall).delete()
	post.objects.filter(posted_on = selectedWall).delete()
	return redirect('wall-details', pk=pk)

class mod_PostListView(ListView):
	model = post
	template_name = 'wall/mod_post_list.html'
	context_object_name = 'posts'

	def get_queryset(self):
		return post.objects.filter(posted_on_id = self.kwargs['pk'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['wall'] = wall.objects.get(pk = self.kwargs['pk'])
		return context

def send_mod_invite(request):
	wall_id = request.GET.get('wall')
	wall_mod = wall.objects.get(pk = wall_id)
	mod_id = request.GET.get('mod_id')
	mod = User.objects.get(pk = mod_id)
	if moderators.objects.filter(wall = wall_id, user = mod_id).exists():
		data = {
			'msg' : 'This User is Already a Moderator',
			'type' : False
		}
	else:
		inst = moderators.objects.create(
			wall = wall_mod,
			user = mod_id,
			username = mod.username
		)
		inst.save()
		mods = moderators.objects.filter(wall = wall_id)
		friends = Friend_acc.objects.filter(u1_id = request.user.id)
		data = {
			'mods' : serializers.serialize('json', mods),
			'friends' : serializers.serialize('json', friends),
			'msg' : 'User Added as a Moderator',
			'type' : True
		}
	json_res = json.dumps(data)
	return HttpResponse(json_res, content_type="application/json")

def home(request):
	context = {
		'walls' : wall.objects.all()
	}
	return render(request, 'wall/home.html', context)

def createpage(request):
	return render(request, 'wall/createpage.html')