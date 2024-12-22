from rest_framework import serializers

from .models import WorkoutProgram, WorkoutExercise, WorkoutPlan
from exercise.serializers import ExerciseSerializer


class WorkoutProgramSerializer(serializers.ModelSerializer):

    exercises = serializers.ReadOnlyField(source="exercise.name")

    class Meta:
        model = WorkoutProgram
        fields = (
            "pk",
            "trainer",
            "client",
            "name",
            "description",
            "exercises",
            "is_public"
        )


class WorkoutExerciseSerializer(serializers.ModelSerializer):

    exercise = ExerciseSerializer()

    class Meta:
        model = WorkoutExercise
        fields = (
            "pk",
            "workout_program",
            "exercise",
            "repetitions",
            "duration",
        )


class WorkoutProgramWithExerciseSerializer(serializers.ModelSerializer):

    exercises = WorkoutExerciseSerializer(
        many=True,
        source="workoutexercise_set"
    )

    class Meta:
        model = WorkoutProgram
        fields = (
            "pk",
            "trainer",
            "client",
            "name",
            "description",
            "exercises",
            "is_public"
        )


class WorkoutPlanSerializer(serializers.ModelSerializer):

    workout_program = serializers.ReadOnlyField(source="workout_program.name")

    class Meta:
        model = WorkoutPlan
        fields = (
            "client",
            "name",
            "description",
            "workout_program",
            "date_time",
            "is_completed",
            "notes",
        )


class WorkoutPlanWithProgramSerializer(serializers.ModelSerializer):

    workout_program = WorkoutProgramSerializer()

    class Meta:
        model = WorkoutPlan
        fields = (
            "client",
            "name",
            "description",
            "workout_program",
            "date-time",
            "is_completed",
            "notes",
        )
