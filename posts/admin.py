from django.contrib import admin
from django.db import models
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.db.models import ManyToManyField
from django.forms import CheckboxSelectMultiple

import admin_thumbnails

from .models import Post, PostImage, Comment, HashTag

# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
@admin_thumbnails.thumbnail("photo")    
class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    
class InlineImageWidget(AdminFileWidget):
    def render(self, name, value, attrs = None, renderer = None):
        html = super().render(name, value, attrs, renderer)
        if value and getattr(value, "url", None):
            html = mark_safe(f'<img src="{value.url}" height="150">') + html
        return html

class LikeUserInline(admin.TabularInline):
    # Post 모델에 연결되어서 해당 작동을 사용하게되면 like_users폴더 안에 through폴더생성이 되어서 그 안에 내용이 담긴다.
    model = Post.like_users.through 
    
    verbose_name = "좋아요 한 User",
    verbose_name_plural = f"{verbose_name}목록"
    extra = 1
    
    def has_change_permission(self, request,obj=None):
        # 이 인라인 데이터는 수정불가라는 뜻
        return False
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "content",
    ]
    
    inlines = [
        CommentInline,
        PostImageInline,
        LikeUserInline
    ]
    
    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple},
    }
    

class PostImageAdmin(admin.ModelAdmin):
    model = PostImage
    extra = 1
    
@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = [
        "id",
        "post",
        "content"
    ]
    
@admin.register(HashTag)
class HashTagAdmin(admin.ModelAdmin):
    pass

