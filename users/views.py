from django.shortcuts import render, redirect
# 주어진 값에 해당하는 자가 있는지 확인
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect("/posts/feeds/")
    
    if request.method == "POST":
        form = LoginForm(data = request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            
            user = authenticate(username = username, password = password)
        
            if user:
                login(request, user)
                return redirect("/posts/feeds/")
            
            else:
                form.add_error(None, "에러입니다.")
        
        context = {"form": form}
        return render(request, "users/login.html", context)
            
    
    else:
        form = LoginForm()
        context= {"form": form}
        return render(request, "users/login.html", context)
    
def logout_view(request):
    logout(request)
    return redirect("/users/login/")