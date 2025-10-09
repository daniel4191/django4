from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            # "user", # 이게 있게되면 유효성 검사시, Comment에서 user가 나오지 않기때문에 무조건 에러
            "post",
            "content",
        ]
        
        widget = {
            "content": forms.Textarea(
                attrs={"placeholder": "댓글 달기...",}
            )
        }