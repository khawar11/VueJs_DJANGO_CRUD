from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from django.middleware import csrf
from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .serializers import CustomerSerializer
from .models import Customer
import logging
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)


def home_view(request):
    return render(request, 'home.html')


@api_view(['POST'])
def user_signup(request):
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Validation logic here
        try:
            # Check if a user with the same username or email already exists
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                return Response({'error': 'username or email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            # If not, create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            # Handle other database integrity errors if needed
            return Response({'error': 'User registration failed.'}, status=status.HTTP_400_BAD_REQUEST)


# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=username, email=email, password=password)

        if user is not None:
            login(request, user)
            # Return an authentication token or session ID here
            return Response({'message': 'User logged in successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not found.'}, status=status.HTTP_400_BAD_REQUEST)


def get_csrf_token(request):
    # Get the CSRF token
    csrf_token = csrf.get_token(request)

    # Return the token as JSON response
    return JsonResponse({'csrf_token': csrf_token})


class CustomerList(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetail(RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.debug("Received PUT request data: %s", request.data)
        logger.debug("Existing customer data: %s", instance)

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.debug("Updated customer data: %s", serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            logger.error("Serializer errors: %s", serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['DELETE'])
def delete_customer(request, customer_id):
    try:
        customer = get_object_or_404(Customer, id=customer_id)
        customer.delete()
        return JsonResponse({'success': True, 'message': 'Customer deleted successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
