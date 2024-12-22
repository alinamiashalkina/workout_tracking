from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class TestCase(APITestCase):
    user = None

    def set_user(self, user):
        if user is None:
            self.user = None
            self.client.credentials(HTTP_AUTHORIZATION="")
            return

        self.user = user
        self.client.credentials(
            HTTP_AUTHORIZATION=
            f"Bearer {get_tokens_for_user(self.user)["access"]}"
        )
