from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import ShortenedLink
from .forms import ShortenLinkForm
from random import sample
import string


# Create your views here.
def home(request):
    return render(request, 'shortener/home.html')


@login_required
def my_links(request):
    links = ShortenedLink.objects.filter(user=request.user)
    return render(request, 'shortener/my_links.html', {'links': links})


@login_required
def shorten(request):
    if request.method == 'GET':
        return render(request, 'shortener/url_shortener.html', {
            'form': ShortenLinkForm
        })
    else:
        special_name = request.POST['special_name']
        original_link = request.POST['original_link']

        if original_link == '':
            return render(request, 'shortener/url_shortener.html', {
                'form': ShortenLinkForm,
                'error': 'Enter a URL to shorten.',
            })
        elif ShortenedLink.objects.filter(original_link=original_link, user=request.user).count() != 0:
            return render(request, 'shortener/url_shortener.html', {
                'form': ShortenLinkForm,
                'error': 'Shortened URL already exists.',
                'new_link': ShortenedLink.objects.get(original_link=original_link, user=request.user).shortened_link
            })
        elif special_name == '':
            while True:
                extra = ''.join(sample(
                    string.ascii_lowercase, k=5))
                new_link = 'bla.ze/' + str(extra)
                if ShortenedLink.objects.filter(shortened_link=new_link, user=request.user).count() == 0:
                    break
            ShortenedLink.objects.create(
                user=request.user,
                original_link=original_link,
                shortened_link=new_link
            )
            return render(request, 'shortener/url_shortener.html', {
                'form': ShortenLinkForm,
                'new_link': new_link
            })
        else:
            new_link = 'bla.ze/' + special_name
            if ShortenedLink.objects.filter(shortened_link=new_link).count() != 0:
                return render(request, 'shortener/url_shortener.html', {
                    'form': ShortenLinkForm,
                    'error': 'Special name already exists. Try another one.'
                })
            ShortenedLink.objects.create(
                user=request.user,
                original_link=original_link,
                shortened_link=new_link
            )
            return render(request, 'shortener/url_shortener.html', {
                'form': ShortenLinkForm,
                'new_link': new_link
            })


@login_required
def delete(request, pk):
    ShortenedLink.objects.get(pk=pk).delete()
    return redirect('shortener:my_links')


@login_required
def goto(request):
    link = ShortenedLink.objects.get(shortened_link=request.GET['search'].strip(), user=request.user).original_link
    return redirect(link)


def check(request):
    if request.method == 'GET':
        return render(request, 'shortener/check_availability.html')
    else:
        pass


def signup_user(request):
    if request.method == 'GET':
        return render(request, 'shortener/signup_user.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'shortener/signup_user.html', {'form': UserCreationForm(), 'error': 'Username already exists.'})
        else:
            return render(request, 'shortener/signup_user.html', {'form': UserCreationForm(),'error': 'Passwords didn\'t match.'})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'shortener/login_user.html', {'form': AuthenticationForm()})
    else:
        user_exists = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user_exists:
            login(request, user_exists)
            return redirect('home')
        else:
            return render(request, 'shortener/login_user.html', {'form': AuthenticationForm(), 'error': 'User credentials invalid.'})


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
