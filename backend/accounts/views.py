from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Account
from .serializers import RegisterSerializer, LoginSerializer
from .tokens import CustomTokenObtainPairSerializer
from .permissions import IsAuthenticatedUser
from audit.services import log_action

from records.services import submissions_count_for_year

class TokenView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    ser = RegisterSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    email = ser.validated_data["email"]
    password = ser.validated_data["password"]

    if Account.objects.filter(email=email).exists():
        return Response({"error": "EMAIL_EXISTS"}, status=status.HTTP_409_CONFLICT)

    user = Account.objects.create_user(email=email, password=password, role="USER")
    refresh = RefreshToken.for_user(user)
    log_action(user, "REGISTER", "ACCOUNT", target_id=user.uid)

    return Response({
        "user_id": user.uid,
        "email": user.email,
        "role": user.role,
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    ser = LoginSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    email = ser.validated_data["email"]
    password = ser.validated_data["password"]

    user = authenticate(request, username=email, password=password)
    if not user:
        return Response({"error": "INVALID_CREDENTIALS"}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    user.last_login_at = timezone.now()
    user.save(update_fields=["last_login_at"])
    log_action(user, "LOGIN", "ACCOUNT", target_id=user.uid)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user_id": user.uid,
        "role": user.role,
    })

@api_view(["POST"])
@permission_classes([AllowAny])
def refresh(request):
    token = request.data.get("refresh")
    if not token:
        return Response({"error": "MISSING_REFRESH"}, status=400)
    try:
        refresh_token = RefreshToken(token)
        return Response({"access": str(refresh_token.access_token)})
    except Exception:
        return Response({"error": "INVALID_REFRESH"}, status=401)

@api_view(["GET"])
@permission_classes([IsAuthenticatedUser])
def me(request):
    now = timezone.localtime(timezone.now())
    year = now.year
    cnt = submissions_count_for_year(request.user.uid, year)
    remaining = max(0, 2 - cnt)
    return Response({
        "user_id": request.user.uid,
        "email": request.user.email,
        "role": request.user.role,
        "year": year,
        "submissions_this_year": cnt,
        "remaining_this_year": remaining,
    })

@api_view(["GET"])
def health(request):
    return Response({"ok": True})
