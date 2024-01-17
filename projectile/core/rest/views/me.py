from rest_framework.generics import RetrieveUpdateAPIView

from common.renderers import ErrorRenderers
from core.permissions import IsActivatedUser
from core.rest.serializers.me import MeDetailSerializer


class MeDetail(RetrieveUpdateAPIView):
    """Views to me detail and update"""

    serializer_class = MeDetailSerializer
    permission_classes = (IsActivatedUser,)
    # renderer_classes = [ErrorRenderers]

    def get_object(self):
        return self.request.user
