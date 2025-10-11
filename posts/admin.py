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
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "content"
    ]
    
    inlines = [
        CommentInline,
        PostImageInline
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
