import logging
from typing import List

from rest_framework.response import Response
from rest_framework.views import APIView

from .bots import ParseError, parse_command, registry
from .serializers import MessageSerializer
from .tasks import handle_bot_message

logger = logging.getLogger(__name__)


class HansenBotWebhook(APIView):
    permission_classes: List[str] = []
    authentication_classes: List[str] = []

    def post(self, request):

        serializer = MessageSerializer(data=request.data)
        valid = serializer.is_valid()
        if not valid:
            logger.info(
                f"Invalid Message! Request: {request.data} | ERRORS: {serializer.errors}",
                extra={"errors": serializer.errors, "request": request.data},
            )
            return Response({}, status=400)

        handle_bot_message(**serializer.validated_data)

        return Response({}, status=200)
