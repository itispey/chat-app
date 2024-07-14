from django.contrib.auth import get_user_model
from rest_framework import generics, mixins, status, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer


class LoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')
        User = get_user_model()
        user, created = User.objects.get_or_create(phone_number=phone_number)
        # normally we have to verify OTP on a separate view
        if otp == '12345':
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        return Response({'message': 'otp is invalid'}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(mixins.ListModelMixin, generics.GenericAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['phone_number', 'username']
    ordering_fields = ['id', 'phone_number', 'username']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
