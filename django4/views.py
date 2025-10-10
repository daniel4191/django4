from django.shortcuts import render, redirect

def index(request):
    if request.user.is_authenticated:
        return redirect("posts:feeds")
    elif not request.user.is_authenticated:
        return redirect("users:login")