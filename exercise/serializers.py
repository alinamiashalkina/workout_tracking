from rest_framework import serializers

from .models import Exercise, Category


class ExerciseSerializer(serializers.ModelSerializer):

    category = serializers.ReadOnlyField(source="category.name")

    class Meta:
        model = Exercise
        fields = (
            "pk",
            "name",
            "description",
            "category",
            "video",
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            "pk",
            "name",
        )
