from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", _("Admin")
        TRAINER = "trainer", _("Trainer")
        CLIENT = "client", _("Client")

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CLIENT,
    )

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_trainer(self):
        return self.role == self.Role.TRAINER

    @property
    def is_client(self):
        return self.role == self.Role.CLIENT


class AdminManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Role.ADMIN)


class Admin(User):
    class Meta:
        proxy = True

    objects = AdminManager()


class TrainerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Role.TRAINER)


class TrainerUser(User):
    class Meta:
        proxy = True

    objects = TrainerManager()


class ClientManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=User.Role.CLIENT)


class ClientUser(User):
    class Meta:
        proxy = True

    objects = ClientManager()
