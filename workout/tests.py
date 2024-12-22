from rest_framework import status
from rest_framework.reverse import reverse

from user.factories import TrainerUserFactory, ClientUserFactory, AdminFactory
from workout_tracking.tests import TestCase
from .factories import WorkoutProgramFactory


class WorkoutProgramVisibilityTests(TestCase):

    def setUp(self):

        self.admin_user = AdminFactory()
        self.trainer_user = TrainerUserFactory()
        self.client_user = ClientUserFactory()
        self.trainer_user2 = TrainerUserFactory()
        self.client_user2 = ClientUserFactory()

        self.public_program = WorkoutProgramFactory(
            name="Public Program",
            client=None
        )
        self.trainer_program = WorkoutProgramFactory(
            name="Trainer Program",
            trainer=self.trainer_user,
            client=self.client_user2
        )
        self.client_program = WorkoutProgramFactory(
            name="Client Program",
            trainer=self.trainer_user2,
            client=self.client_user
        )

    def test_admin_sees_all_programs(self):
        self.set_user(self.admin_user)
        response = self.client.get(reverse("workout_program-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_trainer_sees_own_and_public_programs(self):
        self.set_user(self.trainer_user)
        response = self.client.get(reverse("workout_program-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Тренер должен видеть 1 свою программу и 1 публичную
        self.assertEqual(len(response.data), 2)

    def test_client_sees_own_and_public_programs(self):
        self.set_user(self.client_user)
        response = self.client.get(reverse("workout_program-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Клиент должен видеть 1 свою программу и 1 публичную
        self.assertEqual(len(response.data), 2)

    def test_unauthenticated_user_sees_public_programs(self):
        response = self.client.get(reverse("workout_program-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Неавторизованный должен видеть только 1 публичную программу
        self.assertEqual(len(response.data), 1)
        # Проверяем, что это именно публичная программа
        self.assertEqual(response.data[0]["name"], "Public Program")

    def test_admin_can_see_detail_all_programs(self):
        self.set_user(self.admin_user)
        for program in [
            self.public_program,
            self.trainer_program,
            self.client_program
        ]:
            with self.subTest(program=program):
                response = self.client.get(reverse(
                    "workout_program-detail",
                    args=[program.pk])
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_trainer_can_see_detail_own_and_public_programs(self):
        self.set_user(self.trainer_user)
        available_programs = [self.trainer_program, self.public_program]

        for program in available_programs:
            with self.subTest(program=program):
                response = self.client.get(reverse(
                    "workout_program-detail",
                    args=[program.pk])
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)

        not_available_program = self.client_program
        response = self.client.get(reverse(
            "workout_program-detail",
            args=[not_available_program.pk])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_client_can_see_detail_own_and_public_programs(self):
        self.set_user(self.client_user)
        available_programs = [self.client_program, self.public_program]

        for program in available_programs:
            with self.subTest(program=program):
                response = self.client.get(reverse(
                    "workout_program-detail",
                    args=[program.pk])
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)

        not_available_program = self.trainer_program
        response = self.client.get(reverse(
            "workout_program-detail",
            args=[not_available_program.pk])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_unauthenticated_user_can_see_detail_only_public_programs(self):

        available_program = self.public_program
        response = self.client.get(reverse(
            "workout_program-detail",
            args=[available_program.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        unavailable_programs = [self.client_program, self.trainer_program]
        for program in unavailable_programs:
            with self.subTest(program=program):
                response = self.client.get(reverse(
                    "workout_program-detail",
                    args=[program.pk])
                )
                self.assertEqual(
                    response.status_code,
                    status.HTTP_403_FORBIDDEN
                )
