from django.urls import path

from novel import views

app_name='novel'

urlpatterns= [
    path('', views.home,name='home'),
    path('novel_create/',views.novel_create,name='novel_create'),
    path('novels/',views.novel_list,name='novel_list'),
]


