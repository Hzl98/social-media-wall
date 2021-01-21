from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegForm, AdditionalInfoForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.models import User
from .models import User_additional_info, Friends, Friend_request, Friend_acc
from django.http import JsonResponse, HttpResponse
from pprint import pprint
from django.core import serializers
from django.db import connection
from wall.models import wall
import json
import midtransclient
from random import randint

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# Create your views here.
def register(request):
	if request.method == 'POST':
		form = UserRegForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created')
			return redirect('wall-index')
	else:
		form = UserRegForm()
	return render(request, 'users/register.html', {'form': form})

def privacypolicy(request):
	return render(request, 'users/privacypolicy.html')

def UserProfilePage(request):
	current_user = request.user
	context = {
		'user_info' : User_additional_info.objects.get(user_id=current_user.id),
		'friend_reqs' : Friend_request.objects.filter(target=current_user.id).filter(status=0), # 0 = pending, 1 = acc 
		'friend_list' : Friend_acc.objects.filter(u1_id=current_user.id)
	}
	return render(request, 'users/profile.html', context)

def editProfilePage(request):
	current_user = request.user
	uploadform = AdditionalInfoForm(request.POST)
	context = {
		'user_info' : User_additional_info.objects.get(user_id=current_user.id),
		'form': uploadform
	}
	return render(request, 'users/edit.html')

def get_friends(request):
	friends = Friend_acc.objects.filter(u1_id = request.user.id)
	data = {
		'friends' : serializers.serialize('json', friends)
	}
	json_res = json.dumps(data)
	return HttpResponse(json_res, content_type="application/json")

def search_user(request):
	srckey = request.GET.get('srckey')
	srcres = User.objects.filter(username__icontains=srckey).exclude(username=request.user.username)
	data = serializers.serialize('json', srcres)
	return HttpResponse(data, content_type="application/json")

def add_user(request):
	target_id = request.GET.get('target_id')
	target_user = User.objects.get(id=target_id)
	target_username = target_user.username
	requester_id = request.user.id
	requester_username = request.user.username
	fr_inst = Friend_request.objects.create(
		requester = request.user, 
		requester_username = requester_username,
		target = target_user,
		target_username = target_username
	)
	fr_inst.save()
	data = {
		'msg' : 'Friend Request Sent'
	}
	return JsonResponse(data)

class friend_profile(DetailView):
	model = User
	template_name = 'users/user_profile.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		username = self.object.username
		context['walls'] = wall.objects.filter(owner = username).filter(visibility = 1)
		return context

def acc_user(request):
	request_id = request.GET.get('request_id')
	f_request = Friend_request.objects.get(id=request_id)
	requester_user = User.objects.get(id=f_request.requester_id)
	requester_username = requester_user.username
	inst = Friend_acc.objects.create(
		u1 = request.user,
		u1_username = request.user.username,
		u2 = requester_user,
		u2_username = requester_user.username,
	)
	inst.save()
	inst2 = Friend_acc.objects.create(
		u1 = requester_user,
		u1_username = requester_user.username,
		u2 = request.user,
		u2_username = request.user.username,
	)
	inst2.save()
	f_request.delete()
	friend_reqs = Friend_request.objects.filter(target=request.user.id).filter(status=0)
	friend_list = Friend_acc.objects.filter(u1_id=request.user.id)
	data = {
		'friend_reqs' : serializers.serialize('json', friend_reqs),
		'friend_list' : serializers.serialize('json', friend_list)
	}
	json_res = json.dumps(data)
	return HttpResponse(json_res, content_type="application/json")

def go_premium(request):
	snap = midtransclient.Snap(
		is_production = False,
		server_key = 'SB-Mid-server-ifu2sp7KVtoXPHj1gaFLePrs'
	)
	param = {
		"transaction_details": {
			"order_id": str(randint(100000, 999999)),
			"gross_amount": request.GET.get('amount')
		}, 
		"credit_card":{
			"secure" : True
		}, 
		"customer_details":{
			"first_name": request.user.first_name,
			"last_name": request.user.last_name,
			"email": request.user.email,
		}
	}
	transaction = snap.create_transaction(param)
	transaction_token = transaction['token']
	data = {
		'amount' : request.GET.get('amount'),
		'token' : transaction_token
	}
	json_res = json.dumps(data)
	return HttpResponse(json_res, content_type="application/json")

def change_premium_status(request):
	current_user = request.user
	premium_user = User_additional_info.objects.get(user_id=current_user.id)
	premium_user.is_premium = 1
	premium_user.save()
	data = {
		'msg' : 'Thanks for becoming a Premium Member',
	}
	json_res = json.dumps(data)
	return HttpResponse(json_res, content_type="application/json")