from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chatbot.services.chat_service import ChatService
from chatbot.api.serializers import CHAT_MESSAGE_SERIALIZER


class ChatAPIView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = CHAT_MESSAGE_SERIALIZER

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        service = ChatService()
        message = serializer.validated_data["message"]

        reply = service.process_message(
            user=request.user,
            message=message
        )

        return Response(
            {
                "reply": reply
            }
        )