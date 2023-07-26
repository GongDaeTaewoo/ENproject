from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class NovelInf(models.Model):
    char_name1 = models.CharField(max_length=15, blank=True,default='',null=True)
    char_name2 = models.CharField(max_length=15, blank=True, default='',null=True)

    char_age1 = models.IntegerField(blank=True, default=0,null=True)
    char_age2 = models.IntegerField(blank=True, default=0,null=True)

    char_per1 = models.CharField(max_length=100, blank=True, default='',null=True)
    char_per2 = models.CharField(max_length=100, blank=True, default='',null=True)

    gender_choices = (('남성', '남성'), ('여성', '여성'), ('등장시키지 않음', '등장시키지 않음'))
    char_sex1 = models.CharField(max_length=8, choices=gender_choices, blank=True,default='남자')
    char_sex2 = models.CharField(max_length=8, choices=gender_choices, blank=True,default='남자')

    genre_choices = (('로맨스', '로맨스'), ('판타지', '판타지'), ('고전', '고전'), ('공상과학', '공상과학'), ('일상', '일상'), ('공포', '공포'))
    genre = models.CharField(max_length=10, choices=genre_choices, blank=True)

    story = models.TextField(max_length=150, blank=False)
class MyUser(AbstractUser):
    nickname = models.CharField(max_length=10)

class Novel(models.Model):

    answer_text = models.TextField(max_length=5000)
    novel_infor = models.OneToOneField(NovelInf, on_delete=models.CASCADE)
    recommend = models.IntegerField(default=0)
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    comment_num = models.IntegerField(default=0)
    image = models.ImageField(blank=True,null=True)
    image2 = models.ImageField(blank=True,null=True)
    image3 = models.ImageField(blank=True, null=True)

class Comment(models.Model):
    author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,blank=True,null=True)
    novel = models.ForeignKey(Novel,on_delete=models.CASCADE)
    content = models.TextField(max_length=250)
    pub_date = models.DateTimeField(auto_now_add=True)
    changed_date = models.DateTimeField(auto_now=True)