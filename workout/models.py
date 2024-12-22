from django.db import models


class WorkoutProgram(models.Model):
    trainer = models.ForeignKey(
        "user.TrainerUser", on_delete=models.PROTECT,
        related_name="trainer_workout_programs",
    )
    client = models.ForeignKey(
        "user.ClientUser", on_delete=models.CASCADE,
        related_name="client_workout_programs",
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=50)
    description = models.TextField()
    exercises = models.ManyToManyField(
        "exercise.Exercise",
        through="WorkoutExercise",
        related_name="workout_programs",
    )
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"program {self.name},pk {self.pk}, "
            f"complied by {self.trainer.username} "
        )

    class Meta:
        unique_together = ("client", "name")


class WorkoutExercise(models.Model):
    workout_program = models.ForeignKey(
        WorkoutProgram,
        on_delete=models.CASCADE,
    )
    exercise = models.ForeignKey(
        "exercise.Exercise",
        on_delete=models.CASCADE,
        related_name="workout_program"
    )
    repetitions = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="number of repetitions",
    )
    duration = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="execution time in seconds",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workout_program", "exercise"],
                name="unique_exercise_in_workout_program",
            ),
        ]


class WorkoutPlan(models.Model):
    client = models.ForeignKey(
        "user.ClientUser", on_delete=models.CASCADE,
        related_name="client_workout_plans",
    )
    name = models.CharField(max_length=20)
    description = models.TextField()
    workout_program = models.ForeignKey(
        WorkoutProgram,
        on_delete=models.PROTECT,
        related_name="workout_plans",
    )
    date_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return (
            f"workout plan {self.name},pk {self.pk}, "
            f"for {self.client.username} "
        )

    class Meta:
        unique_together = ("client", "name")
