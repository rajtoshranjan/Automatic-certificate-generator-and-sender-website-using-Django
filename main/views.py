from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import random, string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def index(request):
	
	# print(request.scheme+"://"+request.get_host()+reverse('password_reset'))
	return render(request, 'main/index.html', {'title': "Home"})

@login_required	
def create_user(request):
	if not request.user.is_superuser:
		return redirect("home")

	if request.method == "POST":
		fname = request.POST.get('fname')
		lname = request.POST.get('lname')
		email = request.POST.get('email')
		admin = request.POST.get('admin')
		letters = string.ascii_letters
		passwd = ''.join(random.choice(letters) for letter in range(12))
		user = User.objects.create_user(email, email, passwd)
		user.first_name = fname
		user.last_name = lname
		if admin != None:
			user.is_superuser = True
			user.is_staff = True
		user.save()
		messages.success(request, 'Account for user {} has been created'.format(email))
		send_mail("Your Account has been Created at ISM", 
			f"Hello {fname} {lname} \nYour Account has been Created at ISM patna certificate generator site. you have to set your password. \n \
			\nSteps for reset you password:-\n1) Open {request.scheme}://{request.get_host()+reverse('password_reset')}\
			\n2) Enter your email and press reset button. \n3) Open the email send by us and click the link. \
			\n4) Set your strong password. \nNow You Done you can login into your account by email as username and your password\
			\nRemember your email is your username at this site\nThanks and Regards!", 
			settings.EMAIL_HOST_USER,
			[email],
			fail_silently = False)


	return render(request, 'admin/create_user.html', {
		'title': "User Registration"
		})


@login_required	
def view_users(request):
	if not request.user.is_superuser:
		return redirect("home")
	if request.method == "POST":
		username = request.POST.get('username')
		user = get_object_or_404(User, username = username)
		fname = user.first_name
		lname = user.last_name
		email = user.email
		send_mail("Your Account had been deleted", 
			f"Hello {fname} {lname} \nYour Account has been deleted form ISM patna certificate generator website by {request.user.first_name} {request.user.last_name}\nThanks and Regards!", 
			settings.EMAIL_HOST_USER,
			[email],
			fail_silently = False)

		user.delete()
		messages.success(request, 'User {} has been deleted successfully'.format(username))

	return render(request, 'admin/view_users.html', {
		'users': User.objects.all(),
		'title': "Users"
		})

@login_required	
def edit_user(request, username):
	if not request.user.is_superuser:
		return redirect("home")

	if request.method == "POST":
		fname = request.POST.get('fname')
		lname = request.POST.get('lname')
		email = request.POST.get('email')
		admin = request.POST.get('admin')
		
		user = User.objects.get(username=email)
		user.first_name = fname
		user.last_name = lname
		if admin != None:
			user.is_superuser = True
			user.is_staff = True
		else:
			user.is_superuser = False
			user.is_staff = False
		user.save()
		send_mail(f"Your Account had been edited ", 
			f"Hello {fname} {lname} \nYour Account had been edited by {request.user.first_name} {request.user.last_name}\nThanks and Regards!", 
			settings.EMAIL_HOST_USER,
			[email],
			fail_silently = False)

		return redirect('view_users')

	return render(request, 'admin/edit_user.html', {
		'user': User.objects.get(username=username),
		'title': "Edit User",
		})

@login_required
def change_password(request):
	if request.method == 'POST':
		passChangeForm = PasswordChangeForm(request.user, request.POST)
		if passChangeForm.is_valid():
			passChangeForm.save()
			messages.success(request, f'Password had been changed successfully')
	else:
		passChangeForm = PasswordChangeForm(request.user)

	return render(request, "change_password.html",{'form': passChangeForm, 'title': "Change Password"})