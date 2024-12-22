from django.contrib import admin

from .models import Exercise, Category


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "category", "video",)
    search_fields = ("name", "category",)
    list_filter = ("category",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

