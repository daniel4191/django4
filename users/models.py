from django.db import models
from django.contrib.auth.models import AbstractUser

class Relationships(models.Model):
    from_user = models.ForeignKey(
        "users.User",
        verbose_name="팔로우 요청한 유저",
        related_name="following_relationships",
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        "users.User",
        verbose_name="팔로우 요청의 대상",
        related_name="follower_relationships",
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"관계 ({self.from_user} -> ({self.to_user}))"
    
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
    
    following = models.ManyToManyField(
        "self",
        verbose_name="팔로우 중인 유저들",
        related_name="followers",
        symmetrical=False,
        through = "users.Relationships"
    )
    
    def __str__(self):
        return self.username
    
