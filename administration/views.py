from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from wall.models import wall, post
from django.views.generic import ListView, DetailView, CreateView, UpdateView

logged_in = False

# Create your views here.
def login(request):
	return render(request, 'administration/adminlogin.html')

def do_login(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	user = authenticate(username = username, password = password)
	if user is not None :
		if user.is_superuser == 1:
			return redirect('admin-dashboard')
		else : 
			data = {
				'msg' : 'You do not Have Access to this Page'
			}
			return render(request, 'administration/adminlogin.html', data)
	else :
		data = {
			'msg' : 'Wrong Username or Pass'
		}
		return render(request, 'administration/adminlogin.html', data)

def dashboard(request):
	context = {
		'users' : User.objects.all(),
		'walls' : wall.objects.all()
	}
	return render(request, 'administration/dashboard.html', context)

class user_details(DetailView):
	model = User
	template_name = 'administration/user_details.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = User.objects.get(pk = self.kwargs['pk'])
		context['walls'] = wall.objects.filter(owner = user.username)
		return context

class wall_details(DetailView):
	model = wall
	template_name = 'administration/wall_details.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['posts'] = post.objects.filter(pk = self.kwargs['pk'])
		return context

