import json, datetime
from datetime import datetime

from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate as auth_authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.conf import settings
from django import template
from django.template.loader import get_template 
from django.core.urlresolvers import reverse

from models import Student

def create_user(request):
	
	context = RequestContext(request)

	if all((x in request.POST for x in ['email', 'password'])):

		if User.objects.filter(email=request.POST['email']).count() > 0:
			print 'User Already Exists'
			template = get_template('login.html')
			return HttpResponse(template.render(context))

		else:
			#Username isn't important for this system so we'll just use the email. Less stuff for the user to fill out
			user = User.objects.create_user(request.POST['email'], request.POST['email'], request.POST['password'])
			user.save()

			user = auth_authenticate(username=request.POST['email'], password=request.POST['password'])
			
			student = Student(user=user)
			student.save()

			auth_login(request, user)

			# student = Student(user=user)
			# student.save()

			# msg = EmailMultiAlternatives("<<Subject Line>>", "", "sender-email", [user.email])
			# msg.attach_alternative(render_to_string("<<Link to HTML representation of email contents>>.html"), "text/html")
			# msg.send()

			context = RequestContext(request)
			template = get_template('dashboard.html')

			return HttpResponse(template.render(context))

	else:
		print "Need to add some shit here to handle missing form fields"
		return HttpResponseRedirect(reverse('dashboard'))

def dashboard(request):

	context = RequestContext(request)

	if not request.user.is_authenticated():
		template = get_template('login.html')
		return HttpResponse(template.render(context))

	template = get_template('dashboard.html')
	return HttpResponse(template.render(context))


def login(request):

	context = RequestContext(request)

	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('dashboard'))

	elif all((x in request.POST for x in ['email', 'password'])):
		email = request.POST['email']
		password = request.POST['password']
		user = auth_authenticate(username=email, password=password)
		auth_login(request, user)
		return HttpResponseRedirect(reverse('dashboard'))
	else:
		template = get_template('dashboard.html')
		return HttpResponse(template.render(context))

		

def logout(request):
	'''
	Logs a user out from the system and returns them to the homepage.
	'''

	context = RequestContext(request)
	auth.logout(request)
	template = get_template('login.html')
	return HttpResponse(template.render(context))
