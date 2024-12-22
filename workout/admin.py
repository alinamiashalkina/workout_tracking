from django.contrib import admin

from .models import WorkoutProgram, WorkoutPlan, WorkoutExercise


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "name",
        "description",
        "date_time",
        "is_completed",
    )
    search_fields = ("name",)
    list_filter = ("client", "is_completed",)


class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 3


@admin.register(WorkoutProgram)
class WorkoutProgramAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "trainer",
        "client",
        "is_public",
    )
    search_fields = ("name",)
    list_filter = ("trainer", "client", "is_public",)
    inlines = [WorkoutExerciseInline]
