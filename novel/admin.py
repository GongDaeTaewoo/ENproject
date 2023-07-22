from django.contrib import admin

from novel.models import Novel


@admin.register(Novel)
class NovelAdmin(admin.ModelAdmin):
    pass
