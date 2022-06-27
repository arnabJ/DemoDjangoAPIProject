from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apiV1.models import Address
from apiV1.serializers import RegistrationSerializer, UpdateUserSerializer, AddressSerializer


class RegistrationAPIView(APIView):
    @staticmethod
    def post(request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "Registration successful!"
            data['id'] = user.id
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    @staticmethod
    def post(request):
        json_response = {}
        http_status = status.HTTP_200_OK
        error_messages = []

        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or username == '':
            error_messages.append("'username' is required.")
        if password is None or password == '':
            error_messages.append("'password' is required.")

        if len(error_messages) == 0:
            try:
                user = authenticate(username=username, password=password)
                if user is not None:
                    token = Token.objects.get_or_create(user=user)
                    json_response.update({
                        "token": token[0].key,
                        "user": {
                            "id": user.id,
                            "email": user.email,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "username": user.username
                        }
                    })
                else:
                    json_response.update({"error": "Please verify your username and/or password and try again."})
                    http_status = status.HTTP_401_UNAUTHORIZED
            except Exception as e:
                print(e)
                json_response.update({"error": "Something went wrong, please try again later."})
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            json_response.update({
                "error": error_messages
            })
            http_status = status.HTTP_400_BAD_REQUEST

        return JsonResponse(json_response, status=http_status)


class FetchUserDataAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def get(request):
        json_response = {
            "id": request.user.id,
            "email": request.user.email,
            "firstName": request.user.first_name,
            "lastName": request.user.last_name,
            "username": request.user.username,
        }

        return JsonResponse(json_response)


class UpdateUserAPIView(generics.GenericAPIView, mixins.UpdateModelMixin):
    """API for updating user data."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    lookup_field = 'id'
    pagination_class = None

    def put(self, request, id):
        return self.update(request, id)


# noinspection PyShadowingBuiltins
class AddressAPIView(
    generics.GenericAPIView, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'id'

    def post(self, request, id):
        return self.create(request)

    def get(self, request, id):
        return self.retrieve(request, id)

    def put(self, request, id):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)


class FetchAddressesAPIView(
    generics.GenericAPIView, mixins.ListModelMixin
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all().order_by('id')
    serializer_class = AddressSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['line_one', 'line_two', 'city', 'state', 'country', 'zip_code']
    filterset_fields = ['city', 'state', 'country', 'zip_code']

    def get(self, request):
        return self.list(request)
