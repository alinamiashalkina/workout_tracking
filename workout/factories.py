from datetime import timedelta
from random import choice, randint

import factory.fuzzy
from django.utils import timezone
from faker import Faker

from exercise.factories import ExerciseFactory
from user.factories import TrainerUserFactory, ClientUserFactory
from .models import WorkoutProgram, WorkoutExercise, WorkoutPlan

faker = Faker()


class WorkoutExerciseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WorkoutExercise
        django_get_or_create = ("workout_program", "exercise",)

    workout_program = factory.SelfAttribute("..")
    exercise = factory.SubFactory(ExerciseFactory)
    repetitions = factory.LazyAttribute(
        lambda _: choice([None, randint(1, 50)])
    )
    duration = factory.LazyAttribute(
        lambda _: choice([None, randint(60, 60 * 30)])
    )


class WorkoutProgramFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WorkoutProgram

    trainer = factory.SubFactory(TrainerUserFactory)
    client = factory.SubFactory(ClientUserFactory)
    name = factory.LazyAttribute(lambda _: faker.sentence()[:50])
    description = factory.Faker("text", max_nb_chars=300)

    @factory.post_generation
    def exercises(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for exercise in extracted:
                WorkoutExerciseFactory(workout_program=self, exercise=exercise)
        else:
            for _ in range(3):
                WorkoutExerciseFactory(workout_program=self)

    @factory.lazy_attribute
    def is_public(self):
        return self.client is None


class WorkoutPlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WorkoutPlan

    workout_program = factory.SubFactory(WorkoutProgramFactory)
    # клиент будет тот же, который в программе тренировки
    client = factory.LazyAttribute(lambda o: o.workout_program.client)
    name = factory.LazyAttribute(lambda _: faker.sentence()[:20])
    description = factory.Faker("text", max_nb_chars=300)

    date_time = factory.LazyFunction(
        lambda: timezone.now() + timedelta(days=randint(0, 30))
    )
    is_completed = factory.Faker("boolean")
    notes = factory.Faker("text", max_nb_chars=300)
