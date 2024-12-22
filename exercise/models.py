from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        related_name="exercises",
        on_delete=models.CASCADE,
    )
    video = models.FileField(upload_to="video/", null=True, blank=True)

    def __str__(self):
        return f"{self.name}, category: {self.category.name}"
