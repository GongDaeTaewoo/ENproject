from django.db import models


class NovelInf(models.Model):
    char_name1 = models.CharField(max_length=15, blank=True)
    char_name2 = models.CharField(max_length=15, blank=True)

    char_age1 = models.IntegerField(blank=True)
    char_age2 = models.IntegerField(blank=True)

    char_per1 = models.CharField(max_length=100, blank=True)
    char_per2 = models.CharField(max_length=100, blank=True)

    gender_choices = (('남성', '남성'), ('여성', '여성'), ('등장시키지 않음', '등장시키지 않음'))
    char_sex1 = models.CharField(max_length=8, choices=gender_choices, blank=True)
    char_sex2 = models.CharField(max_length=8, choices=gender_choices, blank=True)

    genre_choices = (('로맨스', '로맨스'), ('판타지', '판타지'), ('고전', '고전'), ('공상과학', '공상과학'), ('일상', '일상'), ('공포', '공포'))
    genre = models.CharField(max_length=10, choices=genre_choices, blank=True)

    story = models.TextField(max_length=150, blank=False)

class Novel(models.Model):

    answer_text = models.TextField(max_length=5000)
    novel_infor = models.ForeignKey(NovelInf, on_delete=models.CASCADE)
