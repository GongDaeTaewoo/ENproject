from django.contrib.auth.views import LogoutView
from django.urls import path

from novel import views
from novel.views import MyLoginView
from openaidjango.settings import LOGIN_URL

app_name='novel'

urlpatterns= [
    path('', views.home,name='home'),
    path('novel_create/',views.novel_create,name='novel_create'),
    path('novels/',views.novel_list,name='novel_list'),
    path('novels/<int:pk>/',views.novel_detail,name='novel_detail'),
    path('novels/<int:pk>/recommend/',views.recommend,name='recommend'),
    path('register/',views.register,name='register'),
    path('login/',MyLoginView.as_view(next_page='/profile/'),name='login'),
    path('logout/',LogoutView.as_view(next_page=LOGIN_URL),name='logout'),
    path('profile/',views.mypage,name='mypage'),
]


