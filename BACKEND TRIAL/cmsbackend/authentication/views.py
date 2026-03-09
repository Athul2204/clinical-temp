from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import CustomTokenObtainPairSerializer, LoginActivitySerializer
from .models import LoginActivity
from .utils import get_client_ip



from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status

from .serializers import CustomTokenObtainPairSerializer
from .models import LoginActivity
from .utils import get_client_ip


class LoginView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        response_data = serializer.validated_data

        user = serializer.user   # ✅ Correct way

        # save login activity
        LoginActivity.objects.create(
            user=user,
            ip_address=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT")
        )

        return Response(response_data, status=status.HTTP_200_OK)
    

class LoginActivityView(APIView):
    """
    View login history
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        logs = LoginActivity.objects.filter(user=request.user)

        serializer = LoginActivitySerializer(logs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)