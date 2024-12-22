"""
URL configuration for workout_tracking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from exercise.views import CategoryViewSet, ExerciseViewSet
from user.views import RegisterView, LoginView, LogoutView
from workout.views import (
    WorkoutProgramViewSet,
    WorkoutExerciseViewSet,
    WorkoutPlanViewSet
)
from . import settings

default_router = DefaultRouter()

default_router.register("api/category", CategoryViewSet,
                        "exercise_category"
                        )
default_router.register("api/exercise", ExerciseViewSet,
                        "exercise"
                        )
default_router.register("api/workout_program", WorkoutProgramViewSet,
                        "workout_program"
                        )
default_router.register("api/workout_exercise", WorkoutExerciseViewSet,
                        "workout_exercise"
                        )
default_router.register("api/workout_plan", WorkoutPlanViewSet,
                        "workout_plan"
                        )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/registration/', RegisterView.as_view(), name='registration'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
] + default_router.urls + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
