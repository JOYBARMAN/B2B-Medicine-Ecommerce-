from rest_framework.generics import RetrieveUpdateAPIView

from common.renderers import ErrorRenderers
from core.permissions import IsAuthenticated
from user_profile.models import Profile
from user_profile.rest.serializers.profile import ProfileSerializer


class ProfileDetail(RetrieveUpdateAPIView):
    """Views to profile detail and update"""

    serializer_class = ProfileSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    renderer_classes = [
        ErrorRenderers,
    ]

    def get_object(self):
        return (
            Profile()
            .get_all_actives()
            .select_related("user")
            .get(user=self.request.user)
        )
