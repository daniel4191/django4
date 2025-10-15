from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User

group_name = ""

class FollowersInline(admin.TabularInline):
    model = User.following.through
    fk_name = "from_user"
    verbose_name = "팔로우 중인 유저들"
    verbose_name_plural = f"{verbose_name} 목록"
    extra = 1
    
class FollowingInline(admin.TabularInline):
    model = User.following.through
    fk_name = "to_user"
    verbose_name = "나를 팔로우 하고 있는 사용자"
    verbose_name_plural = f"{verbose_name} 목록"
    extra = 1
    


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets =[
        (None, {"fields": ("username", "password")}),
        ("개인정보", {"fields": ("first_name", "last_name", "email")}),
        ("추가필드", {"fields": ("profile_image", "short_description")}),
        ("권한", {"fields": ("is_staff", "is_active", "is_superuser",)}),
        ("중요한 일정", {"fields": ("last_login", "date_joined")}),
        ("연관객체", {"fields":("like_posts",)})
    ]
    
    inlines =[
        FollowersInline,
        FollowingInline
    ]
