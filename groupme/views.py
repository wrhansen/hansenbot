import logging
from typing import List

from rest_framework.response import Response
from rest_framework.views import APIView

from .bots import ParseError, parse_command, registry
from .serializers import MessageSerializer

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

        try:
            command, *args = parse_command(serializer.validated_data["text"])
        except ParseError as e:
            logger.info(
                f"No command parsed from message. Request: {request.data}, validated_data: {serializer.validated_data} | ERROR: {e}",
                extra={"request": request.data, "error": e},
            )
            return Response({}, status=400)

        try:
            Bot = registry[command]
        except KeyError:
            logger.info(
                f"Unknown command `{command}`",
                extra={
                    "command": command,
                    "args": args,
                },
            )

            return Response({}, status=400)

        bot = Bot(*args, **serializer.validated_data)
        bot.execute()

        return Response({}, status=200)
