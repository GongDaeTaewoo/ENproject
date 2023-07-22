from django import forms

from novel.models import NovelInf


class NovelInfForm(forms.ModelForm):
    class Meta:
        model = NovelInf
        fields = '__all__'
        widgets = {
            'story':forms.Textarea(
                attrs={
                    "class":"form-control"

                }
            )
        }
        labels = {
            "char_name1":"등장인물1 이름"
            ,"char_name2":"등장인물2 이름",
            "char_age1":"등장인물1 나이",
            "char_age2": "등장인물2 나이",
            "char_sex1": "등장인물1 성별",
            "char_sex2": "등장인물2 성별",
            "char_per1": "등장인물1 성격",
            "char_per2":"등장인물2 성격",
            "genre":"장르",
            "story":"스토리(필수입력)",

        }