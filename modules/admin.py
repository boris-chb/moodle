from django.contrib import admin
from .models import Module, Topic

class TopicInline(admin.StackedInline):
    model = Topic
    extra = 1

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'instructor']
    list_filter = ['created', 'instructor']
    search_fields = ['title', 'overview', 'instructor']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TopicInline]