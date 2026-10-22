from django.contrib import admin
from .models import Task, SubTask, Category

# Встроенная форма для создания подзадач внутри задачи
class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1
# admin.TabularInline — показывает подзадачи в виде таблицы внутри формы задачи.
# model = SubTask — указывает, какую модель добавляем.
# extra = 1 — отображает одну пустую форму для новой подзадачи.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    def short_title(self, obj):
        if len(obj.title) > 10:
            return obj.title[:10] + "..."
        return obj.title

    short_title.short_description = 'Title'

    list_display = ('short_title', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'categories')
    ordering = ('-created_at',)

    inlines = [SubTaskInline]


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):

    actions = ["mark_as_done"]

    @admin.action(description="Mark selected tasks as Done")
    def mark_as_done(self, request, queryset):
        queryset.update(status='done')

    list_display = ('title', 'task', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'task')
    ordering = ('-created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

