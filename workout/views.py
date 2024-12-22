from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response

from user.models import ClientUser, TrainerUser
from workout_tracking.permissions import (
    IsAdminOrTrainerPermission,
    IsAdminOrClientPermission,
)
from .models import WorkoutProgram, WorkoutPlan, WorkoutExercise
from .serializers import (
    WorkoutProgramSerializer,
    WorkoutProgramWithExerciseSerializer,
    WorkoutPlanSerializer,
    WorkoutPlanWithProgramSerializer,
    WorkoutExerciseSerializer,
)


class WorkoutProgramViewSet(viewsets.ModelViewSet):
    queryset = WorkoutProgram.objects.prefetch_related("exercises")
    serializer_class = WorkoutProgramSerializer
    permission_classes = []

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "retrieve":
            return WorkoutProgramWithExerciseSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            '''
            админ видит все программы,
            тренер видит созданные им программы, 
            клиент - созданные для него,
            неавторизованные пользователи видят только публичные программы
            '''
            if user.is_admin:
                return self.queryset.all()
            return self.queryset.filter(
                Q(trainer=user) |
                Q(client=user) |
                Q(is_public=True)
            )
        return self.queryset.filter(is_public=True)

    def create(self, request, *args, **kwargs):
        self.permission_classes.append(IsAdminOrTrainerPermission)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_admin:
            trainer_pk = self.request.data.get("trainer")
            trainer = get_object_or_404(TrainerUser, pk=trainer_pk)
        else:
            trainer = user

        client_pk = self.request.data.get("client")
        is_public = self.request.data.get("is_public", False)

        if is_public:
            client = None
        else:
            if client_pk:
                client = get_object_or_404(ClientUser, pk=client_pk)
            else:
                raise serializers.ValidationError(
                    "You must specify a client "
                    "or make the workout program public."
                )
        serializer.save(trainer=trainer, client=client, is_public=is_public)

    def retrieve(self, request, *args, **kwargs):

        instance = get_object_or_404(WorkoutProgram, pk=kwargs["pk"])

        if not request.user.is_authenticated:
            # Если не авторизован, проверяем, является ли программа публичной
            if instance.is_public:
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                return Response(
                    {
                        "detail": "You don't have permission "
                                  "to view this program."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

        else:
            if (
                    instance.is_public or
                    request.user.is_admin or
                    instance.trainer == request.user or
                    instance.client == request.user
            ):
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            return Response(
                {
                    "detail": "You don't have permission "
                              "to view this program."
                },
                status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        self.permission_classes.append(IsAdminOrTrainerPermission)

        instance = get_object_or_404(self.get_queryset(), pk=kwargs["pk"])
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        self.permission_classes.append(IsAdminOrTrainerPermission)

        instance = get_object_or_404(self.get_queryset(), pk=kwargs["pk"])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkoutExerciseViewSet(viewsets.ModelViewSet):
    queryset = WorkoutExercise.objects.select_related("workout_program")
    serializer_class = WorkoutExerciseSerializer
    permission_classes = [IsAdminOrTrainerPermission]


class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = (
        WorkoutPlan.objects
        .select_related("workout_program")
        .prefetch_related("exercises")
    )
    serializer_class = WorkoutPlanSerializer
    permission_classes = [IsAdminOrClientPermission]

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "retrieve":
            return WorkoutPlanWithProgramSerializer
        return super().get_serializer_class()
