from django.contrib import admin
from .models import *

# Register your models here.



admin.site.register(Flashcard)
admin.site.register(QuestionAnswer)
# admin.site.register(Chapter)

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['id','flash','name']

admin.site.register(SaveAnswer)
# @admin.register(ResearchTopic)
# class ResearchTopicAdmin(admin.ModelAdmin):
#     list_display = ['id','description']

# admin.site.register(Timer)
@admin.register(Timer)
class TimerAdmin(admin.ModelAdmin):
    list_display = ['id','question','user','timer','answer','date','time_start']
