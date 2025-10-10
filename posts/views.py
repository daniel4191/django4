from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse

from .models import Post, Comment, PostImage
from .forms import CommentForm, PostForm

# Create your views here.
def feeds(request):
    # 요청에 포함된 사용자가 로그인 하지 않은 경우
    if not request.user.is_authenticated:
        return redirect("users:login")
    
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
        
        url = reverse("posts:feeds")+f"#post-{comment.post.id}"
        return HttpResponseRedirect(url)
    
@require_POST
def comment_delete(request, comment_id):
    if request.method == "POST":
        comment = Comment.objects.get(id = comment_id)
        if comment.user == request.user:
            comment.delete()
            url = reverse("posts:feeds") + f"#post-{comment.post.id}"
            return HttpResponseRedirect(url)
        else:
            return HttpResponseForbidden("이 댓글을 삭제할 권한이 없습니다.")
        
def post_add(request):
    if request.method == "POST":
        form = PostForm(data = request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            
            for image_file in request.FILES.getlist("images"):
                PostImage.objects.create(
                    post = post,
                    photo = image_file
                )
        
        url = reverse("posts:feeds") + f"#post-{post.id}"
        return HttpResponseRedirect(url)
    
    else:
        form = PostForm()
    context = {"form": form}
    return render(request, "posts/post_add.html", context)