from django.contrib import admin

from novel.models import Novel, MyUser, NovelInf


@admin.register(Novel)
class NovelAdmin(admin.ModelAdmin):
    pass
@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    pass
@admin.register(NovelInf)
class NovelInfAdmin(admin.ModelAdmin):
    pass