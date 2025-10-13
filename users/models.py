from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    profile_image = models.ImageField(
        "프로필 이미지", upload_to="users/profile", blank=True
    )
    short_description = models.TextField(
        "소개글", blank=True
    )
    
    # 좋아요 기능
    like_posts = models.ManyToManyField(
        "posts.Post",
        verbose_name="내가 좋아요 누른 Post 목록",
        related_name="like_users", # 이건 역참조로 들어가서 posts폴더에 있는 Post 모델에 붙여주는 역할을 한다.
        blank=True
    )
    
    def __str__(self):
        return self.username