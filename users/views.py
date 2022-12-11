# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404
from forms import MyUserCreationForm,MyUserChangeForm,MailBoxForm
from django.core.mail import send_mail
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from users.models import MyUser, MailBox
from ond.functions import generate_form_errors,superuser
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models import Q


def create_user(request):

	if request.method == 'POST':
		form = MyUserCreationForm(request.POST)
		if form.is_valid():
			data = form.save(commit=False)
			data.is_active = False
			data.save()

			try:
				send_mail(
				    'New Registration',
				    'Click here for activating new account %s://%s/%s/%s' %(request.scheme,request.META.get('HTTP_HOST'),'verification',data.pk),
				    'from@example.com',
				    [data.email],
				    fail_silently=False,
				)
			except:
				data.delete()

				context = {
					'email': data.email,
					'title': 'Registration Failed'
				}
				return render(request,'users/registration_failed.html',context)

			context = {
				'email': data.email,
				'title': 'Registration Done'
			}
			return render(request,'users/registration_done.html',context)
		else:
			context = {
				'form': form,
				'title': 'Create User'
			}
	else:
		form = MyUserCreationForm()
		form.fields['region'].queryset = form.fields['region'].queryset.none()
		form.fields['city'].queryset = form.fields['city'].queryset.none()

		context = {
			'form':form,
			'title':'Create User',
			"url" : reverse('users:create_user'), 
		}
	return render(request,'users/create_user.html',context)


@login_required(login_url='/login')
def edit_user(request,pk):
	instance = get_object_or_404(MyUser,pk=pk)
	if (request.user == instance) or request.user.is_superuser :
		pass
	else:
		raise PermissionDenied

	if request.method == 'POST':
		form = MyUserChangeForm(request.POST,instance=instance)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('users:view_user', kwargs={'pk': instance.pk}))
		else:
			context ={
				'form':form,
				'title':'Edit User'
			}
	else:
		form = MyUserChangeForm(instance=instance)
		form.fields['region'].queryset = form.fields['region'].queryset.filter(country_id=instance.country.pk)
		form.fields['city'].queryset = form.fields['city'].queryset.filter(region_id=instance.region.pk)

		context = {
			'form':form,
			'title': 'Edit User'
		}
	return render(request,'users/edit_user.html',context)


@login_required(login_url='/login')
def view_user(request,pk):
	instance = get_object_or_404(MyUser,pk=pk)

	context = {
		'instance':instance,
		'title' :'View User'
	}
	return render(request,'users/view_user.html',context)


@login_required(login_url='/login')
@user_passes_test(superuser)
def view_users(request):
	instances = MyUser.objects.filter(is_superuser=False)

	query = request.GET.get('query')
	if query:
		instances = instances.filter(Q(id__contains=query)|Q(username__exact=query)|Q(name__exact=query)|
			Q(email__exact=query)|Q(phone__exact=query))

	context ={
		'title' : 'View Users',
		'instances': instances
	}
	return render(request,'users/view_users.html',context)


@user_passes_test(superuser)
def activate(request,pk):

	user = get_object_or_404(MyUser.objects.filter(pk=pk))
	if user.is_active == True:
		user.is_active = False
	else:
		user.is_active = True

	user.save()

	return HttpResponseRedirect(reverse('users:view_users'))


def verification(request,pk):
	MyUser.objects.filter(pk=pk).update(is_active=True)
	context ={
		'title':'Email Confirmation'
	}
	return render(request,'registration/email_verification.html',context)


def create_mail(request,pk,ad_id):

	to = get_object_or_404(MyUser,pk=pk)
	if request.method == 'POST':
		form = MailBoxForm(request.POST)
		if form.is_valid():
			data = form.save(commit=False)
			if request.user.is_authenticated:
				data.creator = request.user
			data.to = to
			data.ad_id = ad_id
			data.save()

			form = MailBoxForm()
			context ={
				'form': form,
				'message': 'Message sent Successfully',
				'title': 'Create Mail',
			}
		else:
			context = {
				'form':form,
				'title':'Create Mail',
			}
	else:
		form = MailBoxForm()
		context = {
			'form':form,
			'title':'Create mail',
		}
	return render(request,'users/create_mail.html',context)


@login_required(login_url='/login')
def sent_mail(request):
	instances = MailBox.objects.filter(creator=request.user.pk,sentitems_deleted=False)
	inboxes = MailBox.objects.filter(to=request.user,inbox_deleted=False).count()
	sent_items = MailBox.objects.filter(creator=request.user,sentitems_deleted=False).count()
	context = {
		'instances':instances,
		'title':'Send Mail',
		'inboxes':inboxes,
		'sent_items':sent_items
	}
	return render(request,'users/send_mail.html',context)


@login_required(login_url='/login')
def received_mail(request):
	instances = MailBox.objects.filter(to=request.user.pk,inbox_deleted=False)
	inboxes = MailBox.objects.filter(to=request.user,inbox_deleted=False).count()
	sent_items = MailBox.objects.filter(creator=request.user,sentitems_deleted=False).count()
	context = {
		'instances':instances,
		'title':'Received Mail',
		'inboxes':inboxes,
		'sent_items':sent_items
	}
	return render(request,'users/received_mail.html',context)


@login_required(login_url='/login')
def inbox_deleted(request,pk):
	instance = MailBox.objects.filter(pk=pk).update(inbox_deleted=True)
	if (request.user == instance.user):
		pass
	else:
		raise PermissionDenied
	return HttpResponseRedirect(reverse('users:received_mail'))


@login_required(login_url='/login')
def sentitems_deleted(request,pk):
	instance = MailBox.objects.filter(pk=pk).update(sentitems_deleted=True)
	if (request.user == instance.user):
		pass
	else:
		raise PermissionDenied
	return HttpResponseRedirect(reverse('users:sent_mail'))


def ruels(request):
	context ={
		'title': 'Ruels of Use'
	}
	return render(request,'users/ruels.html',context)


def terms(request):
	context ={
		'title': 'Terms and Conditions'
	}
	return render(request,'users/terms.html',context)