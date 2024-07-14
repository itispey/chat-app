from rest_framework import generics, permissions, viewsets, status, filters
from rest_framework.response import Response
from .models import Chat, Message, User
from .serializers import ChatSerializer, MessageSerializer


class ChatListView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['id']

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(members=user)

    def create(self, request, *args, **kwargs):
        user = request.user
        target_id = request.data.get('target_id')
        if not target_id:
            return Response({'message': 'Target user id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target_user = User.objects.get(id=target_id)
        except User.DoesNotExist:
            return Response(
                {"message": "Target user not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        chat = Chat.objects.create()
        chat.members.add(user)
        chat.members.add(target_user)
        chat.save()

        serializer = self.get_serializer(chat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def perform_create(self, serializer):
    #     members = serializer.validated_data.get('members', [])
    #     if not members:
    #         return Response({'message': 'members field required'}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     members.append(self.request.user)
    #     members = list(set(members))
    #     serializer.save(members=members)


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    # search_fields = ['id', 'sender', 'content']
    ordering_fields = ['id', 'sender', 'timestamp']

    def get_queryset(self):
        # we can simply use chat_id or something like uuid to get the messages
        # but here we use target_id to get the messages
        current_user_id = self.request.user.id
        target_id = self.kwargs['pk']
        chat = Chat.objects.filter(
            members__id=current_user_id
        ).filter(
            members__id=target_id
        )

        return Message.objects.filter(chat__in=chat)
