from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import Post
from .forms import CommentForm

# Create your views here.
def feeds(request):
    # 요청에 포함된 사용자가 로그인 하지 않은 경우
    if not request.user.is_authenticated:
        return redirect("/users/login/")
    
    # 모든 글 목록을 템플릿으로 전달
    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        "posts":posts,
        "comment_form": comment_form
        }
    return render(request, "posts/feeds.html", context)

@require_POST # 댓글 작성을 처리할 view, post 요청만 허용한다.
def comment_add(request):
    form = CommentForm(data = request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.save()
        
        print(comment.id)
        print(comment.content)
        print(comment.user)
        
        return redirect("/posts/feeds/")
    else:
        print(form.errors)
        print(request.POST)
    