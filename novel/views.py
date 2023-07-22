from django.shortcuts import render

from novel.forms import NovelInfForm
from novel.models import Novel, NovelInf
import openai

openai.api_key = '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'


def home(request):
    num = Novel.objects.all().count()
    return render(request, 'novel/home.html', {'num': num})


def novel_create(request):
    if request.method == "POST":
        novel_form = NovelInfForm(request.POST)
        if novel_form.is_valid():
            novel = NovelInf(**novel_form.cleaned_data)
            if novel.char_sex1 == '등장시키지 않음':
                messages = [{
                    "role": "user",
                    "content": "소설 하나를 재밌게 써줘. 줄거리를 알려줄게 줄거리: " + novel.story
                               + " 장르는 " + novel.genre + " 등장인물을 알려줄게 " + "등장인물1의 이름: " + novel.char_name2 +
                               " 등장인물1의 성격: " + novel.char_per2 + " 등장인물1의 성별: " + novel.char_sex2 + " 등장인물1의 나이: " + str(novel.char_age2)
                }]
            elif novel.char_sex2 == '등장시키지 않음':
                messages = [{
                    "role": "user",
                    "content": "소설 하나를 재밌게 써줘. 줄거리를 알려줄게 줄거리:" + novel.story
                               + " 장르는 " + novel.genre + " 등장인물을 알려줄게" + "등장인물1의 이름: " + novel.char_name1 +
                               " 등장인물1의 성격: " + novel.char_per1 + " 등장인물1의 성별: " + novel.char_sex1 + " 등장인물1의 나이: " + str(novel.char_age1)
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
                        "content": "소설 하나를 재밌게 써줘. 줄거리를 알려줄게 줄거리:" +novel.story
                                   +" 장르는 " + novel.genre + " 등장인물을 알려줄게 " + "등장인물1의 이름 :" + novel.char_name1 +
                                   " 등장인물1의 성격:" + novel.char_per1 + " 등장인물1의 성별: " + novel.char_sex1 + " 등장인물1의 나이: " + str(novel.char_age1) + " 등장인물2의 이름 " + novel.char_name2 +
                                   " 등장인물2의 성격: " + novel.char_per2 + " 등장인물2의 성별: " + novel.char_sex2 + " 등장인물1의나이 " + str(novel.char_age2)
                    }]
            airesponse = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=messages
            ).choices[0].message.content
            novel = Novel()
            novel.answer_text = airesponse
            novel_inf = novel_form.save(commit=True)
            novel.novel_infor = novel_inf
            novel.save()


    else:
        novel_form = NovelInfForm()
        novel = Novel()
        novel.answer_text = '입력 대기중 또는 로딩중(몇분정도의 시간이 소요될수 있습니다.)'
    return render(request, 'novel/novel_create.html', {'answer': novel, 'form': novel_form})


def novel_list(request):
    novels = Novel.objects.all().order_by('pk')
    context = {'novels': novels}
    return render(request, 'novel/novel_list.html', context)
