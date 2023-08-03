import urllib
import urllib.request as r
from pathlib import Path

import environ

from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect

from novel.forms import NovelInfForm, MyUserCreationForm, CommentForm
from novel.models import Novel, NovelInf, MyUser, Comment
import openai
import os
import sys

# api key숨기기
from openaidjango.settings import env

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)
# openai api key
openai.api_key = env('OPENAI')


def home(request):
    try:
        num = Novel.objects.all().count()
    except:
        num = 0
    return render(request, 'novel/home.html', {'num': num})


def novel_create(request):
    if request.method == "POST":
        novel_form = NovelInfForm(request.POST)
        if novel_form.is_valid():
            novel = NovelInf(**novel_form.cleaned_data)
            # 소설 메세지 준비
            if novel.char_sex1 == '등장시키지 않음' and novel.char_sex2 != '등장시키지 않음':
                messages = [{
                    "role": "user",
                    "content": "소설 하나를 재밌게 써줘.  줄거리를 알려줄게 줄거리: " + novel.story
                               + " 장르는 " + novel.genre + " 등장인물을 알려줄게 " + "등장인물1의 이름: " + novel.char_name2 +
                               " 등장인물1의 성격: " + novel.char_per2 + " 등장인물1의 성별: " + novel.char_sex2 + " 등장인물1의 나이: " + str(
                        novel.char_age2)
                }]
            elif novel.char_sex2 == '등장시키지 않음' and novel.char_sex1 != '등장시키지 않음':
                messages = [{
                    "role": "user",
                    "content": "소설 하나를 재밌게 써줘. 줄거리를 알려줄게 줄거리:" + novel.story
                               + " 장르는 " + novel.genre + " 등장인물을 알려줄게" + "등장인물1의 이름: " + novel.char_name1 +
                               " 등장인물1의 성격: " + novel.char_per1 + " 등장인물1의 성별: " + novel.char_sex1 + " 등장인물1의 나이: " + str(
                        novel.char_age1)
                }]
            elif novel.char_sex2 == '등장시키지 않음' and novel.char_sex1 == '등장시키지 않음':
                messages = [{
                    "role": "user",
                    "content": "소설 하나를 재밌게 써줘. 줄거리를 알려줄게 줄거리:" + novel.story
                               + " 장르는 " + novel.genre + " 이야 "
                }]
            else:
                messages = [
                    {
                        "role": "user",
                        "content": "소설 하나를 재밌게 써줘. 줄거리를 알려줄게 줄거리:" + novel.story
                                   + " 장르는 " + novel.genre + " 등장인물을 알려줄게 " + "등장인물1의 이름 :" + novel.char_name1 +
                                   " 등장인물1의 성격:" + novel.char_per1 + " 등장인물1의 성별: " + novel.char_sex1 + " 등장인물1의 나이: " + str(
                            novel.char_age1) + " 등장인물2의 이름 " + novel.char_name2 +
                                   " 등장인물2의 성격: " + novel.char_per2 + " 등장인물2의 성별: " + novel.char_sex2 + " 등장인물1의나이 " + str(
                            novel.char_age2)
                    }]
                # 소설생성 api
            airesponse = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=messages
            ).choices[0].message.content
            novel = Novel()
            novel.answer_text = airesponse
            novel_inf = novel_form.save(commit=True)
            novel.novel_infor = novel_inf

            # 파파고 api
            client_id = env('CLIENT_ID')  # 개발자센터에서 발급받은 Client ID 값
            client_secret = env('CLIENT_SECRET')  # 개발자센터에서 발급받은 Client Secret 값

            encText = urllib.parse.quote(novel.novel_infor.story)
            data = "source=ko&target=en&text=" + encText
            url = "https://openapi.naver.com/v1/papago/n2mt"
            Papagorequest = r.Request(url)
            Papagorequest.add_header("X-Naver-Client-Id", client_id)
            Papagorequest.add_header("X-Naver-Client-Secret", client_secret)
            response = r.urlopen(Papagorequest, data=data.encode("utf-8"))
            rescode = response.getcode()
            if (rescode == 200):
                response_body = response.read()
                prompt_story = response_body.decode('utf-8')
            else:
                print("Error Code:" + rescode)
            # 이미지 생성 api
            image_ai_response = openai.Image.create(
                prompt=prompt_story,
                n=2,
                size="512x512"
            )
            image_url = image_ai_response['data'][0]['url']
            image_url2 = image_ai_response['data'][1]['url']

            if request.user.is_authenticated:
                novel.user = request.user

            novel.save()

            test = r.urlretrieve(image_url, "openaidjango/static/image/" + str(novel.id) + ".jpg")
            test2 = r.urlretrieve(image_url2, "openaidjango/static/image/" + str(novel.id) + "second.jpg")
            novel.image = str(novel.id) + ".jpg"
            novel.image2 = str(novel.id) + "second.jpg"
            novel.save()
    else:
        novel_form = NovelInfForm()
        novel = Novel()
        novel.answer_text = '입력 대기중 또는 로딩중(몇분정도의 시간이 소요될수 있습니다.)'
        prompt_story = ""
    return render(request, 'novel/novel_create.html', {'answer': novel, 'form': novel_form, 'story_e': prompt_story})


def novel_list(request):
    novels = Novel.objects.all().order_by('pk')

    context = {'novels': novels}
    return render(request, 'novel/novel_list.html', context)


def novel_detail(request, pk):
    novel = get_object_or_404(Novel, pk=pk)

    comments = Comment.objects.all().order_by('-pub_date').filter(novel=novel)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if request.user.is_authenticated:
                comment.author = request.user
            comment.novel = novel
            novel.comment_num += 1
            comment.save()
            novel.save()
            blank_form = CommentForm()
            context = {'novel': novel, 'form': blank_form, 'comments': comments}

    else:
        form = CommentForm()
        context = {'novel': novel, 'form': form, 'comments': comments}

    return render(request, 'novel/novel_detail.html', context)


def recommend(request, pk):
    novel = get_object_or_404(Novel, pk=pk)
    novel.recommend += 1
    novel.save()
    return render(request, 'novel/novel_detail.html', {'novel': novel})


def register(request):
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            login(request, user)
            return redirect('novel:home')
    else:
        form = MyUserCreationForm()
    return render(request, 'novel/register.html', {'form': form})


class MyLoginView(LoginView):
    template_name = "novel/login.html"


@login_required
def mypage(request):
    my_novel = Novel.objects.all().filter(user=request.user)
    return render(request, 'novel/mypage.html', {"my_novel": my_novel})
